"""
Reusable UI components, sidebar filters, custom CSS styling, and export helpers for Streamlit dashboard.
"""

from typing import Dict, Any, Tuple
import io
import streamlit as st
import pandas as pd
import numpy as np


def inject_custom_css():
    """Injects high-end glassmorphism dark theme CSS styling into Streamlit app."""
    st.markdown("""
        <style>
        /* Modern Typography & Dark Mode Aesthetic */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        .main {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #f8fafc;
        }
        
        /* Metric Card Styling */
        .kpi-card {
            background: rgba(30, 41, 59, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(12px);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }
        .kpi-card:hover {
            transform: translateY(-3px);
            border-color: #38bdf8;
        }
        .kpi-label {
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #94a3b8;
            margin-bottom: 6px;
            font-weight: 600;
        }
        .kpi-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: #f8fafc;
        }
        .kpi-sub {
            font-size: 0.8rem;
            color: #38bdf8;
            margin-top: 4px;
            font-weight: 500;
        }
        
        /* Risk Badges */
        .badge-critical {
            background-color: #ef4444;
            color: white;
            padding: 4px 10px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.8rem;
        }
        .badge-high {
            background-color: #f97316;
            color: white;
            padding: 4px 10px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.8rem;
        }
        .badge-medium {
            background-color: #eab308;
            color: black;
            padding: 4px 10px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.8rem;
        }
        .badge-low {
            background-color: #22c55e;
            color: white;
            padding: 4px 10px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.8rem;
        }
        
        /* Sidebar Customization */
        [data-testid="stSidebar"] {
            background: #090d16;
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }
        
        /* Tab Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 48px;
            white-space: pre-wrap;
            background-color: rgba(30, 41, 59, 0.5);
            border-radius: 8px;
            color: #94a3b8;
            font-weight: 600;
        }
        .stTabs [aria-selected="true"] {
            background-color: #0284c7 !important;
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)


def render_kpi_card(label: str, value: str, subtext: str = "", key: str = None):
    """Renders a custom styled glassmorphism KPI card."""
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            {"<div class='kpi-sub'>" + subtext + "</div>" if subtext else ""}
        </div>
    """, unsafe_allow_html=True)


def render_sidebar_filters(df: pd.DataFrame) -> Tuple[pd.DataFrame, float]:
    """
    Renders the interactive sidebar filters for the shipping analysis:
    - Date Range selector
    - Region / State selector (hierarchical multiselect)
    - Ship Mode filter
    - Lead-time Threshold slider (default 7 days)
    
    Returns:
        Tuple[pd.DataFrame, float]: (Filtered DataFrame, Delay Threshold)
    """
    st.sidebar.markdown("### 🔍 Global Logistics Filters")
    st.sidebar.markdown("---")
    
    # 1. Date Range Filter
    min_date = df["Order Date"].min().date()
    max_date = df["Order Date"].max().date()
    
    date_range = st.sidebar.date_input(
        "📅 Order Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    elif isinstance(date_range, (list, tuple)) and len(date_range) == 1:
        start_date = end_date = date_range[0]
    else:
        start_date = end_date = date_range
        
    # 2. Region / State selectors
    all_regions = sorted(df["Region"].dropna().unique().tolist())
    selected_regions = st.sidebar.multiselect(
        "🌎 Customer Region",
        options=all_regions,
        default=all_regions
    )
    
    # Filter states based on chosen regions
    filtered_states_df = df[df["Region"].isin(selected_regions)] if selected_regions else df
    all_states = sorted(filtered_states_df["State/Province"].dropna().unique().tolist())
    
    selected_states = st.sidebar.multiselect(
        "📍 Customer State",
        options=all_states,
        default=[] # Empty default implies all states in selected regions
    )
    
    # 3. Ship Mode Filter
    all_ship_modes = sorted(df["Ship Mode"].dropna().unique().tolist())
    selected_ship_modes = st.sidebar.multiselect(
        "✈️ Ship Mode",
        options=all_ship_modes,
        default=all_ship_modes
    )
    
    # 4. Lead-time Threshold Slider
    delay_threshold = st.sidebar.slider(
        "⏳ Delay Threshold (Days)",
        min_value=900,
        max_value=1700,
        value=1300,
        step=10
    )
    
    # Filter Execution
    filtered_df = df[
        (df["Order Date"].dt.date >= start_date) &
        (df["Order Date"].dt.date <= end_date)
    ]
    
    if selected_regions:
        filtered_df = filtered_df[filtered_df["Region"].isin(selected_regions)]
        
    if selected_states:
        filtered_df = filtered_df[filtered_df["State/Province"].isin(selected_states)]
        
    if selected_ship_modes:
        filtered_df = filtered_df[filtered_df["Ship Mode"].isin(selected_ship_modes)]
        
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Filtered Records:** `{len(filtered_df):,}` / `{len(df):,}`")
    
    return filtered_df, float(delay_threshold)



def get_excel_download_bytes(df_dict: Dict[str, pd.DataFrame]) -> bytes:
    """Creates a multi-tab Excel spreadsheet download buffer from a dict of dataframes."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for sheet_name, df in df_dict.items():
            clean_sheet = sheet_name[:31] # Excel sheet name length limit
            df.to_excel(writer, sheet_name=clean_sheet, index=False)
    return output.getvalue()
