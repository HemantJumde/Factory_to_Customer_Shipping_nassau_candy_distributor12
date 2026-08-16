"""
Automated strategic recommendation engine for Nassau Candy Distributor.
Classifies products into action quadrants and synthesizes specific, data-backed business guidance.
"""

from typing import List, Dict, Any
import pandas as pd
import numpy as np


def generate_strategic_recommendations(product_df: pd.DataFrame, division_df: pd.DataFrame, factory_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generates data-driven strategic business recommendations categorized by product quadrant,
    division focus, and factory optimization.
    """
    if product_df.empty:
        return {"quadrant_summary": {}, "product_recommendations": [], "executive_insights": []}
        
    df_prod = product_df.copy()
    
    # 1. Classify Action Strategy
    def assign_strategy(row):
        matrix = row.get("Matrix Category", "")
        if "1." in matrix:
            return "PROTECT"
        elif "2." in matrix:
            return "OPTIMIZE"
        elif "3." in matrix:
            return "GROW"
        else:
            return "REVIEW"
            
    df_prod["Strategy Action"] = df_prod.apply(assign_strategy, axis=1)
    
    # Group products by strategy action
    protect_prods = df_prod[df_prod["Strategy Action"] == "PROTECT"]
    optimize_prods = df_prod[df_prod["Strategy Action"] == "OPTIMIZE"]
    grow_prods = df_prod[df_prod["Strategy Action"] == "GROW"]
    review_prods = df_prod[df_prod["Strategy Action"] == "REVIEW"]
    
    rec_list = []
    
    # Generate Product-Specific Action Cards
    for _, row in df_prod.iterrows():
        action = row["Strategy Action"]
        pname = row["Product Name"]
        pid = row["Product ID"]
        div = row["Division"]
        sales = row["Sales"]
        margin = row["Gross Margin %"]
        profit = row["Gross_Profit"]
        cost_ratio = row["Cost Ratio %"]
        risk_level = row.get("Risk Level", "N/A")
        
        if action == "PROTECT":
            desc = (
                f"**{pname}** ({pid}) is a core profit engine in the **{div}** division, generating "
                f"**${sales:,.2f}** in revenue and **${profit:,.2f}** in gross profit at a high **{margin:.1f}%** margin. "
                f"Action: Secure supply chain at factory level, maintain premium pricing, and guard market share against stockouts."
            )
        elif action == "OPTIMIZE":
            desc = (
                f"**{pname}** ({pid}) drives massive volume (**${sales:,.2f}** sales) but delivers a suppressed margin of "
                f"**{margin:.1f}%** with manufacturing cost eating **{cost_ratio:.1f}%** of sales. "
                f"Action: Initiate targeted 3-5% price increase, negotiate raw ingredient bulk pricing, and optimize packaging sizes."
            )
        elif action == "GROW":
            desc = (
                f"**{pname}** ({pid}) achieves exceptional profitability (**{margin:.1f}%** margin) but low total volume "
                f"(**${sales:,.2f}** sales). "
                f"Action: Expand regional distribution channels, launch targeted promotional campaigns, and bundle with core chocolate items."
            )
        else: # REVIEW
            desc = (
                f"**{pname}** ({pid}) is an underperforming SKU in the **{div}** division with only **${sales:,.2f}** sales and "
                f"**${profit:,.2f}** total profit ({margin:.1f}% margin). "
                f"Action: Audit production overhead, evaluate SKU rationalization, or convert to seasonal/custom order status."
            )
            
        rec_list.append({
            "Product ID": pid,
            "Product Name": pname,
            "Division": div,
            "Strategy Action": action,
            "Sales": sales,
            "Gross Margin %": margin,
            "Gross Profit": profit,
            "Risk Level": risk_level,
            "Recommendation Details": desc
        })
        
    # Strategic Executive Insights
    insights = []
    
    top_profit_prod = df_prod.loc[df_prod["Gross_Profit"].idxmax()]
    insights.append(
        f"**Top Profit Driver**: `{top_profit_prod['Product Name']}` delivers ${top_profit_prod['Gross_Profit']:,.2f} "
        f"({top_profit_prod['Profit Contribution %']:.1f}% of total distributor profit)."
    )
    
    if not optimize_prods.empty:
        total_opt_sales = optimize_prods["Sales"].sum()
        insights.append(
            f"**Margin Recovery Opportunity**: {len(optimize_prods)} high-volume product(s) ({', '.join(optimize_prods['Product Name'].tolist())}) "
            f"account for ${total_opt_sales:,.2f} in sales but have below-median margins. A 3% margin improvement would yield "
            f"**+${total_opt_sales * 0.03:,.2f}** in additional net profit."
        )
        
    if not review_prods.empty:
        insights.append(
            f"**SKU Rationalization Target**: {len(review_prods)} product(s) in the Review quadrant generate combined profit of "
            f"only **${review_prods['Gross_Profit'].sum():,.2f}**. Reallocating marketing budget to Grow products will yield higher ROI."
        )
        
    # Division Insight
    if not division_df.empty:
        top_div = division_df.iloc[0]
        insights.append(
            f"**Division Dominance**: The **{top_div['Division']}** division commands **{top_div['Profit Contribution %']:.1f}%** "
            f"of total distributor gross profit (${top_div['Gross_Profit']:,.2f})."
        )
        
    return {
        "summary_counts": {
            "Protect": len(protect_prods),
            "Optimize": len(optimize_prods),
            "Grow": len(grow_prods),
            "Review": len(review_prods)
        },
        "product_recommendations_df": pd.DataFrame(rec_list),
        "executive_insights": insights
    }
