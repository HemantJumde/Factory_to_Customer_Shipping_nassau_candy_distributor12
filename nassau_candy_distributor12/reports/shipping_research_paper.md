# Empirical Research Paper: Factory-to-Customer Shipping Route Efficiency Analysis for Nassau Candy Distributor

**Author:** Lead Logistics Analytics Consultant  
**Date:** August 15, 2026  
**Dataset Scope:** 10,194 Order Shipments across 5 Manufacturing Facilities, 15 Product SKUs, and 48 US States.

---

## Abstract

This paper presents an empirical route-level efficiency intelligence analysis for Nassau Candy Distributor. Our objective is to evaluate shipment transit durations (Shipping Lead Time = Ship Date - Order Date) across factory-to-customer routes. 

A profiling of the 10,194 transactions reveals that Nassau Candy's average shipment lead time is **1,320.84 days (approx. 3.6 years)**, indicating a massive systemic lag in order-to-delivery processes. Furthermore, we uncover the **"Expedited Shipping Paradox"**: expedited modes like *First Class* (1,338.28 days) and *Same Day* (1,333.44 days) exhibit slower transit times than *Standard Class* (1,314.33 days), revealing a total failure in logistics priority queueing. 

We identify 54 critical congestion bottlenecks and rank the top 10 fastest and bottom 10 slowest shipping routes to guide a national network optimization strategy.

---

## 1. Introduction & Background

Nassau Candy Distributor operates a nationwide confectionery distribution network. Efficient fulfillment is critical to maintaining distributor alliances and minimizing warehousing holding overhead. 

Historically, logistics planning at Nassau Candy has been reactive, lacking route-level analytics. This study establishes a data-driven model to map out route performance, calculate delay frequencies, and define a normalized **Route Efficiency Score** to prioritize supply chain infrastructure investments.

---

## 2. Methodology & Data Engineering

### 2.1 Data Cleaning & Validation Log
We performed a multi-stage data validation audit on the raw `data/nassau_candy.csv` dataset (10,194 records):
- **Date Verification**: Parsed `Order Date` and `Ship Date` columns under a strict `DD-MM-YYYY` mask.
- **Negative & Empty Filters**: Removed transactions with missing dates or where `Ship Date < Order Date`.
- **Geographic Standardization**: Standardized spaces and casing for customer cities, states, and regions.
- **Factory Assignment**: Mapped products to their respective manufacturing nodes based on the updated factory-product matrices.

### 2.2 Feature Engineering & Model Metrics
- **Shipping Lead Time (Days)**: Computed as \(\text{Ship Date} - \text{Order Date}\).
- **Route Definitions**: Established at the State level (\(\text{Factory} \rightarrow \text{Customer State}\)) and Region level (\(\text{Factory} \rightarrow \text{Customer Region}\)).
- **Delay Frequency %**: Defined as the percentage of shipments on a route that exceed the enterprise threshold of **1,300.0 days**.
- **Route Efficiency Score (0-100)**: Calculated by inverting min-max scaled average lead times, where the fastest average route scores 100.0 and the slowest scores 0.0.
  \[
  \text{Score} = 100 \times \left(1 - \frac{\text{Avg Lead Time} - \text{Min Lead Time}}{\text{Max Lead Time} - \text{Min Lead Time}}\right)
  \]

---

## 3. Empirical Findings

### 3.1 Route Leaderboards (State Level)
The dataset comprises **196 active factory-to-state routes**. The fastest and slowest routes are:

#### Top 5 Most Efficient Routes (Fastest)
1. **Secret Factory ➔ Nebraska**: 1 Shipment | Avg Lead Time: **906.00 Days** | Efficiency Score: **100.0/100**
2. **Secret Factory ➔ New Mexico**: 2 Shipments | Avg Lead Time: **906.00 Days** | Efficiency Score: **100.0/100**
3. **The Other Factory ➔ Louisiana**: 1 Shipment | Avg Lead Time: **907.00 Days** | Efficiency Score: **99.9/100**
4. **The Other Factory ➔ Connecticut**: 2 Shipments | Avg Lead Time: **907.50 Days** | Efficiency Score: **99.8/100**
5. **Wicked Choccy's ➔ Maine**: 2 Shipments | Avg Lead Time: **908.00 Days** | Efficiency Score: **99.7/100**

#### Bottom 5 Least Efficient Routes (Slowest)
1. **Sugar Shack ➔ New Jersey**: 1 Shipment | Avg Lead Time: **1,642.00 Days** | Efficiency Score: **0.0/100**
2. **Secret Factory ➔ New Hampshire**: 1 Shipment | Avg Lead Time: **1,641.00 Days** | Efficiency Score: **0.1/100**
3. **Sugar Shack ➔ Connecticut**: 1 Shipment | Avg Lead Time: **1,641.00 Days** | Efficiency Score: **0.1/100**
4. **Wicked Choccy's ➔ West Virginia**: 2 Shipments | Avg Lead Time: **1,639.00 Days** | Efficiency Score: **0.4/100**
5. **Lot's O' Nuts ➔ North Dakota**: 5 Shipments | Avg Lead Time: **1,638.20 Days** | Efficiency Score: **0.5/100**

---

### 3.2 The "Expedited Shipping Paradox"
A comparative analysis of transit performance across shipping methods reveals a critical structural bottleneck:

| Ship Mode | Shipment Count | Mean Lead Time | Std Dev | Max Lead Time | Delay Rate (>1300d) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Standard Class** | 6,120 | **1,314.33 Days** | 262.40 Days | 1,642 Days | 50.9% |
| **Second Class** | 1,979 | **1,323.85 Days** | 261.81 Days | 1,640 Days | 52.8% |
| **Same Day** | 547 | **1,333.44 Days** | 253.81 Days | 1,636 Days | 55.4% |
| **First Class** | 1,548 | **1,338.28 Days** | 265.63 Days | 1,638 Days | 56.3% |

**Key Diagnostic**: Standard Class shipments are, on average, **24 days faster** than First Class and **19 days faster** than Same Day. This indicates that expedited shipping orders are not receiving priority queue treatment at the warehousing level, creating a negative correlation between service cost and actual performance.

---

### 3.3 Geographic Bottleneck hotspots
We identified **54 routes as high-volume congestion bottlenecks** (defined as routes with above-median volume and above-median lead times). The top congestion nodes are:
- **Wicked Choccy's ➔ New Mexico**: 17 Shipments | Avg LT: **1,488.88 Days** | Delay %: **64.7%**
- **Lot's O' Nuts ➔ Iowa**: 16 Shipments | Avg LT: **1,479.00 Days** | Delay %: **56.2%**
- **Lot's O' Nuts ➔ South Dakota**: 9 Shipments | Avg LT: **1,477.22 Days** | Delay %: **77.8%**
- **Secret Factory ➔ Washington**: 11 Shipments | Avg LT: **1,472.36 Days** | Delay %: **54.5%**
- **Lot's O' Nuts ➔ New Mexico**: 18 Shipments | Avg LT: **1,456.94 Days** | Delay %: **61.1%**

---

## 4. Strategic Recommendations

1. **Resolve the Priority Queue Failure**: Conduct a warehouse operations audit to enforce FIFO (First In, First Out) for expedited methods (Same Day, First Class). Establish automated alerts in the ERP to highlight express orders on the packing line.
2. **Consolidate Low-Volume / Slow Routes**: Slow routes like `Sugar Shack ➔ New Jersey` (1,642 days) and `Sugar Shack ➔ Connecticut` (1,641 days) should be transitioned to regional hubs or third-party logistics (3PL) partners to reduce transit drag.
3. **Establish Regional Transit Thresholds**: Implement geographic service-level agreements (SLAs), adjusting delivery expectations by distance rather than applying a flat threshold across the country.

---

## Appendix

### Data Cleaning Log
| Metric | Count / Value |
| :--- | :---: |
| Initial Rows In | 10,194 |
| Rows Removed (Missing Dates) | 0 |
| Rows Removed (Negative Lead) | 0 |
| Final Rows Out | 10,194 |
| Date Range | 2024-01-02 to 2025-12-31 |

### Ship Mode Breakdown Table
| Ship Mode | Shipments | Avg Lead Time | Std Dev | Max Lead Time |
| :--- | :---: | :---: | :---: | :---: |
| **First Class** | 1,548 | 1,338.28 Days | 265.63 Days | 1,638 Days |
| **Same Day** | 547 | 1,333.44 Days | 253.81 Days | 1,636 Days |
| **Second Class** | 1,979 | 1,323.85 Days | 261.81 Days | 1,640 Days |
| **Standard Class** | 6,120 | 1,314.33 Days | 262.40 Days | 1,642 Days |
