"""
===============================================================
  Retail Sales EDA — Synthetic Dataset Generator
  Author : Data Analyst Portfolio Project
  Purpose: Generate realistic retail sales data for EDA
===============================================================
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# ── Reproducibility ──────────────────────────────────────────
np.random.seed(42)

# ── Configuration ────────────────────────────────────────────
N_ROWS = 2000          # Number of sales records
START_DATE = datetime(2022, 1, 1)
END_DATE   = datetime(2023, 12, 31)

# ── Master Lists ─────────────────────────────────────────────
REGIONS = ["North", "South", "East", "West"]

CATEGORIES = {
    "Furniture": {
        "Bookcases":    ("Bookcase Pro 5-Shelf", "Bookcase Classic 3-Shelf"),
        "Chairs":       ("Ergonomic Office Chair", "Executive Leather Chair", "Guest Chair"),
        "Tables":       ("Dining Table Oak", "Coffee Table Glass", "Study Desk Compact"),
        "Storage":      ("File Cabinet 4-Drawer", "Storage Box Set", "Wardrobe 3-Door"),
    },
    "Office Supplies": {
        "Binders":      ("Premium Binder A4", "Economy Binder Set", "Presentation Binder"),
        "Paper":        ("A4 Copy Paper 500-Sheet", "Photo Glossy Paper", "Carbon Paper"),
        "Pens & Art":   ("Ballpoint Pen Box", "Sketch Pen Set 24", "Highlighter 6-Pack"),
        "Labels":       ("Address Label Roll", "Barcode Label Set", "Color Dot Labels"),
    },
    "Technology": {
        "Phones":       ("Samsung Galaxy A34", "OnePlus Nord CE 3", "Redmi Note 12"),
        "Laptops":      ("Dell Inspiron 15", "HP Pavilion 14", "Lenovo IdeaPad Slim 5"),
        "Accessories":  ("Wireless Mouse Combo", "USB Hub 7-Port", "Laptop Cooling Pad"),
        "Printers":     ("HP LaserJet Pro", "Canon Pixma G3010", "Epson L3252"),
    },
}

# ── Helper: random date ───────────────────────────────────────
def random_date(start: datetime, end: datetime) -> datetime:
    delta = (end - start).days
    return start + timedelta(days=int(np.random.randint(0, delta)))

# ── Build records ─────────────────────────────────────────────
records = []

for i in range(N_ROWS):
    order_date  = random_date(START_DATE, END_DATE)
    ship_date   = order_date + timedelta(days=int(np.random.randint(2, 10)))

    region      = np.random.choice(REGIONS, p=[0.30, 0.25, 0.25, 0.20])   # weighted
    category    = np.random.choice(list(CATEGORIES.keys()), p=[0.35, 0.40, 0.25])
    sub_cat     = np.random.choice(list(CATEGORIES[category].keys()))
    product     = np.random.choice(CATEGORIES[category][sub_cat])

    quantity    = int(np.random.randint(1, 10))

    # Base unit price depends on category
    if category == "Technology":
        base_price = np.random.uniform(800, 80000)
    elif category == "Furniture":
        base_price = np.random.uniform(500, 25000)
    else:
        base_price = np.random.uniform(50, 2000)

    sales       = round(base_price * quantity, 2)

    # Discount: Technology gets higher discounts, Office Supplies lower
    discount_bands = {
        "Technology":       np.random.choice([0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30],
                                              p=[0.20, 0.15, 0.20, 0.20, 0.10, 0.10, 0.05]),
        "Furniture":        np.random.choice([0, 0.05, 0.10, 0.15, 0.20, 0.30],
                                              p=[0.25, 0.20, 0.25, 0.15, 0.10, 0.05]),
        "Office Supplies":  np.random.choice([0, 0.05, 0.10, 0.20],
                                              p=[0.40, 0.30, 0.20, 0.10]),
    }
    discount = discount_bands[category]

    # Profit: high discount => lower or negative profit
    profit_margin_base = np.random.uniform(0.08, 0.35)
    discount_penalty   = discount * np.random.uniform(1.5, 3.0)   # discounts hurt margin
    profit_margin      = profit_margin_base - discount_penalty
    profit             = round(sales * profit_margin, 2)

    # Customer segment
    segment = np.random.choice(["Consumer", "Corporate", "Home Office"],
                                p=[0.52, 0.30, 0.18])

    records.append({
        "Order_ID":       f"ORD-{2022 + i // 1000}-{str(i+1).zfill(5)}",
        "Order_Date":     order_date.strftime("%Y-%m-%d"),
        "Ship_Date":      ship_date.strftime("%Y-%m-%d"),
        "Region":         region,
        "Segment":        segment,
        "Category":       category,
        "Sub_Category":   sub_cat,
        "Product_Name":   product,
        "Sales":          sales,
        "Quantity":       quantity,
        "Discount":       discount,
        "Profit":         profit,
    })

df = pd.DataFrame(records)

# ── Inject ~3% missing values (realistic) ────────────────────
for col in ["Discount", "Profit"]:
    mask = np.random.choice([True, False], size=N_ROWS, p=[0.03, 0.97])
    df.loc[mask, col] = np.nan

# ── Inject ~1% duplicate rows ─────────────────────────────────
dup_idx = np.random.choice(df.index, size=20, replace=False)
df = pd.concat([df, df.loc[dup_idx]], ignore_index=True)

# ── Save ──────────────────────────────────────────────────────
out_path = os.path.join(os.path.dirname(__file__), "..", "data", "retail_data.csv")
df.to_csv(out_path, index=False)

print(f"✅ Dataset saved → {os.path.abspath(out_path)}")
print(f"   Shape  : {df.shape}")
print(f"   Period : {df['Order_Date'].min()}  →  {df['Order_Date'].max()}")
print(f"   Columns: {list(df.columns)}")
