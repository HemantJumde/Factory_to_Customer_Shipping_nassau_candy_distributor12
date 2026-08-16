"""
Recommendations & Data Export page for Nassau Candy Distributor dashboard.
Automated data-backed recommendations engine, quadrant classification, and multi-format dataset exports (CSV / Excel).
"""

import streamlit as st
import pandas as pd
from src.profitability import analyze_product_profitability
from src.division_analysis import analyze_divisions
from src.risk_analysis import compute_product_risk_scores
from src.pareto import compute_pareto_analysis
from src.factory_analysis import analyze_factory_performance
from src.recommendations import generate_strategic_recommendations
from dashboard.components import get_excel_download_bytes


def render_page_recommendations(df: pd.DataFrame, clean_df: pd.DataFrame, quality_audit: dict):
    st.markdown("## 💡 Automated Business Recommendations & Data Downloads")
    st.markdown("Actionable product strategies derived from real analytical metrics, alongside exportable dataset packages.")
    
    if df.empty:
        st.warning("No data available for the selected filters.")
        return
        
    prod_df = analyze_product_profitability(df)
    risk_df = compute_product_risk_scores(prod_df)
    div_df = analyze_divisions(df)
    factory_df = analyze_factory_performance(df, risk_df)
    rev_pareto, prof_pareto, pareto_metrics = compute_pareto_analysis(df)
    
    rec_results = generate_strategic_recommendations(risk_df, div_df, factory_df)
    counts = rec_results["summary_counts"]
    
    # Strategy Quadrant Cards
    st.markdown("### 🎯 Strategic Product Action Quadrants")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("#### 🛡️ PROTECT")
        st.markdown(f"**`{counts.get('Protect', 0)}`** Products")
        st.markdown("High Sales + High Margin")
    with c2:
        st.markdown("#### ⚡ OPTIMIZE")
        st.markdown(f"**`{counts.get('Optimize', 0)}`** Products")
        st.markdown("High Sales + Low Margin")
    with c3:
        st.markdown("#### 🚀 GROW")
        st.markdown(f"**`{counts.get('Grow', 0)}`** Products")
        st.markdown("Low Sales + High Margin")
    with c4:
        st.markdown("#### 🔍 REVIEW")
        st.markdown(f"**`{counts.get('Review', 0)}`** Products")
        st.markdown("Low Sales + Low Margin")
        
    st.markdown("---")
    
    # Executive Key Findings & Recommendations
    st.markdown("### 📋 Executive Key Strategic Recommendations")
    for insight in rec_results["executive_insights"]:
        st.info(f"💡 {insight}")
        
    # Detailed Product Recommendations Data Table
    st.markdown("### 📝 Product-by-Product Action Guidance Table")
    rec_df = rec_results["product_recommendations_df"]
    
    st.dataframe(
        rec_df[[
            "Strategy Action", "Product ID", "Product Name", "Division",
            "Sales", "Gross Margin %", "Gross Profit", "Risk Level", "Recommendation Details"
        ]].style.format({
            "Sales": "${:,.2f}",
            "Gross Margin %": "{:.2f}%",
            "Gross Profit": "${:,.2f}"
        }),
        use_container_width=True,
        height=380
    )
    
    st.markdown("---")
    
    # Data Export Section
    st.markdown("### 📥 Download Analytics Reports & Data Tables")
    st.markdown("Export cleaned raw datasets and processed analytical tables in CSV or multi-tab Excel format.")
    
    export_dict = {
        "Cleaned Raw Data": clean_df,
        "Product Analysis": risk_df,
        "Division Analysis": div_df,
        "Risk Analysis": risk_df[["Product ID", "Product Name", "Division", "Risk Level", "Risk Score", "Risk Reasons"]],
        "Profit Pareto": prof_pareto,
        "Revenue Pareto": rev_pareto,
        "Factory Analysis": factory_df,
        "Recommendations": rec_df
    }
    
    # Excel Download Button
    excel_bytes = get_excel_download_bytes(export_dict)
    
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            label="📊 Download Complete Excel Suite (.xlsx)",
            data=excel_bytes,
            file_name="Nassau_Candy_Profitability_Analysis_Suite.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    with col_dl2:
        st.download_button(
            label="📄 Download Cleaned Data CSV (.csv)",
            data=clean_df.to_csv(index=False).encode("utf-8"),
            file_name="Nassau_Candy_Cleaned_Transactions.csv",
            mime="text/csv"
        )
