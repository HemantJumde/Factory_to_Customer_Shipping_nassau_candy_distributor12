"""
Division performance analysis module for Nassau Candy Distributor.
Evaluates revenue, cost, profit, margins, product count, and division strength rankings.
"""

import pandas as pd
import numpy as np


def analyze_divisions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes comprehensive aggregated metrics across all divisions.
    
    Step 4:
    - Aggregate Sales, Gross Profit, Units by Division.
    - Compute average (weighted) Gross Margin % per division.
    - Compare each division's revenue share vs. profit share — flag any 
      division where profit share is meaningfully below revenue share.
    - Rank divisions by financial efficiency.
    """
    if df.empty:
        return pd.DataFrame()
        
    total_rev = df["Sales"].sum()
    total_prof = df["Gross Profit"].sum()
    
    div_summary = df.groupby("Division").agg(
        Revenue=("Sales", "sum"),
        Cost=("Cost", "sum"),
        Gross_Profit=("Gross Profit", "sum"),
        Units=("Units", "sum"),
        Order_Count=("Order ID", "count"),
        Product_Count=("Product ID", "nunique")
    ).reset_index()
    
    div_summary["Gross Margin %"] = np.where(
        div_summary["Revenue"] > 0,
        (div_summary["Gross_Profit"] / div_summary["Revenue"]) * 100.0,
        0.0
    )
    div_summary["Profit per Unit"] = np.where(
        div_summary["Units"] > 0,
        div_summary["Gross_Profit"] / div_summary["Units"],
        0.0
    )
    div_summary["Cost Ratio %"] = np.where(
        div_summary["Revenue"] > 0,
        (div_summary["Cost"] / div_summary["Revenue"]) * 100.0,
        0.0
    )
    div_summary["Revenue Contribution %"] = (div_summary["Revenue"] / total_rev * 100.0) if total_rev > 0 else 0.0
    div_summary["Profit Contribution %"] = (div_summary["Gross_Profit"] / total_prof * 100.0) if total_prof > 0 else 0.0
    
    # Revenue vs Profit Share Comparison (Imbalance Check)
    div_summary["Profit Share vs Revenue Share Mismatch %"] = div_summary["Profit Contribution %"] - div_summary["Revenue Contribution %"]
    # Flag if profit share is meaningfully below revenue share (threshold: <= -1.0%)
    div_summary["Imbalance Flag"] = div_summary["Profit Share vs Revenue Share Mismatch %"] <= -1.0
    
    # Rank divisions by financial efficiency (weighted Gross Margin % descending)
    div_summary["Financial Efficiency Rank"] = div_summary["Gross Margin %"].rank(ascending=False, method="min").astype(int)
    
    # Division Strength Index (composite rank of Margin %, Profit Contribution %, Profit per Unit)
    div_summary["Margin Rank"] = div_summary["Gross Margin %"].rank(ascending=False, method="min").astype(int)
    div_summary["Profit Rank"] = div_summary["Gross_Profit"].rank(ascending=False, method="min").astype(int)
    div_summary["PPU Rank"] = div_summary["Profit per Unit"].rank(ascending=False, method="min").astype(int)
    
    div_summary["Composite Rank Score"] = div_summary["Margin Rank"] + div_summary["Profit Rank"] + div_summary["PPU Rank"]
    
    def classify_division(row):
        if row["Composite Rank Score"] <= 4:
            return "Strongest (Market Leader)"
        elif row["Composite Rank Score"] <= 7:
            return "Moderate (Stable Performer)"
        else:
            return "Weakest (Underperforming)"
            
    div_summary["Division Classification"] = div_summary.apply(classify_division, axis=1)
    
    return div_summary.sort_values(by="Financial Efficiency Rank").reset_index(drop=True)

