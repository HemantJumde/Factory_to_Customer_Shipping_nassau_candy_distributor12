"""
Profit Concentration Analysis page for Nassau Candy Distributor dashboard.
Calculates 80/20 product concentration and geographic state-level concentration risks.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.pareto import compute_pareto_analysis, compute_state_concentration


def render_page_pareto(df: pd.DataFrame):
    st.markdown("## 📐 Profit & Revenue Concentration Analysis (Pareto)")
    st.markdown("Evaluate product-level 80/20 concentration dynamics and state-level geographic dependencies.")
    
    if df.empty:
        st.warning("No data available for the selected filters.")
        return
        
    rev_df, prof_df, metrics = compute_pareto_analysis(df)
    state_df, state_metrics = compute_state_concentration(df)
    
    # 1. Executive Summary Concentration Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("#### 🎯 80% Profit Drivers")
        st.markdown(f"**`{metrics['profit_80_pct_count']}`** of `{metrics['total_products']}` SKUs")
        st.markdown(f"({metrics['profit_80_pct_product_share']:.1f}% of catalog)")
    with c2:
        st.markdown("#### 🎯 80% Revenue Drivers")
        st.markdown(f"**`{metrics['revenue_80_pct_count']}`** of `{metrics['total_products']}` SKUs")
        st.markdown(f"({metrics['revenue_50_pct_product_share']:.1f}% for 50% revenue)")
    with c3:
        st.markdown("#### ⚠️ Top 5 Profit Share")
        st.markdown(f"**`{metrics['top_5_profit_share_pct']:.1f}%`** of Total Profit")
        st.markdown("Extreme concentration risk!")
    with c4:
        st.markdown("#### 🌎 Top State Revenue Share")
        if not state_df.empty:
            top_state = state_df.iloc[0]
            st.markdown(f"**`{top_state['Revenue Share %']:.1f}%`** ({top_state['State/Province']})")
        else:
            st.markdown("N/A")
        st.markdown("Risk Threshold: 30.0%")
        
    st.markdown("---")
    
    # 2. Risk Warning Alerts
    # Product concentration alert
    if metrics["top_5_profit_share_pct"] > 80.0:
        st.warning(f"⚠️ **High Concentration Risk**: The top 5 products drive **{metrics['top_5_profit_share_pct']:.1f}%** of total gross profit. Nassau Candy is heavily reliant on a very narrow group of SKUs.")
        
    # State-level dependency risk alert
    if state_metrics.get("has_risk", False):
        for state, share in zip(state_metrics["risk_states"], state_metrics["risk_states_shares"]):
            st.error(f"🚨 **Geographic Dependency Risk**: State of **{state}** generates **{share:.1f}%** of total distributor revenue, exceeding the 30.0% risk threshold! Any regional economic disruption in this state poses significant risk.")
    else:
        st.success("✅ **Geographic Diversification**: No single state exceeds 30.0% of total distributor revenue.")
        
    st.markdown("---")
    
    # 3. Dual Pareto Charts
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("### 💵 Gross Profit Pareto Curve")
        st.markdown("Cumulative profit contribution descending. The line represents the running total percentage.")
        
        fig_prof_pareto = go.Figure()
        fig_prof_pareto.add_trace(go.Bar(
            x=prof_df["Product Name"],
            y=prof_df["Gross_Profit"],
            name="Gross Profit ($)",
            marker_color="#10b981"
        ))
        fig_prof_pareto.add_trace(go.Scatter(
            x=prof_df["Product Name"],
            y=prof_df["Cumulative Profit %"],
            name="Cumulative Profit %",
            yaxis="y2",
            mode="lines+markers",
            line=dict(color="#ef4444", width=3)
        ))
        fig_prof_pareto.add_hline(y=80.0, line_dash="dash", line_color="#f59e0b", yref="y2", annotation_text="80% Cutoff")
        fig_prof_pareto.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=380,
            xaxis=dict(tickangle=-45),
            yaxis=dict(title="Gross Profit ($)"),
            yaxis2=dict(title="Cumulative Profit %", overlaying="y", side="right", range=[0, 105], showgrid=False),
            margin=dict(l=20, r=20, t=30, b=100)
        )
        st.plotly_chart(fig_prof_pareto, use_container_width=True)
        
    with col_right:
        st.markdown("### 🌎 State-Level Revenue Share Chart")
        st.markdown("Distribution of distributor revenue by state/province. Threshold boundary marked at 30%.")
        
        # Plot top 10 states by revenue share
        top_states_df = state_df.head(10)
        
        fig_state = px.bar(
            top_states_df,
            x="State/Province",
            y="Revenue Share %",
            color="Revenue Share %",
            text="Revenue Share %",
            color_continuous_scale="Viridis",
            labels={"Revenue Share %": "Revenue Share %", "State/Province": "State"}
        )
        fig_state.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_state.add_hline(y=30.0, line_color="#ef4444", line_dash="dash", annotation_text="30% Dependency Limit")
        
        fig_state.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=380,
            coloraxis_showscale=False,
            margin=dict(l=20, r=20, t=30, b=100)
        )
        st.plotly_chart(fig_state, use_container_width=True)
        
    st.markdown("---")
    
    # 4. Profit Concentration Table
    st.markdown("### 📊 SKU Profit Concentration Breakdown Table")
    display_pareto = prof_df[[
        "Product Rank", "Product ID", "Product Name", "Division", "Gross_Profit",
        "Profit %", "Cumulative Profit %", "Pareto Class"
    ]]
    st.dataframe(
        display_pareto.style.format({
            "Gross_Profit": "${:,.2f}",
            "Profit %": "{:.2f}%",
            "Cumulative Profit %": "{:.2f}%"
        }),
        use_container_width=True
    )

