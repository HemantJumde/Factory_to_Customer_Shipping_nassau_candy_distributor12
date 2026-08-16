"""
Route analysis and performance aggregation module for Nassau Candy Route Efficiency Analysis.
Computes route-level statistics, delay frequencies, and normalized efficiency scores.
"""

from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np


def aggregate_route_performance(df: pd.DataFrame, delay_threshold: float = 7.0) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Aggregates shipping records by route (State-level and Region-level).
    
    Each route computes:
    - Total shipments (Route Volume)
    - Average shipping lead time
    - Lead time variability (standard deviation)
    - Delay frequency (% of shipments exceeding threshold)
    - Route Efficiency Score (normalized 0-100 where shorter lead time = higher score)
    
    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: (State-level Route DF, Region-level Route DF)
    """
    if df.empty:
        return pd.DataFrame(), pd.DataFrame()
        
    # Helper to aggregate at a specific route level
    def aggregate_level(group_col, route_name_col):
        grouped = df.groupby([group_col, "Factory", route_name_col]).agg(
            Shipments=("Order ID", "count"),
            Avg_Lead_Time=("Shipping Lead Time", "mean"),
            Std_Lead_Time=("Shipping Lead Time", "std"),
            Delays=("Shipping Lead Time", lambda x: (x > delay_threshold).sum()),
            Sales=("Sales", "sum"),
            Units=("Units", "sum")
        ).reset_index()
        
        # Handle cases where std is NaN (e.g. only 1 shipment on the route)
        grouped["Std_Lead_Time"] = grouped["Std_Lead_Time"].fillna(0.0)
        
        # Calculate delay frequency
        grouped["Delay Frequency %"] = np.where(
            grouped["Shipments"] > 0,
            (grouped["Delays"] / grouped["Shipments"]) * 100.0,
            0.0
        )
        
        # Calculate Route Efficiency Score (0 to 100)
        # Normalized: 100 = fastest average route, 0 = slowest average route
        avg_lt = grouped["Avg_Lead_Time"]
        min_lt = avg_lt.min()
        max_lt = avg_lt.max()
        
        if max_lt == min_lt:
            grouped["Route Efficiency Score"] = 100.0
        else:
            grouped["Route Efficiency Score"] = 100.0 * (1.0 - (avg_lt - min_lt) / (max_lt - min_lt))
            
        # Round columns for clean display
        grouped["Avg_Lead_Time"] = grouped["Avg_Lead_Time"].round(2)
        grouped["Std_Lead_Time"] = grouped["Std_Lead_Time"].round(2)
        grouped["Delay Frequency %"] = grouped["Delay Frequency %"].round(2)
        grouped["Route Efficiency Score"] = grouped["Route Efficiency Score"].round(2)
        
        return grouped
        
    state_routes = aggregate_level("Route State", "State/Province")
    region_routes = aggregate_level("Route Region", "Region")
    
    # Sort by Efficiency Score descending
    state_routes = state_routes.sort_values(by="Route Efficiency Score", ascending=False).reset_index(drop=True)
    region_routes = region_routes.sort_values(by="Route Efficiency Score", ascending=False).reset_index(drop=True)
    
    return state_routes, region_routes


def get_route_leaderboards(route_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Extracts the Top 10 most efficient and Bottom 10 least efficient routes.
    """
    if route_df.empty:
        return pd.DataFrame(), pd.DataFrame()
        
    # Sort descending for top efficient routes
    top_efficient = route_df.sort_values(by="Route Efficiency Score", ascending=False).head(10).reset_index(drop=True)
    # Sort ascending for least efficient routes
    least_efficient = route_df.sort_values(by="Route Efficiency Score", ascending=True).head(10).reset_index(drop=True)
    
    return top_efficient, least_efficient


def detect_bottlenecks(df: pd.DataFrame, state_route_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Identifies geographic bottlenecks using two criteria:
    1. Congestion-prone Routes: High shipment volume + poor lead time (above median lead time).
    2. Region/State Bottlenecks: Areas with high delay frequencies.
    """
    if state_route_df.empty:
        return pd.DataFrame(), pd.DataFrame()
        
    median_volume = state_route_df["Shipments"].median()
    median_lead_time = state_route_df["Avg_Lead_Time"].median()
    
    # Congestion filter: Volume >= Median Volume AND Lead Time >= Median Lead Time
    congestion_df = state_route_df[
        (state_route_df["Shipments"] >= median_volume) &
        (state_route_df["Avg_Lead_Time"] >= median_lead_time)
    ].sort_values(by="Avg_Lead_Time", ascending=False).reset_index(drop=True)
    
    # High-delay routes: Delay Frequency % > 50%
    delay_df = state_route_df[state_route_df["Delay Frequency %"] > 50.0].sort_values(
        by="Delay Frequency %", ascending=False
    ).reset_index(drop=True)
    
    return congestion_df, delay_df
