"""
Geographic Shipping Map tab page for Nassau Candy Route Efficiency Analysis dashboard.
Renders US state-level choropleth lead time heatmap and highlights regional bottlenecks.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.route_analysis import aggregate_route_performance, detect_bottlenecks

# Mapping of US State Names to 2-letter codes for choropleth
US_STATE_CODES = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
    "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
    "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
    "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
    "District Of Columbia": "DC", "District of Columbia": "DC"
}


def render_page_geo_map(df: pd.DataFrame, delay_threshold: float):
    st.markdown("## 🌎 Geographic Shipping Map & Bottleneck Analysis")
    st.markdown("Visualize spatial logistics performance across the United States and identify high-delay nodes.")
    
    if df.empty:
        st.warning("No data available for the selected filters.")
        return
        
    state_routes, region_routes = aggregate_route_performance(df, delay_threshold)
    congestion_df, delay_df = detect_bottlenecks(df, state_routes)
    
    # 1. Calculate State-level averages for Choropleth
    state_avg = df.groupby("State/Province").agg(
        Avg_Lead_Time=("Shipping Lead Time", "mean"),
        Shipments=("Order ID", "count"),
        Delays=("Shipping Lead Time", lambda x: (x > delay_threshold).sum())
    ).reset_index()
    
    state_avg["Delay Rate %"] = (state_avg["Delays"] / state_avg["Shipments"] * 100.0).round(2)
    state_avg["State Code"] = state_avg["State/Province"].map(US_STATE_CODES)
    
    # Drop rows without valid state codes (e.g. if any Canadian province is in data)
    state_avg = state_avg.dropna(subset=["State Code"])
    
    # 2. Render Choropleth Map
    st.markdown("### 🗺️ US Shipping Efficiency Heatmap")
    st.markdown("Color gradients represent the average lead time (days) for shipments arriving in each state.")
    
    fig_map = px.choropleth(
        state_avg,
        locations="State Code",
        locationmode="USA-states",
        scope="usa",
        color="Avg_Lead_Time",
        color_continuous_scale="RdYlGn_r", # Green for fast, Red for slow
        hover_name="State/Province",
        hover_data=["Shipments", "Delay Rate %"],
        labels={"Avg_Lead_Time": "Avg Lead Time (Days)"}
    )
    
    fig_map.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        geo=dict(
            bgcolor="rgba(0,0,0,0)",
            lakecolor="#0f172a",
            landcolor="#1e293b",
            subunitcolor="#475569"
        ),
        height=500,
        margin=dict(l=0, r=0, t=10, b=0)
    )
    
    st.plotly_chart(fig_map, use_container_width=True)
    
    st.markdown("---")
    
    # 3. Bottleneck Analysis Sections
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("### 🚦 High-Volume Congestion Bottlenecks")
        st.markdown("Routes with **above-median volume** AND **above-median lead times** (warranting process flow changes).")
        
        if not congestion_df.empty:
            st.dataframe(
                congestion_df[["Route State", "Shipments", "Avg_Lead_Time", "Delay Frequency %"]].style.format({
                    "Avg_Lead_Time": "{:.2f} Days",
                    "Delay Frequency %": "{:.2f}%"
                }),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.success("No high-volume congestion bottlenecks detected!")
            
    with col_right:
        st.markdown("### ⚠️ Delay-Prone Routes (>50% Delays)")
        st.markdown("Routes where **more than half** of all shipments exceed the delivery threshold.")
        
        if not delay_df.empty:
            st.dataframe(
                delay_df[["Route State", "Shipments", "Avg_Lead_Time", "Delay Frequency %"]].style.format({
                    "Avg_Lead_Time": "{:.2f} Days",
                    "Delay Frequency %": "{:.2f}%"
                }),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.success("No high-delay routes detected!")
