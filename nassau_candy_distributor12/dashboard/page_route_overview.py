"""
Route Efficiency Overview tab page for Nassau Candy Shipping Route Analysis dashboard.
Displays overall shipping KPIs, fastest/slowest leaderboards, and route metrics.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.route_analysis import aggregate_route_performance, get_route_leaderboards


def render_page_route_overview(df: pd.DataFrame, delay_threshold: float):
    st.markdown("## 📊 Route Efficiency Overview")
    st.markdown("Macro-level operational metrics, shipping duration leaderboards, and route performance rankings.")
    
    if df.empty:
        st.warning("No data available for the selected filters.")
        return
        
    # Aggregate route performance
    state_routes, region_routes = aggregate_route_performance(df, delay_threshold)
    
    if state_routes.empty:
        st.warning("No route data generated.")
        return
        
    # 1. Macro KPIs
    total_shipments = len(df)
    avg_lead_time = df["Shipping Lead Time"].mean()
    delay_rate = (df["Shipping Lead Time"] > delay_threshold).sum() / total_shipments * 100.0 if total_shipments > 0 else 0.0
    num_routes = len(state_routes)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Shipments", f"{total_shipments:,}")
    with c2:
        st.metric("Average Lead Time", f"{avg_lead_time:.2f} Days")
    with c3:
        st.metric("Enterprise Delay Rate %", f"{delay_rate:.2f}%", f"Threshold: > {delay_threshold} days")
    with c4:
        st.metric("Active Shipping Routes", f"{num_routes:,} (State-Level)")
        
    st.markdown("---")
    
    # 2. Fastest vs Slowest Routes (Leaderboards)
    st.markdown("### 🏆 Route Efficiency Leaderboards")
    top_eff, least_eff = get_route_leaderboards(state_routes)
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.success("🟢 Top 10 Most Efficient Routes (Fastest Lead Times)")
        st.dataframe(
            top_eff[["Factory", "State/Province", "Shipments", "Avg_Lead_Time", "Route Efficiency Score"]].style.format({
                "Avg_Lead_Time": "{:.2f} Days",
                "Route Efficiency Score": "{:.1f}/100"
            }),
            use_container_width=True,
            hide_index=True
        )
        
    with col_right:
        st.error("🔴 Bottom 10 Least Efficient Routes (Slowest Lead Times)")
        st.dataframe(
            least_eff[["Factory", "State/Province", "Shipments", "Avg_Lead_Time", "Route Efficiency Score"]].style.format({
                "Avg_Lead_Time": "{:.2f} Days",
                "Route Efficiency Score": "{:.1f}/100"
            }),
            use_container_width=True,
            hide_index=True
        )
        
    st.markdown("---")
    
    # 3. Bar Chart: Average Lead Time by Route (State Level)
    st.markdown("### 📈 Average Lead Time by Shipping Route (State Level)")
    st.markdown("Average shipping duration per active route, ordered from fastest to slowest.")
    
    # Sort state routes for the chart
    chart_df = state_routes.sort_values(by="Avg_Lead_Time").head(30) # Show top 30 routes for readability
    
    fig_bar = px.bar(
        chart_df,
        x="Route State",
        y="Avg_Lead_Time",
        color="Avg_Lead_Time",
        color_continuous_scale="RdYlGn_r", # green for fast, red for slow
        labels={"Avg_Lead_Time": "Avg Lead Time (Days)", "Route State": "Route"},
        text="Avg_Lead_Time"
    )
    fig_bar.update_traces(texttemplate="%{text:.1f}d", textposition="outside")
    fig_bar.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=400,
        xaxis=dict(tickangle=-45, title="Shipping Route"),
        yaxis=dict(title="Average Lead Time (Days)"),
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    
    st.markdown("---")
    
    # 4. Full Leaderboard Table
    st.markdown("### 📋 Complete Route Performance Leaderboard")
    st.markdown("Comprehensive performance metrics for all factory-to-state shipping routes.")
    
    st.dataframe(
        state_routes[[
            "Route State", "Factory", "State/Province", "Shipments", 
            "Avg_Lead_Time", "Std_Lead_Time", "Delays", "Delay Frequency %", "Route Efficiency Score"
        ]].style.format({
            "Avg_Lead_Time": "{:.2f}",
            "Std_Lead_Time": "{:.2f}",
            "Delays": "{:,}",
            "Delay Frequency %": "{:.2f}%",
            "Route Efficiency Score": "{:.1f}"
        }),
        use_container_width=True,
        height=400
    )
