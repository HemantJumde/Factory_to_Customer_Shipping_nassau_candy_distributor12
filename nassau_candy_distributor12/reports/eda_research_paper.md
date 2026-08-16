# Exploratory Data Analysis & Empirical Research Paper: Nassau Candy Distributor Profitability & Margin Performance

**Author:** Antigravity Data Science & Advanced Analytics Team  
**Dataset Analyzed:** `Nassau Candy Distributor.csv` (10,194 Transaction Records)  
**Scope:** Product SKU Economics, Division Performance, Pareto Concentration, Margin Risk Diagnostics, and Factory Mapping.

---

## Abstract

This research paper provides an empirical exploratory data analysis (EDA) of product line profitability and gross margin performance for Nassau Candy Distributor. Utilizing 10,194 order transactions spanning 2024 through 2025, we evaluate SKU-level economics, manufacturing cost ratios, Pareto concentration risks, and facility geographic performance. Our findings reveal extreme profit concentration: 5 core Chocolate products generate **95.06% of total gross profit** ($88,824.62 out of $93,442.80), while the Other and Sugar divisions combined contribute less than 5% of net profit. Furthermore, `Kazookles` is identified as a Critical Risk SKU with a **92.31% manufacturing cost ratio** (7.69% gross margin).

---

## 1. Introduction & Methodology

Nassau Candy Distributor operates as a regional wholesale confectionery distributor across 4 major US geographic regions (Pacific, Atlantic, Interior, Gulf) servicing 59 states/provinces and 542 cities. Products are supplied by 5 regional manufacturing facilities.

### 1.1 Data Audit & Integrity
The raw dataset was subjected to automated data cleaning and quality validation:
- **Total Records Analyzed:** 10,194 orders
- **Missing Values / Nulls:** 0 across all 18 fields (100% data completeness)
- **Duplicate Rows:** 0 duplicates detected
- **Formula Integrity:** Verified $Gross Profit = Sales - Cost$ across 100% of records ($0.00$ discrepancy).

---

## 2. Macro-Level Financial KPIs

| Financial Metric | Empirical Calculated Value |
| :--- | :--- |
| **Total Gross Revenue** | **$141,783.63** |
| **Total Manufacturing Cost** | **$48,340.83** |
| **Total Gross Profit** | **$93,442.80** |
| **Overall Gross Margin %** | **65.91%** |
| **Total Units Distributed** | **38,654 units** |
| **Average Profit per Unit** | **$2.42 / unit** |
| **Total Order Count** | **8,549 orders** |
| **Average Order Value (AOV)** | **$16.58 / order** |
| **Overall Cost Ratio %** | **34.09%** |

---

## 3. Division Performance & Portfolio Dynamics

The distributor operates 3 product divisions: **Chocolate**, **Other**, and **Sugar**.

| Division | Active SKUs | Revenue ($) | Cost ($) | Gross Profit ($) | Gross Margin % | Profit Contribution % | Classification |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Chocolate** | 5 | $131,692.90 | $42,868.28 | $88,824.62 | **67.45%** | **95.06%** | Market Leader (Strongest) |
| **Other** | 3 | $9,663.25 | $5,329.80 | $4,333.45 | **44.84%** | **4.64%** | Volume Performer (Moderate) |
| **Sugar** | 7 | $427.48 | $142.75 | $284.73 | **66.61%** | **0.30%** | Niche / Tail (Weakest) |

### Key Division Insights:
1. **Chocolate Division Dominance**: The Chocolate division is the financial backbone of the enterprise, driving 92.88% of total revenue and 95.06% of total gross profit.
2. **Other Division Margin Compression**: The Other division exhibits compressed margins (44.84%) driven primarily by `Kazookles` (7.69% margin).
3. **Sugar Division Sub-Scale Volume**: Despite a healthy 66.61% gross margin, the Sugar division generates only $427.48 total revenue across 7 SKUs, representing extreme under-utilization of distribution capacity.

---

## 4. Product-Level SKU Economics & Matrix Analysis

Using median sales ($597.50) and median margin (65.33%) as boundary lines, products are classified into a 2x2 Profitability Matrix:

```text
                     High Sales (>= $597.50)         Low Sales (< $597.50)
                 +-------------------------------+-------------------------------+
High Margin      | 1. STAR / PROTECT             | 3. NICHE / GROW               |
(>= 65.33%)      | • Scrumdiddlyumptious (69.4%) | • Everlasting Gobstopper (80%)|
                 | • Nutty Crunch (71.3%)        | • Hair Toffee (77.8%)         |
                 | • Fudge Mallows (66.7%)       | • Laffy Taffy (62.3%)         |
                 | • Triple Dazzle (65.3%)       |                               |
                 +-------------------------------+-------------------------------+
Low Margin       | 2. VOLUME DRIVER / OPTIMIZE   | 4. UNDERPERFORMER / REVIEW    |
(< 65.33%)       | • Milk Chocolate (64.9%)      | • Fizzy Lifting Drinks (60.0%)|
                 | • Lickable Wallpaper (50.0%)  | • SweeTARTS (46.7%)           |
                 | • Wonka Gum (52.0%)           | • Nerds (46.7%)               |
                 | • Kazookles (7.69%)           | • Fun Dip (40.0%)             |
                 +-------------------------------+-------------------------------+
```

### Complete SKU Leaderboard:

| Product Name | Division | Revenue ($) | Gross Profit ($) | Gross Margin % | Cost Ratio % | Matrix Category | Risk Level |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **Wonka Bar - Scrumdiddlyumptious** | Chocolate | $27,874.80 | **$19,357.50** | 69.44% | 30.56% | Star / Protect | Low Risk |
| **Wonka Bar - Triple Dazzle Caramel**| Chocolate | $28,485.00 | **$18,610.20** | 65.33% | 34.67% | Star / Protect | Low Risk |
| **Wonka Bar - Milk Chocolate** | Chocolate | $26,867.75 | **$17,443.37** | 64.92% | 35.08% | Volume Driver | Low Risk |
| **Wonka Bar - Nutty Crunch** | Chocolate | $23,574.95 | **$16,819.95** | 71.35% | 28.65% | Star / Protect | Low Risk |
| **Wonka Bar - Fudge Mallows** | Chocolate | $24,890.40 | **$16,593.60** | 66.67% | 33.33% | Star / Protect | Low Risk |
| **Lickable Wallpaper** | Other | $7,860.00 | $3,930.00 | 50.00% | 50.00% | Volume Driver | Medium Risk |
| **Wonka Gum** | Other | $597.50 | $310.70 | 52.00% | 48.00% | Volume Driver | High Risk |
| **Everlasting Gobstopper** | Sugar | $130.00 | $104.00 | 80.00% | 20.00% | Niche / Grow | Low Risk |
| **Kazookles** | Other | $1,205.75 | **$92.75** | **7.69%** | **92.31%** | Volume Driver | **Critical Risk** |
| **Hair Toffee** | Sugar | $76.50 | $59.50 | 77.78% | 22.22% | Niche / Grow | Low Risk |
| **Fizzy Lifting Drinks** | Other/Sugar | $78.75 | $47.25 | 60.00% | 40.00% | Underperformer | Low Risk |
| **Laffy Taffy** | Sugar | $53.73 | $33.48 | 62.31% | 37.69% | Niche / Grow | Low Risk |
| **SweeTARTS** | Sugar | $61.50 | $28.70 | 46.67% | 53.33% | Underperformer | Medium Risk |
| **Nerds** | Sugar | $15.00 | $7.00 | 46.67% | 53.33% | Underperformer | Medium Risk |
| **Fun Dip** | Sugar | $12.00 | $4.80 | 40.00% | 60.00% | Underperformer | Medium Risk |

---

## 5. Pareto (80/20) Concentration Analysis

Cumulative concentration analysis reveals extreme portfolio dependency:
- **50% Profit Concentration:** Achieved by just **3 products** (Scrumdiddlyumptious, Triple Dazzle, Milk Chocolate).
- **80% Profit Concentration:** Achieved by **5 products** (the 5 Chocolate Wonka Bars).
- **95.06% Profit Concentration:** Total Chocolate division contribution.
- **Tail Products (10 SKUs):** The remaining 10 non-chocolate products account for two-thirds of the SKU catalog but generate only **4.94% of gross profit**.

---

## 6. Manufacturing Facility Geographic Diagnostics

| Factory Name | Coordinates | Location | Gross Profit ($) | Gross Margin % | High Risk SKUs |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **Wicked Choccy's** | `32.076176, -81.088371` | Savannah, GA | $72,004.67 | 66.61% | 0 |
| **Lot's O' Nuts** | `32.881893, -111.768036` | Casa Grande, AZ | $16,819.95 | 71.35% | 0 |
| **The Other Factory** | `35.117500, -89.971107` | Memphis, TN | $4,333.45 | 44.84% | 2 (`Kazookles`, `Wonka Gum`) |
| **Sugar Shack** | `48.119140, -96.181150` | Thief River Falls, MN | $237.48 | 68.10% | 3 (`SweeTARTS`, `Nerds`, `Fun Dip`) |
| **Secret Factory** | `41.446333, -90.565487` | Moline, IL | $47.25 | 60.00% | 0 |

---

## 7. Conclusions & Academic Recommendations

1. **Supply Chain Protection**: Prioritize raw chocolate supply agreements at Savannah, GA and Casa Grande, AZ facilities.
2. **Kazookles Margin Remediation**: `Kazookles` manufacturing cost ratio (92.31%) requires immediate raw material procurement audit or a mandatory 40% wholesale price adjustment.
3. **Sugar Portfolio Restructuring**: Consolidate low-volume Sugar SKUs (Fun Dip, Nerds, SweeTARTS) into multi-flavor assortment packs to reduce handling overhead and increase order basket size.

---

## Appendix

### Data Cleaning & Validation Log
| Metric | Count |
| :--- | :---: |
| Initial Rows In | 10,194 |
| Rows Removed (Sales <= 0) | 0 |
| Rows Imputed (Units / GP) | 0 |
| Final Rows Out | 10,194 |

### Full Product KPI Table
| Product ID | Product Name | Division | Sales | Cost | Gross Profit | Gross Margin % | Units | Profit per Unit | Revenue Share % | Profit Share % | Segment | Below Threshold Flag |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :---: |
| CHO-SCR-58000 | Wonka Bar - Scrumdiddlyumptious | Chocolate | $27,874.80 | $8,517.30 | $19,357.50 | 69.44% | 7,743 | $2.50 | 19.66% | 20.72% | High-profit / high-margin (Top Performer) | False |
| CHO-TRI-54000 | Wonka Bar - Triple Dazzle Caramel | Chocolate | $28,485.00 | $9,874.80 | $18,610.20 | 65.33% | 7,596 | $2.45 | 20.09% | 19.92% | High-profit / high-margin (Top Performer) | False |
| CHO-MIL-31000 | Wonka Bar - Milk Chocolate | Chocolate | $26,867.75 | $9,424.38 | $17,443.37 | 64.92% | 8,267 | $2.11 | 18.95% | 18.67% | High-profit / high-margin (Top Performer) | False |
| CHO-NUT-13000 | Wonka Bar - Nutty Crunch Surprise | Chocolate | $23,574.95 | $6,755.00 | $16,819.95 | 71.35% | 6,755 | $2.49 | 16.63% | 18.00% | High-profit / high-margin (Top Performer) | False |
| CHO-FUD-51000 | Wonka Bar - Fudge Mallows | Chocolate | $24,890.40 | $8,296.80 | $16,593.60 | 66.67% | 6,914 | $2.40 | 17.56% | 17.76% | High-profit / high-margin (Top Performer) | False |
| OTH-LIC-15000 | Lickable Wallpaper | Other | $7,860.00 | $3,930.00 | $3,930.00 | 50.00% | 393 | $10.00 | 5.54% | 4.21% | High-sales / low-margin (Margin Risk) | False |
| OTH-GUM-21000 | Wonka Gum | Other | $597.50 | $286.80 | $310.70 | 52.00% | 478 | $0.65 | 0.42% | 0.33% | High-sales / low-margin (Margin Risk) | False |
| SUG-EVE-47000 | Everlasting Gobstopper | Sugar | $130.00 | $26.00 | $104.00 | 80.00% | 13 | $8.00 | 0.09% | 0.11% | Low-sales / high-margin (Niche) | False |
| OTH-KAZ-38000 | Kazookles | Other | $1,205.75 | $1,113.00 | $92.75 | 7.69% | 371 | $0.25 | 0.85% | 0.10% | High-sales / low-margin (Margin Risk) | True |
| SUG-HAI-55000 | Hair Toffee | Sugar | $76.50 | $17.00 | $59.50 | 77.78% | 17 | $3.50 | 0.05% | 0.06% | Low-sales / low-profit (Low Priority / Cut) | False |
| OTH-FIZ-56000 | Fizzy Lifting Drinks | Sugar | $78.75 | $31.50 | $47.25 | 60.00% | 21 | $2.25 | 0.06% | 0.05% | Low-sales / low-profit (Low Priority / Cut) | False |
| SUG-LAF-25000 | Laffy Taffy | Sugar | $53.73 | $20.25 | $33.48 | 62.31% | 27 | $1.24 | 0.04% | 0.04% | Low-sales / low-profit (Low Priority / Cut) | False |
| SUG-SWE-91000 | Sweetarts | Sugar | $61.50 | $32.80 | $28.70 | 46.67% | 41 | $0.70 | 0.04% | 0.03% | Low-sales / low-profit (Low Priority / Cut) | False |
| SUG-NER-92000 | Nerds | Sugar | $15.00 | $8.00 | $7.00 | 46.67% | 10 | $0.70 | 0.01% | 0.01% | Low-sales / low-profit (Low Priority / Cut) | False |
| SUG-FUN-75000 | Fun Dip | Sugar | $12.00 | $7.20 | $4.80 | 40.00% | 8 | $0.60 | 0.01% | 0.01% | Low-sales / low-profit (Low Priority / Cut) | False |

