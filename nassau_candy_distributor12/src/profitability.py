"""
Profitability and product performance module for Nassau Candy Distributor.
Computes KPIs, product rankings, 2x2 profitability matrix, and volatility metrics.
"""

from typing import Dict, Any
import pandas as pd
import numpy as np


def calculate_overall_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes top-level executive KPIs across the dataset.
    """
    if df.empty:
        return {
            "total_revenue": 0.0,
            "total_cost": 0.0,
            "total_gross_profit": 0.0,
            "gross_margin_pct": 0.0,
            "total_units": 0,
            "profit_per_unit": 0.0,
            "cost_ratio_pct": 0.0,
            "total_orders": 0,
            "avg_order_value": 0.0,
            "margin_volatility": 0.0
        }
        
    revenue = float(df["Sales"].sum())
    cost = float(df["Cost"].sum())
    gross_profit = float(df["Gross Profit"].sum())
    units = int(df["Units"].sum())
    orders = int(df["Order ID"].nunique())
    
    margin_pct = (gross_profit / revenue * 100.0) if revenue > 0 else 0.0
    profit_per_unit = (gross_profit / units) if units > 0 else 0.0
    cost_ratio_pct = (cost / revenue * 100.0) if revenue > 0 else 0.0
    avg_order_value = (revenue / orders) if orders > 0 else 0.0
    
    # Calculate order-level margin volatility (std dev of margin %)
    order_margins = (df["Gross Profit"] / df["Sales"] * 100.0).dropna()
    margin_volatility = float(order_margins.std()) if len(order_margins) > 1 else 0.0
    
    return {
        "total_revenue": revenue,
        "total_cost": cost,
        "total_gross_profit": gross_profit,
        "gross_margin_pct": margin_pct,
        "total_units": units,
        "profit_per_unit": profit_per_unit,
        "cost_ratio_pct": cost_ratio_pct,
        "total_orders": orders,
        "avg_order_value": avg_order_value,
        "margin_volatility": margin_volatility
    }


def analyze_product_profitability(df: pd.DataFrame, margin_threshold: float = 20.0) -> pd.DataFrame:
    """
    Aggregates product-level performance metrics, rankings, contribution %, segmentation, and margin checks.
    
    Step 2 KPIs:
    - Gross Margin % = Gross Profit ÷ Sales * 100
    - Profit per Unit = Gross Profit ÷ Units
    - Revenue Contribution % = Product Sales ÷ Total Sales * 100
    - Profit Contribution % = Product Gross Profit ÷ Total Gross Profit * 100
    Leaderboard sorted by Gross Profit descending.
    
    Step 3 Product Segmentation:
    - High-profit / high-margin products (Top Performer)
    - High-sales / low-margin products (Margin Risk)
    - Low-sales / low-profit products (Low Priority / Cut)
    - Low-sales / high-margin products (Niche)
    - Configurable margin threshold flag (default 20%).
    """
    if df.empty:
        return pd.DataFrame()
        
    total_rev = df["Sales"].sum()
    total_prof = df["Gross Profit"].sum()
    
    grouped = df.groupby(["Division", "Product ID", "Product Name"]).agg(
        Sales=("Sales", "sum"),
        Cost=("Cost", "sum"),
        Gross_Profit=("Gross Profit", "sum"),
        Units=("Units", "sum"),
        Order_Count=("Order ID", "count")
    ).reset_index()
    
    grouped["Gross Margin %"] = np.where(
        grouped["Sales"] > 0,
        (grouped["Gross_Profit"] / grouped["Sales"]) * 100.0,
        0.0
    )
    grouped["Profit per Unit"] = np.where(
        grouped["Units"] > 0,
        grouped["Gross_Profit"] / grouped["Units"],
        0.0
    )
    grouped["Cost Ratio %"] = np.where(
        grouped["Sales"] > 0,
        (grouped["Cost"] / grouped["Sales"]) * 100.0,
        0.0
    )
    grouped["Revenue Contribution %"] = (grouped["Sales"] / total_rev * 100.0) if total_rev > 0 else 0.0
    grouped["Profit Contribution %"] = (grouped["Gross_Profit"] / total_prof * 100.0) if total_prof > 0 else 0.0
    
    # Calculate order-level margin volatility per product
    product_volatility = df.groupby("Product ID").apply(
        lambda g: (g["Gross Profit"] / g["Sales"] * 100.0).std() if len(g) > 1 else 0.0
    ).reset_index(name="Margin Volatility")
    
    grouped = grouped.merge(product_volatility, on="Product ID", how="left").fillna(0.0)
    
    # Segmentation Boundaries
    median_sales = grouped["Sales"].median()
    median_margin = grouped["Gross Margin %"].median()
    median_profit = grouped["Gross_Profit"].median()
    
    def segment_product(row):
        sales = row["Sales"]
        margin = row["Gross Margin %"]
        profit = row["Gross_Profit"]
        
        # High-profit / high-margin products (top performers)
        if sales >= median_sales and margin >= median_margin:
            return "High-profit / high-margin (Top Performer)"
        # High-sales / low-margin products (margin risk despite volume)
        elif sales >= median_sales and margin < median_margin:
            return "High-sales / low-margin (Margin Risk)"
        # Low-sales / low-profit products (low priority / possible cut)
        elif sales < median_sales and profit < median_profit:
            return "Low-sales / low-profit (Low Priority / Cut)"
        # Low-sales / high-margin products (niche)
        else:
            return "Low-sales / high-margin (Niche)"
            
    def assign_action(segment_name):
        if "Top Performer" in segment_name:
            return "Protect & Retain"
        elif "Margin Risk" in segment_name:
            return "Repricing / Cost Review"
        elif "Niche" in segment_name:
            return "Promote & Grow"
        else:
            return "Rationalize / Discontinue Review"
            
    grouped["Segment"] = grouped.apply(segment_product, axis=1)
    grouped["Recommended Action"] = grouped["Segment"].apply(assign_action)
    
    # Step 3 configurable margin threshold flag (default 20.0%)
    grouped["Below Threshold Flag"] = grouped["Gross Margin %"] < margin_threshold
    
    # Keep compatibility with previous matrix categories
    grouped["Matrix Category"] = grouped["Segment"].replace({
        "High-profit / high-margin (Top Performer)": "1. High Sales + High Margin (Star/Protect)",
        "High-sales / low-margin (Margin Risk)": "2. High Sales + Low Margin (Volume Driver/Optimize)",
        "Low-sales / high-margin (Niche)": "3. Low Sales + High Margin (Niche/Grow)",
        "Low-sales / low-profit (Low Priority / Cut)": "4. Low Sales + Low Margin (Underperformer/Review)"
    })
    
    # Rankings
    grouped["Sales Rank"] = grouped["Sales"].rank(ascending=False, method="min").astype(int)
    grouped["Profit Rank"] = grouped["Gross_Profit"].rank(ascending=False, method="min").astype(int)
    grouped["Margin Rank"] = grouped["Gross Margin %"].rank(ascending=False, method="min").astype(int)
    grouped["Profit/Unit Rank"] = grouped["Profit per Unit"].rank(ascending=False, method="min").astype(int)
    
    return grouped.sort_values(by="Gross_Profit", ascending=False).reset_index(drop=True)

