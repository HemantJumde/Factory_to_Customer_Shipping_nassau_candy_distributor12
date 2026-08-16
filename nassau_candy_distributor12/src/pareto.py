"""
Pareto (80/20) analysis module for Nassau Candy Distributor.
Calculates cumulative revenue and profit contribution, identifying concentration risks.
"""

from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np


def compute_pareto_analysis(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
    """
    Computes Pareto cumulative distributions for both Revenue and Gross Profit.
    
    Returns:
        Tuple: (Revenue Pareto DataFrame, Profit Pareto DataFrame, Concentration Metrics Dict)
    """
    if df.empty:
        empty_df = pd.DataFrame()
        return empty_df, empty_df, {}
        
    prod = df.groupby(["Division", "Product ID", "Product Name"]).agg(
        Revenue=("Sales", "sum"),
        Gross_Profit=("Gross Profit", "sum"),
        Units=("Units", "sum")
    ).reset_index()
    
    total_rev = prod["Revenue"].sum()
    total_prof = prod["Gross_Profit"].sum()
    total_prods = len(prod)
    
    # 1. Revenue Pareto
    rev_df = prod.sort_values(by="Revenue", ascending=False).reset_index(drop=True)
    rev_df["Revenue %"] = (rev_df["Revenue"] / total_rev * 100.0) if total_rev > 0 else 0.0
    rev_df["Cumulative Revenue %"] = rev_df["Revenue %"].cumsum()
    rev_df["Product Rank"] = np.arange(1, total_prods + 1)
    rev_df["Product Share %"] = (rev_df["Product Rank"] / total_prods * 100.0)
    
    def pareto_category(cum_pct):
        if cum_pct <= 80.0:
            return "Class A (Top 80%)"
        elif cum_pct <= 95.0:
            return "Class B (Next 15%)"
        else:
            return "Class C (Tail 5%)"
            
    rev_df["Pareto Class"] = rev_df["Cumulative Revenue %"].apply(pareto_category)
    
    # 2. Profit Pareto
    prof_df = prod.sort_values(by="Gross_Profit", ascending=False).reset_index(drop=True)
    prof_df["Profit %"] = (prof_df["Gross_Profit"] / total_prof * 100.0) if total_prof > 0 else 0.0
    prof_df["Cumulative Profit %"] = prof_df["Profit %"].cumsum()
    prof_df["Product Rank"] = np.arange(1, total_prods + 1)
    prof_df["Product Share %"] = (prof_df["Product Rank"] / total_prods * 100.0)
    prof_df["Pareto Class"] = prof_df["Cumulative Profit %"].apply(pareto_category)
    
    # 3. Threshold counts (50%, 80%, 90% cumulative)
    # Using shift to find the first product that crosses the threshold
    def get_threshold_count(df_sorted, cum_col, target_pct=80.0):
        # Number of products needed to reach or exceed target_pct cumulative share
        shifted_cum = df_sorted[cum_col].shift(1, fill_value=0.0)
        count = int((shifted_cum < target_pct).sum())
        return max(1, min(count, total_prods))
        
    rev_50 = get_threshold_count(rev_df, "Cumulative Revenue %", 50.0)
    rev_80 = get_threshold_count(rev_df, "Cumulative Revenue %", 80.0)
    rev_90 = get_threshold_count(rev_df, "Cumulative Revenue %", 90.0)
    
    prof_50 = get_threshold_count(prof_df, "Cumulative Profit %", 50.0)
    prof_80 = get_threshold_count(prof_df, "Cumulative Profit %", 80.0)
    prof_90 = get_threshold_count(prof_df, "Cumulative Profit %", 90.0)
    
    top_1_profit_share = float(prof_df["Profit %"].iloc[0]) if total_prods > 0 else 0.0
    top_3_profit_share = float(prof_df["Profit %"].iloc[:3].sum()) if total_prods >= 3 else 100.0
    top_5_profit_share = float(prof_df["Profit %"].iloc[:5].sum()) if total_prods >= 5 else 100.0
    
    # State-level concentration metrics
    state_df, state_metrics = compute_state_concentration(df)
    
    summary_metrics = {
        "total_products": total_prods,
        "revenue_50_pct_count": rev_50,
        "revenue_80_pct_count": rev_80,
        "revenue_90_pct_count": rev_90,
        "profit_50_pct_count": prof_50,
        "profit_80_pct_count": prof_80,
        "profit_90_pct_count": prof_90,
        "top_1_profit_share_pct": top_1_profit_share,
        "top_3_profit_share_pct": top_3_profit_share,
        "top_5_profit_share_pct": top_5_profit_share,
        "revenue_50_pct_product_share": (rev_50 / total_prods * 100.0),
        "profit_50_pct_product_share": (prof_50 / total_prods * 100.0),
        "profit_80_pct_product_share": (prof_80 / total_prods * 100.0),
        "concentration_risk_level": "HIGH (Heavy reliance on top 5 products)" if top_5_profit_share > 95.0 else "MODERATE",
        "state_dependency_risk": state_metrics
    }
    
    return rev_df, prof_df, summary_metrics


def compute_state_concentration(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Aggregates sales by State/Province and flags if any single state exceeds 30% of total revenue.
    """
    if df.empty:
        return pd.DataFrame(), {}
        
    total_revenue = df["Sales"].sum()
    state_df = df.groupby("State/Province").agg(
        Sales=("Sales", "sum"),
        Profit=("Gross Profit", "sum"),
        Orders=("Order ID", "count")
    ).reset_index()
    
    state_df["Revenue Share %"] = (state_df["Sales"] / total_revenue * 100.0) if total_revenue > 0 else 0.0
    state_df = state_df.sort_values(by="Sales", ascending=False).reset_index(drop=True)
    
    # Flag states with > 30% of total revenue
    risk_states = state_df[state_df["Revenue Share %"] > 30.0]
    has_risk = len(risk_states) > 0
    
    state_metrics = {
        "has_risk": has_risk,
        "risk_states": risk_states["State/Province"].tolist(),
        "risk_states_shares": risk_states["Revenue Share %"].tolist()
    }
    
    return state_df, state_metrics

