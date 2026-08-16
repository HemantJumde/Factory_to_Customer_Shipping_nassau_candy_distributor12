"""
Ship Mode Comparison tab page for Nassau Candy Route Efficiency Analysis dashboard.
Compares lead times, delay frequencies, and trade-offs across shipping methods.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def render_page_ship_mode(df: pd.DataFrame, delay_threshold: float):
    st.markdown("## ✈️ Ship Mode Performance Analysis")
    st.markdown("Assess lead times, reliability, and cost-to-time trade-offs across delivery methods.")
    
    if df.empty:
        st.warning("No data available for the selected filters.")
        return
        
    # 1. Compute summary stats per Ship Mode
    sm_summary = df.groupby("Ship Mode").agg(
        Shipments=("Order ID", "count"),
        Avg_Lead_Time=("Shipping Lead Time", "mean"),
        Std_Lead_Time=("Shipping Lead Time", "std"),
        Delays=("Shipping Lead Time", lambda x: (x > delay_threshold).sum()),
        Avg_Sales=("Sales", "mean"),
        Avg_Profit=("Gross Profit", "mean")
    ).reset_index()
    
    sm_summary["Std_Lead_Time"] = sm_summary["Std_Lead_Time"].fillna(0.0)
    sm_summary["Delay Rate %"] = (sm_summary["Delays"] / sm_summary["Shipments"] * 100.0).round(2)
    sm_summary["Avg_Lead_Time"] = sm_summary["Avg_Lead_Time"].round(2)
    sm_summary["Std_Lead_Time"] = sm_summary["Std_Lead_Time"].round(2)
    sm_summary["Avg_Sales"] = sm_summary["Avg_Sales"].round(2)
    sm_summary["Avg_Profit"] = sm_summary["Avg_Profit"].round(2)
    
    # 2. Render Metrics Table
    st.markdown("### 📋 Shipping Method Performance Benchmarks")
    st.dataframe(
        sm_summary[[
            "Ship Mode", "Shipments", "Avg_Lead_Time", "Std_Lead_Time", "Delay Rate %", "Avg_Sales", "Avg_Profit"
        ]].style.format({
            "Shipments": "{:,}",
            "Avg_Lead_Time": "{:.2f} Days",
            "Std_Lead_Time": "{:.2f} Days",
            "Delay Rate %": "{:.2f}%",
            "Avg_Sales": "${:,.2f}",
            "Avg_Profit": "${:,.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("---")
    
    # 3. Visualizations
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("### 📦 Lead Time Distribution by Shipping Method")
        fig_box = px.box(
            df,
            x="Ship Mode",
            y="Shipping Lead Time",
            color="Ship Mode",
            color_discrete_sequence=px.colors.qualitative.Safe,
            labels={"Shipping Lead Time": "Lead Time (Days)"}
        )
        fig_box.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=380,
            showlegend=False
        )
        st.plotly_chart(fig_box, use_container_width=True)
        
    with col_right:
        st.markdown("### ⏳ Delay Frequency by Shipping Method")
        fig_delay = px.bar(
            sm_summary,
            x="Ship Mode",
            y="Delay Rate %",
            color="Ship Mode",
            color_discrete_sequence=px.colors.qualitative.Safe,
            text="Delay Rate %",
            labels={"Delay Rate %": "Delay Rate (%)"}
        )
        fig_delay.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_delay.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=380,
            showlegend=False,
            yaxis=dict(range=[0, 110])
        )
        st.plotly_chart(fig_delay, use_container_width=True)
        
    st.markdown("---")
    
    # 4. Cost-Time Tradeoffs Analysis (Descriptive)
    st.markdown("### 💰 Cost-Time Trade-off Insights")
    
    # Business logic notes
    st.info("""
    - **Same Day & First Class**: Represent the fastest delivery methods. While they reduce lead times, they typically incur higher shipping premiums (evaluated relative to average Order Sales value).
    - **Standard Class**: High-volume, slower delivery method. Best suited for bulk orders that are not time-sensitive, where the distributor saves on shipping expenses.
    - **Observations**: Notice if the average Sales and Profit values differ significantly between First Class/Same Day and Standard. If expedited orders have lower sales values, the company may be overspending on expedited shipping premiums for small baskets.
    """)
