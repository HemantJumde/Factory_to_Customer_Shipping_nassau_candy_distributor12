# Product Line Profitability & Margin Performance Analysis for Nassau Candy Distributor

A production-quality Python & Streamlit analytics application designed to analyze product-line economics, gross margins, division benchmarks, Pareto concentration risks, and manufacturing facility performance for Nassau Candy Distributor.

---

## 🚀 Quick Start & Execution

### Prerequisites
- Python 3.10+ installed
- Dependencies listed in `requirements.txt`

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch the Streamlit Dashboard
```bash
streamlit run app.py
```

Access the interactive dashboard in your browser at `http://localhost:8501`.

---

## 📁 Project Architecture

```text
nassau_candy/
├── app.py                      # Main Streamlit dashboard application
├── requirements.txt            # Project dependencies
├── README.md                   # Setup and execution guide
├── data/
│   └── nassau_candy.csv        # Primary dataset (10,194 order records)
├── src/
│   ├── __init__.py
│   ├── data_loader.py          # Cached data loading module
│   ├── cleaning.py             # Data quality audit & validation engine
│   ├── profitability.py        # Executive KPIs, product rankings & 2x2 matrix
│   ├── division_analysis.py    # Division performance & comparative benchmarks
│   ├── pareto.py               # 80/20 Revenue and Profit concentration analysis
│   ├── risk_analysis.py        # Multi-factor transparent margin risk engine
│   ├── factory_analysis.py     # Production facility mapping & geo analytics
│   └── recommendations.py      # Automated strategic recommendation engine
├── dashboard/
│   ├── __init__.py
│   ├── components.py           # Custom CSS theme, KPI cards, sidebar filters & exports
│   ├── page_overview.py        # Executive Overview tab
│   ├── page_product.py         # Product Profitability & 2x2 Matrix tab
│   ├── page_division.py        # Division Performance tab
│   ├── page_cost_margin.py     # Cost & Margin Diagnostics tab
│   ├── page_pareto.py          # Pareto Analysis tab
│   ├── page_factory.py         # Factory Performance & Geo Map tab
│   └── page_recommendations.py # Automated Recommendations & Export tab
├── notebooks/
│   └── exploratory_analysis.py # Python analytical reference script
└── reports/
    ├── eda_research_paper.md    # In-depth EDA & Research Report
    ├── executive_summary.md     # C-suite Executive Summary
    └── business_recommendations.md # Strategic Business Recommendation Plan
```

---

## 🏭 Manufacturing Facility Coordinates & Product Mapping

| Factory Name | Geographic Coordinates | Primary Product Assignments |
| :--- | :--- | :--- |
| **Lot's O' Nuts** | `32.881893, -111.768036` (Casa Grande, AZ) | `CHO-NUT-13000` (Wonka Bar - Nutty Crunch Surprise) |
| **Wicked Choccy's** | `32.076176, -81.088371` (Savannah, GA) | Core Chocolate Division (`CHO-FUD`, `CHO-MIL`, `CHO-SCR`, `CHO-TRI`) |
| **Sugar Shack** | `48.119140, -96.181150` (Thief River Falls, MN) | Sugar Division (`SUG-EVE`, `SUG-FUN`, `SUG-HAI`, `SUG-LAF`, `SUG-NER`, `SUG-SWE`) |
| **Secret Factory** | `41.446333, -90.565487` (Moline, IL) | Novelty Product `OTH-FIZ-56000` (Fizzy Lifting Drinks) |
| **The Other Factory** | `35.117500, -89.971107` (Memphis, TN) | Other Division (`OTH-GUM`, `OTH-KAZ`, `OTH-LIC`) |

---

## 📊 Key Findings Summary

1. **Chocolate Division Dominance**: Delivers **$131,705.50** in revenue (92.9% of total) and **$88,821.62** in gross profit at a **67.4% gross margin**.
2. **Top SKU**: `Wonka Bar -Scrumdiddlyumptious` (`CHO-SCR-58000`) is the highest gross profit generator ($19,357.50 profit, 69.4% margin).
3. **Pareto Concentration**: Just **5 products** (all in Chocolate) generate **95.1% of total distributor profit**, indicating significant product concentration reliance.
4. **Other & Sugar Drag**: Sugar and Other divisions contribute less than 2.5% of total gross profit, suffering from low order volume and compressed profit per unit.
