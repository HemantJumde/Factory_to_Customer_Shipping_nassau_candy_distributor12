"""
Margin and product risk scoring engine for Nassau Candy Distributor.
Calculates multi-factor transparent risk scores (0-100), risk tiers, and specific risk drivers.
"""

from typing import List
import pandas as pd
import numpy as np


def compute_product_risk_scores(product_df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes a transparent composite Risk Score (0 - 100) and classifies products into:
    Low, Medium, High, Critical Risk.
    
    Risk Factors Evaluated:
    1. Margin Risk (0-25 pts): Margin below target benchmark
    2. Cost Ratio Risk (0-25 pts): High manufacturing cost ratio
    3. Volume Mismatch Risk (0-25 pts): High sales volume combined with low margin
    4. Profit Contribution Risk (0-15 pts): Low absolute profit generation
    5. Volatility Risk (0-10 pts): High margin fluctuation across orders
    
    Returns:
        pd.DataFrame: Product DataFrame enhanced with Risk Score, Risk Tier, and Reason Drivers.
    """
    if product_df.empty:
        return pd.DataFrame()
        
    df = product_df.copy()
    
    median_sales = df["Sales"].median()
    median_margin = df["Gross Margin %"].median()
    avg_cost_ratio = df["Cost Ratio %"].mean()
    
    def score_single_product(row):
        score = 0.0
        reasons = []
        
        margin = row["Gross Margin %"]
        cost_ratio = row["Cost Ratio %"]
        sales = row["Sales"]
        profit = row["Gross_Profit"]
        volatility = row.get("Margin Volatility", 0.0)
        
        # 1. Margin Risk (0-25 pts)
        if margin < 25.0:
            score += 25.0
            reasons.append(f"Severely low gross margin ({margin:.1f}%)")
        elif margin < 40.0:
            score += 15.0
            reasons.append(f"Sub-target gross margin ({margin:.1f}%)")
        elif margin < median_margin:
            score += 5.0
            reasons.append(f"Margin below median ({margin:.1f}%)")
            
        # 2. Cost Ratio Risk (0-25 pts)
        if cost_ratio > 75.0:
            score += 25.0
            reasons.append(f"Critical cost ratio ({cost_ratio:.1f}% of sales)")
        elif cost_ratio > 60.0:
            score += 15.0
            reasons.append(f"High manufacturing cost ratio ({cost_ratio:.1f}%)")
        elif cost_ratio > avg_cost_ratio:
            score += 5.0
            reasons.append(f"Above-average cost ratio ({cost_ratio:.1f}%)")
            
        # 3. High Sales + Low Margin Mismatch (0-25 pts)
        if sales >= median_sales and margin < median_margin:
            score += 25.0
            reasons.append("High-volume product suffering from compressed margin")
        elif sales < median_sales and margin < 35.0:
            score += 15.0
            reasons.append("Low-volume product with low margin drag")
            
        # 4. Low Absolute Profit (0-15 pts)
        if profit < 50.0:
            score += 15.0
            reasons.append(f"Negligible absolute profit generation (${profit:.2f})")
        elif profit < 500.0:
            score += 10.0
            reasons.append(f"Low profit contribution (${profit:.2f})")
            
        # 5. Margin Volatility Risk (0-10 pts)
        if volatility > 15.0:
            score += 10.0
            reasons.append(f"High order margin volatility (std dev {volatility:.1f}%)")
        elif volatility > 8.0:
            score += 5.0
            reasons.append(f"Moderate margin volatility ({volatility:.1f}%)")
            
        if not reasons:
            reasons.append("Strong margin, healthy cost ratio, and high profit contribution")
            
        score = min(100.0, max(0.0, score))
        
        # Risk Classification
        if score >= 70.0:
            tier = "Critical Risk"
        elif score >= 45.0:
            tier = "High Risk"
        elif score >= 25.0:
            tier = "Medium Risk"
        else:
            tier = "Low Risk"
            
        return pd.Series({
            "Risk Score": score,
            "Risk Level": tier,
            "Risk Reasons": " | ".join(reasons)
        })
        
    risk_metrics = df.apply(score_single_product, axis=1)
    df = pd.concat([df, risk_metrics], axis=1)
    
    # Sort by Risk Score descending
    return df.sort_values(by="Risk Score", ascending=False).reset_index(drop=True)


def get_margin_risk_table(product_df: pd.DataFrame, margin_threshold: float = 20.0) -> pd.DataFrame:
    """
    Step 6 Margin Risk Table:
    Identifies products with sales volume > 0 and gross margin below the threshold.
    Recommends: Repricing, Cost Renegotiation, or Discontinuation Review, with a one-line rationale.
    """
    if product_df.empty:
        return pd.DataFrame(columns=["Product ID", "Product Name", "Division", "Sales", "Gross Margin %", "Cost Ratio %", "Recommended Action", "Rationale"])
        
    # Standardize column naming if necessary (Gross Margin % vs Gross_Margin_Pct)
    margin_col = "Gross Margin %" if "Gross Margin %" in product_df.columns else "Gross Margin %"
    
    flagged = product_df[product_df[margin_col] < margin_threshold].copy()
    if flagged.empty:
        return pd.DataFrame(columns=["Product ID", "Product Name", "Division", "Sales", "Gross Margin %", "Cost Ratio %", "Recommended Action", "Rationale"])
        
    records = []
    for _, row in flagged.iterrows():
        pname = row["Product Name"]
        pid = row["Product ID"]
        div = row["Division"]
        sales = row["Sales"]
        margin = row[margin_col]
        cost_ratio = row["Cost Ratio %"]
        
        # Heuristics to determine specific action and rationale
        if cost_ratio > 90.0:
            rec = "Cost Renegotiation"
            rat = f"Critical manufacturing cost ratio ({cost_ratio:.1f}%) requires immediate raw material procurement audit and supplier price renegotiation."
        elif sales < 150.0:
            rec = "Discontinuation Review"
            rat = f"Sub-scale product (Sales: ${sales:.2f}) with compressed margin ({margin:.1f}%) warrants SKU rationalization and discontinuation review."
        else:
            rec = "Repricing"
            rat = f"Significant sales volume (${sales:,.2f}) but compressed margin ({margin:.1f}%) warrants a mandatory 10-15% wholesale price adjustment."
            
        records.append({
            "Product ID": pid,
            "Product Name": pname,
            "Division": div,
            "Sales": sales,
            "Gross Margin %": margin,
            "Cost Ratio %": cost_ratio,
            "Recommended Action": rec,
            "Rationale": rat
        })
        
    return pd.DataFrame(records)

