"""
Factory performance & geographic mapping module for Nassau Candy Distributor.
Maps products to production facilities and computes operational metrics and risk exposures.
"""

from typing import Dict, Any
import pandas as pd
import numpy as np


FACTORY_COORDINATES = {
    "Lot's O' Nuts": {"lat": 32.881893, "lon": -111.768036, "city": "Casa Grande", "state": "Arizona"},
    "Wicked Choccy's": {"lat": 32.076176, "lon": -81.088371, "city": "Savannah", "state": "Georgia"},
    "Sugar Shack": {"lat": 48.119140, "lon": -96.181150, "city": "Thief River Falls", "state": "Minnesota"},
    "Secret Factory": {"lat": 41.446333, "lon": -90.565487, "city": "Moline", "state": "Illinois"},
    "The Other Factory": {"lat": 35.117500, "lon": -89.971107, "city": "Memphis", "state": "Tennessee"}
}


def map_product_to_factory(product_id: str) -> str:
    """
    Maps a Product ID to its assigned manufacturing factory facility.
    """
    pid = str(product_id).strip().upper()
    if pid == "CHO-NUT-13000":
        return "Lot's O' Nuts"
    elif pid.startswith("CHO-"):
        return "Wicked Choccy's"
    elif pid.startswith("SUG-"):
        return "Sugar Shack"
    elif pid == "OTH-FIZ-56000":
        return "Secret Factory"
    else:
        return "The Other Factory"


def add_factory_info_to_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Appends Factory name, Latitude, and Longitude to the order-level DataFrame.
    """
    df_copy = df.copy()
    df_copy["Factory"] = df_copy["Product ID"].apply(map_product_to_factory)
    df_copy["Factory Lat"] = df_copy["Factory"].apply(lambda f: FACTORY_COORDINATES[f]["lat"])
    df_copy["Factory Lon"] = df_copy["Factory"].apply(lambda f: FACTORY_COORDINATES[f]["lon"])
    df_copy["Factory Location"] = df_copy["Factory"].apply(
        lambda f: f"{FACTORY_COORDINATES[f]['city']}, {FACTORY_COORDINATES[f]['state']}"
    )
    return df_copy


def analyze_factory_performance(df: pd.DataFrame, risk_df: pd.DataFrame = None) -> pd.DataFrame:
    """
    Aggregates factory-level KPIs: Revenue, Cost, Profit, Margin, Product Count, and High Risk Products.
    """
    if df.empty:
        return pd.DataFrame()
        
    df_factory = add_factory_info_to_df(df)
    
    total_rev = df_factory["Sales"].sum()
    total_prof = df_factory["Gross Profit"].sum()
    
    grouped = df_factory.groupby(["Factory", "Factory Lat", "Factory Lon", "Factory Location"]).agg(
        Revenue=("Sales", "sum"),
        Cost=("Cost", "sum"),
        Gross_Profit=("Gross Profit", "sum"),
        Units=("Units", "sum"),
        Order_Count=("Order ID", "count"),
        Product_Count=("Product ID", "nunique")
    ).reset_index()
    
    grouped["Gross Margin %"] = np.where(
        grouped["Revenue"] > 0,
        (grouped["Gross_Profit"] / grouped["Revenue"]) * 100.0,
        0.0
    )
    grouped["Profit per Unit"] = np.where(
        grouped["Units"] > 0,
        grouped["Gross_Profit"] / grouped["Units"],
        0.0
    )
    grouped["Revenue Contribution %"] = (grouped["Revenue"] / total_rev * 100.0) if total_rev > 0 else 0.0
    grouped["Profit Contribution %"] = (grouped["Gross_Profit"] / total_prof * 100.0) if total_prof > 0 else 0.0
    
    # Calculate high risk products count per factory if risk_df is provided
    if risk_df is not None and not risk_df.empty:
        risk_copy = risk_df.copy()
        risk_copy["Factory"] = risk_copy["Product ID"].apply(map_product_to_factory)
        
        high_risk_counts = risk_copy[risk_copy["Risk Level"].isin(["High Risk", "Critical Risk"])].groupby(
            "Factory"
        )["Product ID"].nunique().reset_index(name="High/Critical Risk Products")
        
        grouped = grouped.merge(high_risk_counts, on="Factory", how="left").fillna({"High/Critical Risk Products": 0})
        grouped["High/Critical Risk Products"] = grouped["High/Critical Risk Products"].astype(int)
    else:
        grouped["High/Critical Risk Products"] = 0
        
    return grouped.sort_values(by="Gross_Profit", ascending=False).reset_index(drop=True)
