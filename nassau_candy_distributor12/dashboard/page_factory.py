"""
Factory Performance & Geographic Analysis page for Nassau Candy Distributor dashboard.
Evaluates production facility performance, factory geo map, SKU assignments, and facility risk exposure.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.profitability import analyze_product_profitability
from src.risk_analysis import compute_product_risk_scores
from src.factory_analysis import analyze_factory_performance, FACTORY_COORDINATES


def render_page_factory(df: pd.DataFrame):
    st.markdown("## 🏭 Factory Performance & Geographic Analytics")
    st.markdown("Operational evaluation of 5 primary manufacturing facilities across output, financial margin, and risk exposure.")
    
    if df.empty:
        st.warning("No data available for the selected filters.")
        return
        
    prod_df = analyze_product_profitability(df)
    risk_df = compute_product_risk_scores(prod_df)
    factory_df = analyze_factory_performance(df, risk_df)
    
    # Factory Geographic Map
    st.markdown("### 🗺️ Production Facility Geographic Distribution Map")
    
    fig_map = px.scatter_mapbox(
        factory_df,
        lat="Factory Lat",
        lon="Factory Lon",
        size="Gross_Profit",
        color="Gross Margin %",
        hover_name="Factory",
        hover_data=["Factory Location", "Revenue", "Gross_Profit", "Product_Count", "High/Critical Risk Products"],
        text="Factory",
        color_continuous_scale="Viridis",
        size_max=35,
        zoom=3.2,
        center={"lat": 39.8283, "lon": -98.5795}, # USA Geographic Center
        mapbox_style="carto-darkmatter"
    )
    fig_map.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        height=450,
        margin=dict(l=0, r=0, t=10, b=0)
    )
    st.plotly_chart(fig_map, use_container_width=True)
    
    st.markdown("---")
    
    # Factory Financial Comparison Charts
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("### 💵 Revenue vs Gross Profit by Factory")
        fig_fac_fin = go.Figure()
        fig_fac_fin.add_trace(go.Bar(
            x=factory_df["Factory"], y=factory_df["Revenue"], name="Revenue ($)", marker_color="#0284c7"
        ))
        fig_fac_fin.add_trace(go.Bar(
            x=factory_df["Factory"], y=factory_df["Gross_Profit"], name="Gross Profit ($)", marker_color="#10b981"
        ))
        fig_fac_fin.update_layout(
            barmode="group",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=380,
            xaxis=dict(tickangle=-15)
        )
        st.plotly_chart(fig_fac_fin, use_container_width=True)
        
    with col_right:
        st.markdown("### 🏭 Gross Margin % & Risk Exposure")
        fig_fac_margin = go.Figure()
        fig_fac_margin.add_trace(go.Bar(
            x=factory_df["Factory"], y=factory_df["Gross Margin %"], name="Gross Margin %", marker_color="#f59e0b"
        ))
        fig_fac_margin.add_trace(go.Scatter(
            x=factory_df["Factory"], y=factory_df["High/Critical Risk Products"], name="High/Critical Risk SKUs", yaxis="y2",
            mode="lines+markers", line=dict(color="#ef4444", width=3), marker=dict(size=10)
        ))
        fig_fac_margin.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=380,
            xaxis=dict(tickangle=-15),
            yaxis=dict(title="Gross Margin %", range=[0, 100]),
            yaxis2=dict(title="High Risk SKU Count", overlaying="y", side="right", showgrid=False)
        )
        st.plotly_chart(fig_fac_margin, use_container_width=True)
        
    # Factory Summary Data Table
    st.markdown("### 📋 Factory Metrics Summary Table")
    
    display_cols = [
        "Factory", "Factory Location", "Revenue", "Cost", "Gross_Profit",
        "Gross Margin %", "Units", "Profit per Unit", "Product_Count", "High/Critical Risk Products",
        "Revenue Contribution %", "Profit Contribution %"
    ]
    
    st.dataframe(
        factory_df[display_cols].style.format({
            "Revenue": "${:,.2f}",
            "Cost": "${:,.2f}",
            "Gross_Profit": "${:,.2f}",
            "Gross Margin %": "{:.2f}%",
            "Units": "{:,}",
            "Profit per Unit": "${:.2f}",
            "Revenue Contribution %": "{:.2f}%",
            "Profit Contribution %": "{:.2f}%"
        }),
        use_container_width=True
    )
