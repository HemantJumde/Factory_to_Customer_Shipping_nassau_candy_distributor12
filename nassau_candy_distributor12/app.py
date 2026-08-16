"""
Main Streamlit application entry point for Nassau Candy Factory-to-Customer Shipping Route Analysis.
Run with: streamlit run app.py
"""

import os
import sys
import streamlit as st

# Configure page metadata
st.set_page_config(
    page_title="Nassau Candy — Shipping Route Efficiency Analytics",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ensure current directory is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.data_loader import load_raw_data
from src.route_cleaning import clean_and_prepare_route_data
from dashboard.components import inject_custom_css, render_sidebar_filters
from dashboard.page_route_overview import render_page_route_overview
from dashboard.page_geo_map import render_page_geo_map
from dashboard.page_ship_mode import render_page_ship_mode
from dashboard.page_route_drilldown import render_page_route_drilldown


@st.cache_data
def get_cleaned_shipping_data():
    """Loads, cleans, and enriches dataset for route efficiency analysis (cached)."""
    raw_df = load_raw_data()
    cleaned_df, quality_audit = clean_and_prepare_route_data(raw_df)
    return cleaned_df, quality_audit


def main():
    # Inject Custom CSS Theme
    inject_custom_css()
    
    # Load Data
    try:
        df, quality_audit = get_cleaned_shipping_data()
    except Exception as e:
        st.error(f"❌ Error loading dataset: {str(e)}")
        st.info("Please verify that `data/nassau_candy.csv` exists in the project folder.")
        st.stop()
        
    # App Header Banner
    st.markdown("""
        <div style="background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%); padding: 24px; border-radius: 12px; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.08); box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
            <h1 style="color: white; margin: 0; font-size: 2.2rem; font-weight: 700;">🚛 Nassau Candy Logistics Suite</h1>
            <p style="color: #38bdf8; margin: 4px 0 0 0; font-size: 1.1rem; font-weight: 500;">Factory-to-Customer Shipping Route Efficiency Analytics Portal</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Render Sidebar Filters
    filtered_df, delay_threshold = render_sidebar_filters(df)
    
    # Navigation Tabs (Exactly 4 Tabs requested in requirements)
    tab_overview, tab_map, tab_shipmode, tab_drilldown = st.tabs([
        "📊 Route Efficiency Overview",
        "🌎 Geographic Shipping Map",
        "✈️ Ship Mode Comparison",
        "🔍 Route Drill-Down"
    ])
    
    with tab_overview:
        render_page_route_overview(filtered_df, delay_threshold)
        
    with tab_map:
        render_page_geo_map(filtered_df, delay_threshold)
        
    with tab_shipmode:
        render_page_ship_mode(filtered_df, delay_threshold)
        
    with tab_drilldown:
        render_page_route_drilldown(filtered_df, delay_threshold)


if __name__ == "__main__":
    main()
