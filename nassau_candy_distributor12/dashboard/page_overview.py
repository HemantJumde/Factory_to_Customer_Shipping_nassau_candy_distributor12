"""
Executive Overview page for Nassau Candy Distributor dashboard.
Displays top-level KPIs, revenue & profit trends, margin performance, top products, division breakdown, and key executive findings.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dashboard.components import render_kpi_card
from src.profitability import calculate_overall_kpis, analyze_product_profitability
from src.division_analysis import analyze_divisions


def render_page_overview(df: pd.DataFrame):
    st.markdown("## 📊 Executive Overview & Business Health")
    st.markdown("Macro-level profitability, performance trends, division hierarchy, and key business highlights.")
    
    if df.empty:
        st.warning("No data available for the selected filters.")
        return
        
    # Top KPIs
    kpis = calculate_overall_kpis(df)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        render_kpi_card("Total Revenue", f"${kpis['total_revenue']:,.2f}", f"{kpis['total_orders']:,} Total Orders")
    with col2:
        render_kpi_card("Total Cost", f"${kpis['total_cost']:,.2f}", f"{kpis['cost_ratio_pct']:.1f}% Cost Ratio")
    with col3:
        render_kpi_card("Gross Profit", f"${kpis['total_gross_profit']:,.2f}", f"{kpis['profit_per_unit']:.2f} / Unit")
    with col4:
        render_kpi_card("Gross Margin %", f"{kpis['gross_margin_pct']:.2f}%", f"Target Benchmark: 50.0%")
    with col5:
        render_kpi_card("Units Sold", f"{kpis['total_units']:,}", f"${kpis['avg_order_value']:.2f} Avg Order Value")
        
    st.markdown("---")
    
    # Revenue, Profit & Margin Time Series Trends
    st.markdown("### 📈 Monthly Revenue, Gross Profit & Margin Trends")
    
    monthly = df.set_index("Order Date").resample("M").agg(
        Sales=("Sales", "sum"),
        Cost=("Cost", "sum"),
        Gross_Profit=("Gross Profit", "sum"),
        Units=("Units", "sum")
    ).reset_index()
    
    monthly["Order Month"] = monthly["Order Date"].dt.strftime("%b %Y")
    monthly["Gross Margin %"] = (monthly["Gross_Profit"] / monthly["Sales"] * 100.0).fillna(0.0)
    
    fig_trend = go.Figure()
    
    fig_trend.add_trace(go.Bar(
        x=monthly["Order Month"],
        y=monthly["Sales"],
        name="Revenue ($)",
        marker_color="#0284c7",
        opacity=0.85
    ))
    
    fig_trend.add_trace(go.Bar(
        x=monthly["Order Month"],
        y=monthly["Gross_Profit"],
        name="Gross Profit ($)",
        marker_color="#10b981",
        opacity=0.9
    ))
    
    fig_trend.add_trace(go.Scatter(
        x=monthly["Order Month"],
        y=monthly["Gross Margin %"],
        name="Gross Margin %",
        yaxis="y2",
        mode="lines+markers",
        line=dict(color="#f59e0b", width=3),
        marker=dict(size=8)
    ))
    
    fig_trend.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=420,
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis=dict(title="Amount ($)", gridcolor="rgba(255,255,255,0.08)"),
        yaxis2=dict(title="Gross Margin %", overlaying="y", side="right", range=[0, 100], showgrid=False)
    )
    
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Product & Division Breakdown Section
    col_left, col_right = st.columns(2)
    
    prod_df = analyze_product_profitability(df)
    div_df = analyze_divisions(df)
    
    with col_left:
        st.markdown("### 🏆 Top 5 Products by Profit")
        top_5_prod = prod_df.head(5)
        fig_prod = px.bar(
            top_5_prod,
            x="Gross_Profit",
            y="Product Name",
            orientation="h",
            text="Gross_Profit",
            color="Gross Margin %",
            color_continuous_scale="Viridis",
            labels={"Gross_Profit": "Gross Profit ($)", "Product Name": "Product"}
        )
        fig_prod.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
        fig_prod.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=350,
            yaxis=dict(autorange="reversed")
        )
        st.plotly_chart(fig_prod, use_container_width=True)
        
    with col_right:
        st.markdown("### 🏢 Division Profit Contribution")
        fig_div = px.pie(
            div_df,
            values="Gross_Profit",
            names="Division",
            hole=0.45,
            color="Division",
            color_discrete_map={"Chocolate": "#8b5cf6", "Other": "#06b6d4", "Sugar": "#f43f5e"}
        )
        fig_div.update_traces(textinfo="label+percent+value", valueformat="$,.0f")
        fig_div.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=350
        )
        st.plotly_chart(fig_div, use_container_width=True)
        
    # Key Executive Findings Box
    st.markdown("### 📌 Executive Key Findings")
    st.info("""
    - **Chocolate Dominance**: The Chocolate division is the core revenue driver ($131.7K out of $141.8K total), delivering **66.0% gross margin** and generating 97.8% of total distributor profits.
    - **Other & Sugar Division Drag**: The Sugar and Other divisions contribute less than 2.5% of total gross profit, suffering from low order volume and compressed profit per unit.
    - **Top Profit SKU**: `Wonka Bar -Scrumdiddlyumptious` is the single most profitable product, generating **$19,357.50** in gross profit (69.4% margin).
    - **Margin Volatility**: Order-level margin volatility remains low (std dev ~2.8%), indicating stable contract pricing across customer shipments.
    """)
