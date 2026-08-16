"""
Route Drill-Down tab page for Nassau Candy Route Efficiency Analysis dashboard.
Allows state-level drilldown and order-level transaction timeline inspections.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def render_page_route_drilldown(df: pd.DataFrame, delay_threshold: float):
    st.markdown("## 🔍 Route Performance Drill-Down")
    st.markdown("Select a specific factory and customer state to inspect transaction-level timelines and efficiency trends.")
    
    if df.empty:
        st.warning("No data available for the selected filters.")
        return
        
    # 1. Sidebar/Dropdown selectors for Drill-down
    col_sel1, col_sel2 = st.columns(2)
    
    with col_sel1:
        factory_list = sorted(df["Factory"].unique())
        selected_factory = st.selectbox("Select Factory Node", factory_list)
        
    with col_sel2:
        # Filter states available for the selected factory
        available_states = sorted(df[df["Factory"] == selected_factory]["State/Province"].unique())
        selected_state = st.selectbox("Select Customer State/Province", available_states)
        
    # Filter dataset for this specific route
    route_data = df[(df["Factory"] == selected_factory) & (df["State/Province"] == selected_state)].copy()
    
    if route_data.empty:
        st.warning("No shipments found for this specific route combination.")
        return
        
    # Sort by order date
    route_data = route_data.sort_values(by="Order Date")
    
    # 2. Route Metrics
    total_orders = len(route_data)
    avg_lt = route_data["Shipping Lead Time"].mean()
    max_lt = route_data["Shipping Lead Time"].max()
    delays = (route_data["Shipping Lead Time"] > delay_threshold).sum()
    route_delay_rate = (delays / total_orders * 100.0) if total_orders > 0 else 0.0
    
    st.markdown(f"### 📍 Route Analysis: `{selected_factory} ➔ {selected_state}`")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Shipments", f"{total_orders:,}")
    with c2:
        st.metric("Average Lead Time", f"{avg_lt:.2f} Days")
    with c3:
        st.metric("Max Lead Time", f"{max_lt:.1f} Days")
    with c4:
        st.metric("Route Delay Rate %", f"{route_delay_rate:.2f}%", f"Count: {delays}")
        
    st.markdown("---")
    
    # 3. Shipment timeline trend chart
    st.markdown("### 📅 Shipment Timeline & Lead Time Trends over Time")
    
    # Plot lead time over order date
    fig_line = px.scatter(
        route_data,
        x="Order Date",
        y="Shipping Lead Time",
        color="Ship Mode",
        size="Units",
        hover_data=["Order ID", "Product Name", "Sales"],
        color_discrete_sequence=px.colors.qualitative.Safe,
        labels={"Shipping Lead Time": "Lead Time (Days)", "Order Date": "Order Date"}
    )
    
    # Add a horizontal line for the delay threshold
    fig_line.add_hline(
        y=delay_threshold, 
        line_dash="dash", 
        line_color="red", 
        annotation_text="Delay Threshold", 
        annotation_position="top left"
    )
    
    fig_line.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=350,
        xaxis=dict(title="Order Date"),
        yaxis=dict(title="Lead Time (Days)")
    )
    
    st.plotly_chart(fig_line, use_container_width=True)
    
    st.markdown("---")
    
    # 4. Order-level Details Table
    st.markdown("### 📋 Order-level Shipment Details")
    st.markdown("Detailed transaction grid for all orders shipped on this route.")
    
    st.dataframe(
        route_data[[
            "Order ID", "Order Date", "Ship Date", "Ship Mode", 
            "Shipping Lead Time", "Customer ID", "Product Name", "Sales", "Units"
        ]].style.format({
            "Order Date": lambda x: x.strftime("%Y-%m-%d") if not pd.isnull(x) else "",
            "Ship Date": lambda x: x.strftime("%Y-%m-%d") if not pd.isnull(x) else "",
            "Shipping Lead Time": "{:.0f} Days",
            "Sales": "${:,.2f}",
            "Units": "{:,}"
        }),
        use_container_width=True,
        height=300
    )
