"""
Division Performance Dashboard page for Nassau Candy Distributor dashboard.
Evaluates revenue, profit contribution, and order-level margin distributions by division.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from src.division_analysis import analyze_divisions



def render_page_division(df: pd.DataFrame):
    st.markdown("## 🏢 Division Performance Dashboard")
    st.markdown("Benchmarking revenue contribution, absolute profit, and margin efficiency across business divisions.")
    
    if df.empty:
        st.warning("No data available for the selected filters.")
        return
        
    div_df = analyze_divisions(df)
    
    # 1. Division Summary Cards
    cols = st.columns(len(div_df))
    for idx, row in div_df.iterrows():
        if idx < len(cols):
            with cols[idx]:
                st.markdown(f"### {row['Division']}")
                st.markdown(f"**Classification:** `{row['Division Classification']}`")
                st.markdown(f"**Revenue:** `${row['Revenue']:,.2f}`")
                st.markdown(f"**Gross Profit:** `${row['Gross_Profit']:,.2f}`")
                st.markdown(f"**Gross Margin:** `{row['Gross Margin %']:.2f}%`")
                st.markdown(f"**Profit Share:** `{row['Profit Contribution %']:.1f}%`")
                st.markdown(f"**Active Products:** `{row['Product_Count']}` SKUs")
                # Highlight if division profit share is underperforming relative to revenue share
                if row["Imbalance Flag"]:
                    st.warning("⚠️ Profit Share is below Revenue Share!")
                else:
                    st.success("✅ Healthy Profit-to-Revenue Ratio")
                
    st.markdown("---")
    
    # 2. Charts Row (Revenue vs Gross Profit Bar Chart + Margin Boxplot)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Revenue vs Gross Profit by Division")
        st.markdown("Comparison of total revenue (blue) and absolute gross profit (green) by division.")
        
        fig_rev_prof = go.Figure()
        fig_rev_prof.add_trace(go.Bar(
            x=div_df["Division"], 
            y=div_df["Revenue"], 
            name="Revenue ($)", 
            marker_color="#0284c7"
        ))
        fig_rev_prof.add_trace(go.Bar(
            x=div_df["Division"], 
            y=div_df["Gross_Profit"], 
            name="Gross Profit ($)", 
            marker_color="#10b981"
        ))
        fig_rev_prof.update_layout(
            barmode="group",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=380,
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_rev_prof, use_container_width=True)
        
    with col2:
        st.markdown("### 📦 Gross Margin % Distribution by Division")
        st.markdown("Order-level gross margin spread (minimum, quartiles, outliers) across divisions.")
        
        # Calculate order-level margin percentage
        df_order_margin = df.copy()
        df_order_margin["Order Gross Margin %"] = np.where(
            df_order_margin["Sales"] > 0,
            (df_order_margin["Gross Profit"] / df_order_margin["Sales"]) * 100.0,
            0.0
        )
        
        fig_box = px.box(
            df_order_margin,
            x="Division",
            y="Order Gross Margin %",
            color="Division",
            points="outliers",
            color_discrete_map={"Chocolate": "#8b5cf6", "Other": "#06b6d4", "Sugar": "#f43f5e"}
        )
        fig_box.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=380,
            showlegend=False,
            margin=dict(l=20, r=20, t=30, b=20),
            xaxis=dict(title="Division"),
            yaxis=dict(title="Order Margin %", range=[0, 105], gridcolor="rgba(255,255,255,0.08)")
        )
        st.plotly_chart(fig_box, use_container_width=True)
        
    st.markdown("---")
    
    # 3. Division Summary Table
    st.markdown("### 📋 Division Metrics Summary Table")
    
    display_cols = [
        "Division", "Division Classification", "Revenue", "Cost", "Gross_Profit",
        "Gross Margin %", "Units", "Profit per Unit", "Cost Ratio %",
        "Product_Count", "Revenue Contribution %", "Profit Contribution %", 
        "Profit Share vs Revenue Share Mismatch %", "Imbalance Flag"
    ]
    
    st.dataframe(
        div_df[display_cols].style.format({
            "Revenue": "${:,.2f}",
            "Cost": "${:,.2f}",
            "Gross_Profit": "${:,.2f}",
            "Gross Margin %": "{:.2f}%",
            "Units": "{:,}",
            "Profit per Unit": "${:.2f}",
            "Cost Ratio %": "{:.2f}%",
            "Revenue Contribution %": "{:.2f}%",
            "Profit Contribution %": "{:.2f}%",
            "Profit Share vs Revenue Share Mismatch %": "{:+.2f}%"
        }),
        use_container_width=True
    )

