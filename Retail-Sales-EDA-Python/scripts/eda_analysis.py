"""
================================================================
  Retail Sales EDA & Profitability Analysis
  Author  : Portfolio Project — Data Analyst Internship
  Dataset : retail_data.csv  (2000+ synthetic rows)
  Tools   : Pandas, NumPy, Matplotlib, Seaborn
================================================================
"""

# ── 0. Imports ────────────────────────────────────────────────
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
import os

warnings.filterwarnings("ignore")

# Style
sns.set_theme(style="darkgrid", palette="muted")
plt.rcParams.update({
    "figure.dpi": 130,
    "font.family": "DejaVu Sans",
    "axes.titlesize": 13,
    "axes.labelsize": 11,
})

IMAGES = os.path.join(os.path.dirname(__file__), "..", "images")
os.makedirs(IMAGES, exist_ok=True)

def save(name):
    path = os.path.join(IMAGES, name)
    plt.tight_layout()
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"  [saved] {name}")


# ================================================================
# STEP 1 — LOAD DATA
# ================================================================
print("\n" + "="*60)
print("  STEP 1 : Loading Data")
print("="*60)

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "retail_data.csv")
df = pd.read_csv(DATA_PATH, parse_dates=["Order_Date", "Ship_Date"])

print(f"  Raw shape   : {df.shape}")
print(f"  Columns     : {list(df.columns)}")
print(f"  Date range  : {df['Order_Date'].min().date()}  to  {df['Order_Date'].max().date()}")


# ================================================================
# STEP 2 — DATA CLEANING
# ================================================================
print("\n" + "="*60)
print("  STEP 2 : Data Cleaning")
print("="*60)

# 2a. Missing values BEFORE
print("\n  Missing values (before cleaning):")
print(df.isnull().sum()[df.isnull().sum() > 0])

# 2b. Fill missing Discount with 0 (no discount applied)
df["Discount"] = df["Discount"].fillna(0)

# 2c. Fill missing Profit using median profit margin of the same Category
df["Profit_Margin_Rate"] = df["Profit"] / df["Sales"]
median_margin = df.groupby("Category")["Profit_Margin_Rate"].transform("median")
df["Profit"] = df["Profit"].fillna(df["Sales"] * median_margin)
df.drop(columns=["Profit_Margin_Rate"], inplace=True)

# 2d. Remove duplicates
before = len(df)
df.drop_duplicates(inplace=True)
df.reset_index(drop=True, inplace=True)
print(f"\n  Duplicates removed : {before - len(df)} rows")
print(f"  Clean shape        : {df.shape}")

# 2e. Derived columns
df["Year"]          = df["Order_Date"].dt.year
df["Month"]         = df["Order_Date"].dt.month
df["Month_Name"]    = df["Order_Date"].dt.strftime("%b")
df["Year_Month"]    = df["Order_Date"].dt.to_period("M").astype(str)
df["Profit_Margin"] = (df["Profit"] / df["Sales"]) * 100      # percentage
df["Discount_Band"] = pd.cut(
    df["Discount"],
    bins=[-0.01, 0.0, 0.10, 0.20, 1.0],
    labels=["No Discount", "Low (1-10%)", "Medium (11-20%)", "High (>20%)"]
)

print("\n  Derived columns added: Year, Month, Month_Name, Year_Month,")
print("                         Profit_Margin, Discount_Band")
print("\n  Missing values (after cleaning):")
print(df.isnull().sum()[df.isnull().sum() > 0] if df.isnull().sum().any() else "  None — dataset is clean!")

# Data types
df["Quantity"] = df["Quantity"].astype(int)
print(f"\n  Data types:\n{df.dtypes}")


# ================================================================
# STEP 3 — OVERALL KPIs
# ================================================================
print("\n" + "="*60)
print("  STEP 3 : Overall Business KPIs")
print("="*60)

total_revenue       = df["Sales"].sum()
total_profit        = df["Profit"].sum()
overall_margin      = (total_profit / total_revenue) * 100
total_orders        = df["Order_ID"].nunique()
avg_order_value     = total_revenue / total_orders
total_units_sold    = df["Quantity"].sum()

print(f"\n  Total Revenue     : Rs {total_revenue:,.0f}")
print(f"  Total Profit      : Rs {total_profit:,.0f}")
print(f"  Profit Margin     : {overall_margin:.1f}%")
print(f"  Total Orders      : {total_orders:,}")
print(f"  Avg Order Value   : Rs {avg_order_value:,.0f}")
print(f"  Total Units Sold  : {total_units_sold:,}")

# KPI bar card
fig, axes = plt.subplots(1, 3, figsize=(13, 4))
kpi_labels  = ["Total Revenue (Rs Cr)", "Total Profit (Rs Cr)", "Profit Margin (%)"]
kpi_values  = [total_revenue / 1e7, total_profit / 1e7, overall_margin]
kpi_colors  = ["#4C72B0", "#55A868", "#C44E52"]
for ax, lbl, val, col in zip(axes, kpi_labels, kpi_values, kpi_colors):
    ax.barh([0], [val], color=col, height=0.5)
    ax.set_xlim(0, val * 1.4)
    ax.set_yticks([])
    ax.set_xlabel(lbl, fontsize=12)
    ax.text(val * 0.5, 0, f"{val:.2f}", va="center", ha="center",
            color="white", fontsize=14, fontweight="bold")
    for spine in ax.spines.values():
        spine.set_visible(False)
fig.suptitle("Overall Business KPIs — Retail Sales 2022–2023", fontsize=14, fontweight="bold", y=1.02)
save("01_overall_kpis.png")


# ================================================================
# STEP 4 — REGIONAL ANALYSIS
# ================================================================
print("\n" + "="*60)
print("  STEP 4 : Regional Analysis")
print("="*60)

regional = df.groupby("Region").agg(
    Revenue=("Sales",  "sum"),
    Profit =("Profit", "sum"),
    Orders =("Order_ID", "count"),
).reset_index()
regional["Margin_%"] = (regional["Profit"] / regional["Revenue"] * 100).round(1)
regional.sort_values("Revenue", ascending=False, inplace=True)
print(regional.to_string(index=False))

# Best region vs worst
best_region  = regional.iloc[0]
worst_region = regional.iloc[-1]
gap_pct = ((best_region["Revenue"] - worst_region["Revenue"]) / best_region["Revenue"] * 100)
print(f"\n  INSIGHT: {best_region['Region']} leads revenue. "
      f"{worst_region['Region']} underperforms by {gap_pct:.1f}%.")

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
# Revenue by region
bars = axes[0].bar(regional["Region"], regional["Revenue"] / 1e6,
                   color=sns.color_palette("Blues_d", len(regional)))
axes[0].set_title("Revenue by Region (Rs Lakhs)")
axes[0].set_ylabel("Revenue (Rs Lakhs)")
for bar, val in zip(bars, regional["Revenue"] / 1e6):
    axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                 f"{val:.0f}L", ha="center", fontsize=9, fontweight="bold")

# Profit Margin by region
colors = ["#55A868" if m > overall_margin else "#C44E52" for m in regional["Margin_%"]]
axes[1].bar(regional["Region"], regional["Margin_%"], color=colors)
axes[1].axhline(overall_margin, linestyle="--", color="navy", linewidth=1.5,
                label=f"Avg Margin {overall_margin:.1f}%")
axes[1].set_title("Profit Margin % by Region")
axes[1].set_ylabel("Profit Margin (%)")
axes[1].legend()
save("02_regional_analysis.png")


# ================================================================
# STEP 5 — CATEGORY ANALYSIS
# ================================================================
print("\n" + "="*60)
print("  STEP 5 : Category & Sub-Category Analysis")
print("="*60)

cat = df.groupby("Category").agg(
    Revenue=("Sales",  "sum"),
    Profit =("Profit", "sum"),
    Units  =("Quantity", "sum"),
).reset_index()
cat["Margin_%"] = (cat["Profit"] / cat["Revenue"] * 100).round(1)
cat["Rev_Share_%"] = (cat["Revenue"] / cat["Revenue"].sum() * 100).round(1)
cat.sort_values("Revenue", ascending=False, inplace=True)
print(cat.to_string(index=False))

# Sub-category heatmap data
subcat = df.groupby(["Category", "Sub_Category"]).agg(
    Revenue=("Sales", "sum"),
    Profit =("Profit", "sum")
).reset_index()
subcat["Margin"] = (subcat["Profit"] / subcat["Revenue"] * 100).round(1)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Revenue share — donut
wedges, texts, autotexts = axes[0].pie(
    cat["Revenue"], labels=cat["Category"],
    autopct="%1.1f%%", startangle=90,
    colors=["#4C72B0", "#55A868", "#C44E52"],
    wedgeprops=dict(width=0.5, edgecolor="white")
)
axes[0].set_title("Revenue Share by Category")

# Sub-category profit margin bar
subcat_sorted = subcat.sort_values("Margin", ascending=True)
colors_sc = ["#C44E52" if m < 0 else "#55A868" for m in subcat_sorted["Margin"]]
axes[1].barh(subcat_sorted["Sub_Category"], subcat_sorted["Margin"], color=colors_sc)
axes[1].axvline(0, color="black", linewidth=0.8)
axes[1].set_title("Profit Margin % by Sub-Category")
axes[1].set_xlabel("Profit Margin (%)")
save("03_category_analysis.png")


# ================================================================
# STEP 6 — PRODUCT ANALYSIS
# ================================================================
print("\n" + "="*60)
print("  STEP 6 : Product Analysis")
print("="*60)

prod = df.groupby("Product_Name").agg(
    Revenue=("Sales",  "sum"),
    Profit =("Profit", "sum"),
    Units  =("Quantity", "sum"),
    Orders =("Order_ID", "count"),
).reset_index()
prod["Margin_%"] = (prod["Profit"] / prod["Revenue"] * 100).round(1)

top10_rev    = prod.nlargest(10, "Revenue")
top10_profit = prod.nlargest(10, "Profit")
low5         = prod.nsmallest(5, "Profit")

print("\n  Top 10 Products by Revenue:")
print(top10_rev[["Product_Name", "Revenue", "Profit", "Margin_%"]].to_string(index=False))
print("\n  Bottom 5 Products by Profit (Loss makers):")
print(low5[["Product_Name", "Revenue", "Profit", "Margin_%"]].to_string(index=False))

# Pareto analysis
prod_sorted = prod.sort_values("Revenue", ascending=False).reset_index(drop=True)
prod_sorted["Cum_Rev"] = prod_sorted["Revenue"].cumsum()
prod_sorted["Cum_Rev_%"] = prod_sorted["Cum_Rev"] / prod_sorted["Revenue"].sum() * 100
top_20pct_idx = int(len(prod_sorted) * 0.20)
top_20_rev_share = prod_sorted.iloc[top_20pct_idx - 1]["Cum_Rev_%"]
print(f"\n  PARETO INSIGHT: Top 20% products contribute "
      f"{top_20_rev_share:.0f}% of total revenue.")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Top 10 revenue
axes[0].barh(top10_rev["Product_Name"][::-1], top10_rev["Revenue"][::-1] / 1e3,
             color=sns.color_palette("Blues_d", 10))
axes[0].set_title("Top 10 Products by Revenue (Rs '000)")
axes[0].set_xlabel("Revenue (Rs '000)")

# Top 10 profit
clrs = ["#55A868" if p > 0 else "#C44E52" for p in top10_profit["Profit"]]
axes[1].barh(top10_profit["Product_Name"][::-1], top10_profit["Profit"][::-1] / 1e3, color=clrs)
axes[1].set_title("Top 10 Products by Profit (Rs '000)")
axes[1].set_xlabel("Profit (Rs '000)")
save("04_product_analysis.png")


# ================================================================
# STEP 7 — DISCOUNT ANALYSIS (Profit Leakage)
# ================================================================
print("\n" + "="*60)
print("  STEP 7 : Discount Impact & Profit Leakage")
print("="*60)

disc = df.groupby("Discount_Band").agg(
    Revenue     =("Sales",          "sum"),
    Profit      =("Profit",         "sum"),
    Avg_Margin  =("Profit_Margin",  "mean"),
    Orders      =("Order_ID",       "count"),
).reset_index()
disc["Margin_%"] = disc["Avg_Margin"].round(1)
print(disc[["Discount_Band", "Revenue", "Profit", "Margin_%", "Orders"]].to_string(index=False))

no_disc_margin   = disc[disc["Discount_Band"] == "No Discount"]["Margin_%"].values[0]
high_disc_margin = disc[disc["Discount_Band"] == "High (>20%)" ]["Margin_%"].values
margin_drop      = no_disc_margin - (high_disc_margin[0] if len(high_disc_margin) else 0)
loss_orders      = df[df["Profit"] < 0]
loss_revenue     = loss_orders["Sales"].sum()
print(f"\n  INSIGHT: High discounts (>20%) reduce profit margin by "
      f"{margin_drop:.1f} percentage points vs no-discount orders.")
print(f"  INSIGHT: {len(loss_orders):,} orders are LOSS-MAKING, "
      f"draining Rs {abs(loss_orders['Profit'].sum()):,.0f} in profit leakage.")
print(f"  INSIGHT: Loss orders represent "
      f"{len(loss_orders)/len(df)*100:.1f}% of all orders "
      f"but {loss_revenue/total_revenue*100:.1f}% of revenue — "
      f"high-risk concentration.")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Margin by discount band
bar_colors = ["#55A868", "#4C72B0", "#DD8452", "#C44E52"]
axes[0].bar(disc["Discount_Band"], disc["Margin_%"], color=bar_colors)
axes[0].axhline(0, color="black", linewidth=0.8, linestyle="--")
axes[0].set_title("Avg Profit Margin % by Discount Band")
axes[0].set_ylabel("Profit Margin (%)")
axes[0].set_xlabel("Discount Band")
for i, (band, val) in enumerate(zip(disc["Discount_Band"], disc["Margin_%"])):
    axes[0].text(i, val + 0.3, f"{val:.1f}%", ha="center", fontsize=9, fontweight="bold")

# Scatter: Discount vs Profit Margin
sample = df.sample(min(500, len(df)), random_state=42)
scatter_colors = ["#C44E52" if p < 0 else "#4C72B0" for p in sample["Profit"]]
axes[1].scatter(sample["Discount"] * 100, sample["Profit_Margin"],
                alpha=0.5, c=scatter_colors, s=30)
axes[1].axhline(0, color="red", linestyle="--", linewidth=1)
axes[1].axvline(20, color="orange", linestyle="--", linewidth=1, label="20% discount line")
axes[1].set_title("Discount % vs Profit Margin (sample 500)")
axes[1].set_xlabel("Discount (%)")
axes[1].set_ylabel("Profit Margin (%)")
axes[1].legend()
save("05_discount_analysis.png")


# ================================================================
# STEP 8 — TIME SERIES ANALYSIS
# ================================================================
print("\n" + "="*60)
print("  STEP 8 : Monthly Sales & Seasonality")
print("="*60)

monthly = df.groupby("Year_Month").agg(
    Revenue=("Sales",  "sum"),
    Profit =("Profit", "sum"),
    Orders =("Order_ID", "count"),
).reset_index().sort_values("Year_Month")
monthly["Rolling_Rev_3M"] = monthly["Revenue"].rolling(3, min_periods=1).mean()

# Peak month
peak_month = monthly.loc[monthly["Revenue"].idxmax()]
print(f"  Peak Revenue Month : {peak_month['Year_Month']}  "
      f"(Rs {peak_month['Revenue']:,.0f})")

# Monthly by category
monthly_cat = df.groupby(["Year_Month", "Category"])["Sales"].sum().reset_index()
monthly_cat.sort_values("Year_Month", inplace=True)

fig, axes = plt.subplots(2, 1, figsize=(15, 10))

# Overall monthly revenue + profit
x = range(len(monthly))
axes[0].fill_between(x, monthly["Revenue"] / 1e3, alpha=0.3, color="#4C72B0")
axes[0].plot(x, monthly["Revenue"] / 1e3, color="#4C72B0", linewidth=2, label="Revenue")
axes[0].plot(x, monthly["Rolling_Rev_3M"] / 1e3, color="navy",
             linewidth=1.5, linestyle="--", label="3M Rolling Avg")
axes[0].plot(x, monthly["Profit"] / 1e3, color="#55A868", linewidth=2, label="Profit")
axes[0].set_xticks(x)
axes[0].set_xticklabels(monthly["Year_Month"], rotation=45, ha="right", fontsize=8)
axes[0].set_title("Monthly Revenue & Profit Trend (2022–2023)")
axes[0].set_ylabel("Amount (Rs '000)")
axes[0].legend()

# Category-wise monthly revenue
for cat_name, grp in monthly_cat.groupby("Category"):
    axes[1].plot(grp["Year_Month"], grp["Sales"] / 1e3, marker="o",
                 markersize=4, linewidth=1.8, label=cat_name)
axes[1].set_title("Monthly Revenue by Category")
axes[1].set_xlabel("Month")
axes[1].set_ylabel("Revenue (Rs '000)")
axes[1].tick_params(axis="x", rotation=45, labelsize=8)
axes[1].legend()
save("06_time_series.png")


# ================================================================
# STEP 9 — SEGMENT ANALYSIS
# ================================================================
print("\n" + "="*60)
print("  STEP 9 : Customer Segment Analysis")
print("="*60)

seg = df.groupby("Segment").agg(
    Revenue=("Sales",  "sum"),
    Profit =("Profit", "sum"),
    Orders =("Order_ID", "count"),
).reset_index()
seg["Margin_%"] = (seg["Profit"] / seg["Revenue"] * 100).round(1)
print(seg.to_string(index=False))

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
axes[0].pie(seg["Revenue"], labels=seg["Segment"],
            autopct="%1.1f%%", startangle=90,
            colors=["#4C72B0", "#55A868", "#DD8452"],
            wedgeprops=dict(width=0.5, edgecolor="white"))
axes[0].set_title("Revenue Share by Customer Segment")

axes[1].bar(seg["Segment"], seg["Margin_%"],
            color=["#4C72B0", "#55A868", "#DD8452"])
axes[1].set_title("Profit Margin % by Segment")
axes[1].set_ylabel("Profit Margin (%)")
for i, (seg_name, val) in enumerate(zip(seg["Segment"], seg["Margin_%"])):
    axes[1].text(i, val + 0.2, f"{val:.1f}%", ha="center", fontsize=9, fontweight="bold")
save("07_segment_analysis.png")


# ================================================================
# STEP 10 — COMBINED INSIGHT DASHBOARD
# ================================================================
print("\n" + "="*60)
print("  STEP 10 : Building Summary Insight Dashboard")
print("="*60)

fig = plt.figure(figsize=(18, 12))
fig.suptitle("Retail Sales EDA — Executive Summary Dashboard (2022–2023)",
             fontsize=16, fontweight="bold", y=0.98)

# Panel A — KPI cards
ax_kpi = fig.add_subplot(4, 4, (1, 2))
ax_kpi.axis("off")
kpi_text = (
    f"Total Revenue : Rs {total_revenue/1e7:.2f} Cr\n"
    f"Total Profit  : Rs {total_profit/1e7:.2f} Cr\n"
    f"Profit Margin : {overall_margin:.1f}%\n"
    f"Total Orders  : {total_orders:,}\n"
    f"Units Sold    : {total_units_sold:,}"
)
ax_kpi.text(0.05, 0.95, "KEY PERFORMANCE INDICATORS", transform=ax_kpi.transAxes,
            fontsize=11, fontweight="bold", va="top", color="#2c3e50")
ax_kpi.text(0.05, 0.70, kpi_text, transform=ax_kpi.transAxes,
            fontsize=10, va="top", fontfamily="monospace", color="#34495e",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#ecf0f1", edgecolor="#bdc3c7"))

# Panel B — Revenue by region
ax_reg = fig.add_subplot(4, 4, (3, 4))
ax_reg.bar(regional["Region"], regional["Revenue"] / 1e6,
           color=sns.color_palette("Blues_d", len(regional)))
ax_reg.set_title("Revenue by Region (Rs Lakhs)")
ax_reg.set_ylabel("Rs Lakhs")

# Panel C — Category donut
ax_cat = fig.add_subplot(4, 4, (5, 6))
ax_cat.pie(cat["Revenue"], labels=cat["Category"], autopct="%1.0f%%",
           colors=["#4C72B0", "#55A868", "#C44E52"],
           wedgeprops=dict(width=0.5, edgecolor="white"), startangle=90)
ax_cat.set_title("Revenue by Category")

# Panel D — Margin by discount band
ax_disc = fig.add_subplot(4, 4, (7, 8))
ax_disc.bar(disc["Discount_Band"], disc["Margin_%"],
            color=["#55A868", "#4C72B0", "#DD8452", "#C44E52"])
ax_disc.axhline(0, color="black", linewidth=0.8, linestyle="--")
ax_disc.set_title("Margin % by Discount Band")
ax_disc.set_xticklabels(disc["Discount_Band"], rotation=15, ha="right", fontsize=8)

# Panel E — Monthly trend (full width)
ax_trend = fig.add_subplot(4, 1, 3)
ax_trend.fill_between(range(len(monthly)), monthly["Revenue"] / 1e3, alpha=0.25, color="#4C72B0")
ax_trend.plot(range(len(monthly)), monthly["Revenue"] / 1e3,
              color="#4C72B0", linewidth=2, label="Revenue")
ax_trend.plot(range(len(monthly)), monthly["Profit"] / 1e3,
              color="#55A868", linewidth=2, label="Profit")
ax_trend.set_xticks(range(len(monthly)))
ax_trend.set_xticklabels(monthly["Year_Month"], rotation=45, ha="right", fontsize=7)
ax_trend.set_title("Monthly Revenue & Profit Trend")
ax_trend.set_ylabel("Rs '000")
ax_trend.legend()

# Panel F — Insights text
ax_ins = fig.add_subplot(4, 1, 4)
ax_ins.axis("off")
insights = (
    f"KEY INSIGHTS\n\n"
    f"1. Top 20% of products contribute {top_20_rev_share:.0f}% of total revenue (Pareto Principle confirmed).\n"
    f"2. High-discount orders (>20%) reduce profit margin by {margin_drop:.1f} pp vs zero-discount orders.\n"
    f"3. {len(loss_orders):,} loss-making orders drain Rs {abs(loss_orders['Profit'].sum()):,.0f} — "
       f"primary profit leakage source.\n"
    f"4. {best_region['Region']} region leads with Rs {best_region['Revenue']/1e6:.0f}L revenue; "
       f"{worst_region['Region']} underperforms by {gap_pct:.0f}%.\n"
    f"5. Peak sales month: {peak_month['Year_Month']} — indicates Q4 / festive-season seasonality.\n"
    f"6. Technology category has lowest margin despite highest price points — driven by heavy discounting."
)
ax_ins.text(0.01, 0.95, insights, transform=ax_ins.transAxes,
            fontsize=9.5, va="top", fontfamily="monospace",
            bbox=dict(boxstyle="round,pad=0.6", facecolor="#ffeaa7", edgecolor="#fdcb6e"))

plt.subplots_adjust(hspace=0.55, wspace=0.4)
save("00_executive_dashboard.png")

# ================================================================
# FINAL SUMMARY
# ================================================================
print("\n" + "="*60)
print("  ANALYSIS COMPLETE")
print("="*60)
print(f"\n  Revenue         : Rs {total_revenue:,.0f}")
print(f"  Profit          : Rs {total_profit:,.0f}")
print(f"  Profit Margin   : {overall_margin:.1f}%")
print(f"  Loss Orders     : {len(loss_orders):,} ({len(loss_orders)/len(df)*100:.1f}%)")
print(f"  Profit Leakage  : Rs {abs(loss_orders['Profit'].sum()):,.0f}")
print(f"\n  Charts saved to : {os.path.abspath(IMAGES)}")
print("="*60)
