<!-- PROJECT BANNER -->
<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=rect&color=0:1a1a2e,100:0f3460&height=120&text=📈%20Retail%20Sales%20EDA%20%26%20Profitability%20Analysis&fontSize=28&fontColor=e0e0e0&fontAlignY=50" width="100%" />
</div>

<div align="center">

<!-- BADGES -->
![Status](https://img.shields.io/badge/Status-Completed-success?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)

**End-to-end exploratory data analysis using Python to uncover revenue drivers, profit leakage, and the quantified impact of discount strategies on retail profitability.**

[Key Findings](#-key-insights) · [Methodology](#-methodology) · [Business Recommendations](#-business-recommendations)

</div>

---

## 📋 Table of Contents

- [Business Problem](#-business-problem)
- [Objectives](#-objectives)
- [Dataset](#-dataset)
- [Tech Stack](#-tech-stack)
- [Methodology](#-methodology)
- [KPIs Analyzed](#-kpis-analyzed)
- [Visualizations](#-visualizations)
- [Key Insights](#-key-insights)
- [Business Recommendations](#-business-recommendations)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Future Improvements](#-future-improvements)
- [License](#-license)
- [Contact](#-contact)

---

## 🎯 Business Problem

E-commerce and retail platforms routinely offer **blanket discounts** to drive sales volume — but rarely quantify the **profitability threshold** at which margin erosion outpaces volume gains. This creates a hidden profit leak that compounds over time.

This analysis answers the critical business question:

> **"At what discount level do we start losing money, and which product categories are most affected?"**

By combining statistical analysis with business-context visualization, this project transforms raw transaction data into a **data-driven discounting strategy** that protects margins while maintaining competitive pricing.

---

## 🎯 Objectives

- ✅ Perform comprehensive EDA on retail sales data to understand revenue distribution
- ✅ Identify the top revenue drivers by category, segment, and region
- ✅ Quantify profit leakage from excessive discounting
- ✅ Determine the **optimal discount threshold** beyond which margins erode
- ✅ Analyze correlation between discount levels, sales volume, and profitability
- ✅ Deliver actionable pricing recommendations with supporting visualizations

---

## 📊 Dataset

| Property | Detail |
|----------|--------|
| **Source** | Retail Sales Dataset |
| **Records** | *Update with your actual record count* |
| **Features** | *Update with your actual column count* |
| **Granularity** | Transaction-level |

<details>
<summary>📌 Key Columns (click to expand)</summary>

| Column | Type | Description |
|--------|------|-------------|
| `Order_ID` | String | Unique order identifier |
| `Category` | String | Product category |
| `Sub_Category` | String | Product sub-category |
| `Sales` | Float | Transaction revenue |
| `Profit` | Float | Transaction profit |
| `Discount` | Float | Discount applied (0.0–1.0) |
| `Quantity` | Integer | Units ordered |
| `Region` | String | Geographic region |
| `Segment` | String | Customer segment (Consumer/Corporate/Home Office) |
| `Ship_Mode` | String | Shipping method |

*Update columns to match your actual dataset.*

</details>

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Language** | Python 3.11 | Core analysis language |
| **Data Manipulation** | Pandas | Data cleaning, transformation, aggregation |
| **Numerical Computing** | NumPy | Statistical calculations |
| **Visualization** | Matplotlib, Seaborn | Charts, heatmaps, distribution plots |
| **Statistics** | SciPy (optional) | Correlation analysis, hypothesis testing |
| **Environment** | Jupyter Notebook | Interactive analysis workflow |
| **Version Control** | Git, GitHub | Source control |

---

## 📐 Methodology

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Loading   │───▶│  Data Cleaning   │───▶│    EDA &        │───▶│  Statistical    │───▶│  Insights &     │
│   & Inspection   │    │  & Preparation   │    │  Visualization  │    │  Analysis       │    │  Recommendations│
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 1. Data Loading & Inspection
- Loaded dataset using Pandas
- Inspected shape, dtypes, null counts, and basic statistics
- Identified data quality issues

### 2. Data Cleaning & Preparation
- Handled missing values (imputation / removal based on context)
- Standardized data types (dates, categories, numeric)
- Created derived columns (profit margin %, discount buckets, date parts)

### 3. Exploratory Data Analysis
- **Univariate:** Distribution of sales, profit, discount levels
- **Bivariate:** Sales vs. profit, discount vs. profit margin, category vs. revenue
- **Multivariate:** Segment × Category × Discount interaction effects

### 4. Statistical Analysis
- Correlation matrix for all numeric variables
- Discount threshold analysis (breakeven identification)
- Category-level profitability ranking

### 5. Insights & Recommendations
- Synthesized findings into actionable business recommendations
- Quantified dollar impact of proposed changes

---

## 📏 KPIs Analyzed

| KPI | Description |
|-----|-------------|
| **Total Revenue** | Sum of all transaction sales |
| **Total Profit** | Sum of all transaction profits |
| **Profit Margin %** | Profit / Revenue × 100 |
| **Average Discount** | Mean discount across transactions |
| **Discount-Profit Correlation** | Statistical relationship between discount and profit |
| **Revenue by Category** | Category-level revenue contribution |
| **Profit by Segment** | Customer segment profitability |

---

## 📊 Visualizations

> **📸 Add your key EDA visualizations here.**
>
> **How to export:**
> 1. In your Jupyter notebook, save plots using `plt.savefig('docs/images/plot_name.png', dpi=150, bbox_inches='tight')`
> 2. Uncomment the image tags below

<!-- UNCOMMENT AFTER ADDING VISUALIZATIONS:

<div align="center">
  <img src="docs/images/correlation_heatmap.png" alt="Correlation Heatmap" width="70%" />
  <br/>
  <em>Correlation Matrix — Relationships Between Sales, Profit, Discount, and Quantity</em>
</div>

<br/>

<div align="center">
  <img src="docs/images/discount_vs_profit.png" alt="Discount vs Profit" width="70%" />
  <br/>
  <em>Discount Impact — Profit Margin Erosion Beyond 30% Discount Threshold</em>
</div>

<br/>

<div align="center">
  <img src="docs/images/category_revenue.png" alt="Category Revenue" width="70%" />
  <br/>
  <em>Category Analysis — Revenue and Profit Contribution by Product Category</em>
</div>

<br/>

<div align="center">
  <img src="docs/images/segment_profitability.png" alt="Segment Analysis" width="70%" />
  <br/>
  <em>Customer Segments — Profitability Comparison Across Consumer, Corporate, and Home Office</em>
</div>

-->

**📸 Visualizations coming soon** — Run the Jupyter notebook to generate all analysis charts.

---

## 💡 Key Insights

### 1. The 30% Discount Cliff
Discounts above **30%** consistently erode profit margins **without a proportional lift in sales volume**. This represents a clear breakeven threshold that pricing teams should enforce.

### 2. Revenue Concentration Risk
A small number of sub-categories generate the majority of revenue, while several sub-categories operate at a net loss due to aggressive discounting.

### 3. Segment-Level Profitability Differences
The Corporate segment shows higher average order values but also receives deeper discounts, resulting in compressed margins compared to the Consumer segment.

### 4. Profit Leakage Hotspots
Specific category-region combinations show negative profit margins — these represent immediate intervention opportunities where either pricing or discounting policies need adjustment.

> **Note:** Update these with specific numbers from your actual analysis.

---

## 📋 Business Recommendations

| # | Recommendation | Expected Impact | Priority |
|---|---------------|----------------|----------|
| 1 | **Cap discounts at 30%** across all categories | Eliminate below-breakeven promotions | 🔴 High |
| 2 | **Investigate loss-making sub-categories** | Identify pricing/cost issues | 🔴 High |
| 3 | **Restructure Corporate segment pricing** | Improve margins without volume loss | 🟡 Medium |
| 4 | **Implement category-specific discount tiers** | Optimize per-category profitability | 🟡 Medium |
| 5 | **Build automated margin monitoring** | Early warning for profit erosion | 🟢 Low |

---

## 📁 Project Structure

```
retail-sales-eda-profitability-analysis/
│
├── 📂 data/
│   └── retail_sales_data.csv          # Raw sales dataset
├── 📂 docs/
│   └── images/                        # EDA visualizations & charts
├── 📂 notebooks/
│   └── retail_eda_analysis.ipynb      # Main analysis notebook
├── requirements.txt                   # Python dependencies
├── LICENSE                            # MIT License
└── README.md                          # This file
```

> **Note:** Move all files from the nested `Retail-Sales-EDA-Python/` subfolder to the repository root.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Jupyter Notebook or JupyterLab

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/anant-saini2006/retail-sales-eda-profitability-analysis.git
cd retail-sales-eda-profitability-analysis

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate          # macOS/Linux
# venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch Jupyter Notebook
jupyter notebook notebooks/retail_eda_analysis.ipynb
```

### Requirements

```
pandas>=2.0
numpy>=1.24
matplotlib>=3.7
seaborn>=0.12
scipy>=1.10
jupyter>=1.0
```

---

## 🔮 Future Improvements

- [ ] Build a Streamlit dashboard for interactive exploration
- [ ] Add customer-level RFM segmentation
- [ ] Implement time-series decomposition for trend analysis
- [ ] Build a discount optimization model using linear programming
- [ ] Create automated PDF report generation
- [ ] Add hypothesis testing (A/B test framework for discount experiments)

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 📬 Contact

**Anant Saini** — Data Analyst · Final-Year B.Tech IT

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://linkedin.com/in/YOUR-LINKEDIN)
[![Email](https://img.shields.io/badge/Email-EA4335?style=flat-square&logo=gmail&logoColor=white)](mailto:duanantsaini2006@gmail.com)
[![Portfolio](https://img.shields.io/badge/Portfolio-000?style=flat-square&logo=vercel&logoColor=white)](https://YOUR-PORTFOLIO-URL)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/anant-saini2006)

---

<div align="center">

⭐ If you found this project useful, please consider giving it a star!

</div>
