"""
Cost vs Margin Diagnostics page for Nassau Candy Distributor dashboard.
Displays order-level cost-sales diagnostics, dynamic margin risk table, and data exports.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from src.profitability import analyze_product_profitability
from src.risk_analysis import get_margin_risk_table
from dashboard.components import get_excel_download_bytes


def render_page_cost_margin(df: pd.DataFrame, clean_df: pd.DataFrame, margin_threshold: float):
    st.markdown("## 🔍 Cost & Margin Diagnostics")
    st.markdown("Diagnose order-level cost structure, evaluate products below margin threshold, and review recommendations.")
    
    if df.empty:
        st.warning("No data available for the selected filters.")
        return
        
    prod_df = analyze_product_profitability(df, margin_threshold)
    risk_table = get_margin_risk_table(prod_df, margin_threshold)
    
    # 1. Order-Level Cost vs Sales Scatter
    st.markdown("### 📈 Order-Level Cost vs Sales Diagnostics")
    st.markdown("Transaction-level view of Cost vs Sales grouped by Division. Points below the diagonal are profitable; closer to the line means higher cost-ratio.")
    
    fig_scatter = px.scatter(
        df,
        x="Sales",
        y="Cost",
        color="Division",
        hover_data=["Order ID", "Product ID", "Product Name", "Gross Profit", "Units"],
        color_discrete_map={"Chocolate": "#8b5cf6", "Other": "#06b6d4", "Sugar": "#f43f5e"},
        opacity=0.65
    )
    
    # Add a reference 1:1 line representing zero margin (Cost = Sales)
    max_val = max(df["Sales"].max(), df["Cost"].max())
    fig_scatter.add_trace(go.Scatter(
        x=[0, max_val],
        y=[0, max_val],
        mode="lines",
        name="Cost = Sales (0% Margin)",
        line=dict(color="#ef4444", dash="dash")
    ))
    
    fig_scatter.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=420,
        xaxis=dict(title="Order Sales ($)", gridcolor="rgba(255,255,255,0.08)"),
        yaxis=dict(title="Order Cost ($)", gridcolor="rgba(255,255,255,0.08)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.markdown("---")
    
    # 2. Dynamic Margin Risk Table
    st.markdown("### ⚠️ Margin Risk Diagnostics Table")
    st.markdown(f"Products with sales volume and a profit margin below the current threshold of **{margin_threshold:.1f}%**.")
    
    if not risk_table.empty:
        st.error(f"🚨 {len(risk_table)} product(s) flagged below the {margin_threshold:.1f}% margin threshold!")
        st.dataframe(
            risk_table.style.format({
                "Sales": "${:,.2f}",
                "Gross Margin %": "{:.2f}%",
                "Cost Ratio %": "{:.2f}%"
            }),
            use_container_width=True
        )
    else:
        st.success(f"✅ No products found below the {margin_threshold:.1f}% margin threshold!")
        
    st.markdown("---")
    
    # 3. Downloads / Export Suite (previously on page_recommendations)
    st.markdown("### 📥 Download Analytics Reports & Data Tables")
    st.markdown("Export cleaned raw datasets and processed analytical tables in CSV or multi-tab Excel format.")
    
    # Generate export dictionary
    from src.division_analysis import analyze_divisions
    from src.pareto import compute_pareto_analysis
    from src.factory_analysis import analyze_factory_performance
    from src.risk_analysis import compute_product_risk_scores
    
    risk_df = compute_product_risk_scores(prod_df)
    div_df = analyze_divisions(df)
    factory_df = analyze_factory_performance(df, risk_df)
    rev_pareto, prof_pareto, pareto_metrics = compute_pareto_analysis(df)

    
    export_dict = {
        "Cleaned Raw Data": clean_df,
        "Product Analysis": risk_df,
        "Division Analysis": div_df,
        "Margin Risk Table": risk_table if not risk_table.empty else pd.DataFrame(columns=["Status"]),
        "Profit Pareto": prof_pareto,
        "Revenue Pareto": rev_pareto,
        "Factory Performance": factory_df
    }

    
    excel_bytes = get_excel_download_bytes(export_dict)
    
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            label="📊 Download Complete Excel Suite (.xlsx)",
            data=excel_bytes,
            file_name="Nassau_Candy_Diagnostics_Suite.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    with col_dl2:
        st.download_button(
            label="📄 Download Cleaned Data CSV (.csv)",
            data=clean_df.to_csv(index=False).encode("utf-8"),
            file_name="Nassau_Candy_Cleaned_Transactions.csv",
            mime="text/csv"
        )

