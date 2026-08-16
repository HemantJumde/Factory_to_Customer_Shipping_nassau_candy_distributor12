"""
Data cleaning and validation module for Nassau Candy Route Efficiency Analysis.
Parses shipping dates, filters invalid/negative lead times, and standardizes geography and factories.
"""

from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np

# Coordinates for all 5 factory locations
FACTORY_COORDINATES = {
    "Lot's O' Nuts": {"lat": 32.881893, "lon": -111.768036, "city": "Casa Grande", "state": "Arizona"},
    "Wicked Choccy's": {"lat": 32.076176, "lon": -81.088371, "city": "Savannah", "state": "Georgia"},
    "Sugar Shack": {"lat": 48.119140, "lon": -96.181150, "city": "Thief River Falls", "state": "Minnesota"},
    "Secret Factory": {"lat": 41.446333, "lon": -90.565487, "city": "Moline", "state": "Illinois"},
    "The Other Factory": {"lat": 35.117500, "lon": -89.971107, "city": "Memphis", "state": "Tennessee"}
}

# New Product-to-Factory mapping
PRODUCT_FACTORY_MAP = {
    # Lot's O' Nuts
    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",
    # Wicked Choccy's
    "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",
    # Sugar Shack
    "Laffy Taffy": "Sugar Shack",
    "Sweetarts": "Sugar Shack",
    "SweeTarts": "Sugar Shack",
    "SweeTARTS": "Sugar Shack",
    "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack",
    "Fizzy Lifting Drinks": "Sugar Shack",
    # Secret Factory
    "Everlasting Gobstopper": "Secret Factory",
    "Lickable Wallpaper": "Secret Factory",
    "Wonka Gum": "Secret Factory",
    # The Other Factory
    "Hair Toffee": "The Other Factory",
    "Kazookles": "The Other Factory"
}


def clean_and_prepare_route_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Validates, cleans, and standardizes dataset specifically for route efficiency.
    
    Business Rules:
    - Parse Order Date and Ship Date as DD-MM-YYYY
    - Remove rows with missing dates or where Ship Date < Order Date (negative lead time)
    - Standardize Product Name and Division (trim, consistent casing)
    - Apply Product-to-Factory mapping and append coordinates
    - Calculate Shipping Lead Time (days)
    - Output cleaning log (rows in, rows removed, rows out)
    """
    df_clean = df.copy()
    rows_in = len(df_clean)
    
    # 1. Standardize text columns (trim & title case)
    string_cols = ["Order ID", "Ship Mode", "Country/Region", "City", "State/Province",
                   "Postal Code", "Division", "Region", "Product ID", "Product Name"]
    for col in string_cols:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(str).str.strip()
            
    if "Product Name" in df_clean.columns:
        df_clean["Product Name"] = df_clean["Product Name"].str.title()
    if "Division" in df_clean.columns:
        df_clean["Division"] = df_clean["Division"].str.title()
        
    # 2. Parse Dates as DD-MM-YYYY
    df_clean["Order Date"] = pd.to_datetime(df_clean["Order Date"], format="%d-%m-%Y", errors="coerce")
    df_clean["Ship Date"] = pd.to_datetime(df_clean["Ship Date"], format="%d-%m-%Y", errors="coerce")
    
    # 3. Handle missing shipment records or invalid date formats
    missing_dates = df_clean["Order Date"].isnull() | df_clean["Ship Date"].isnull()
    rows_missing_dates = int(missing_dates.sum())
    
    # 4. Calculate Shipping Lead Time (days)
    df_clean["Shipping Lead Time"] = (df_clean["Ship Date"] - df_clean["Order Date"]).dt.days
    
    # 5. Remove negative or invalid lead times
    negative_lead_time = df_clean["Shipping Lead Time"] < 0
    rows_negative_lead = int(negative_lead_time.fillna(False).sum())
    
    # Combine removal criteria
    invalid_mask = missing_dates | negative_lead_time | df_clean["Shipping Lead Time"].isnull()
    rows_removed = int(invalid_mask.sum())
    
    # Filter the dataset
    df_clean = df_clean[~invalid_mask].reset_index(drop=True)
    
    # 6. Apply Product-to-Factory mapping
    def assign_factory(prod_name):
        return PRODUCT_FACTORY_MAP.get(prod_name, "The Other Factory")
        
    df_clean["Factory"] = df_clean["Product Name"].apply(assign_factory)
    
    # Map factory coordinates
    df_clean["Factory Lat"] = df_clean["Factory"].apply(lambda f: FACTORY_COORDINATES[f]["lat"])
    df_clean["Factory Lon"] = df_clean["Factory"].apply(lambda f: FACTORY_COORDINATES[f]["lon"])
    df_clean["Factory Location"] = df_clean["Factory"].apply(
        lambda f: f"{FACTORY_COORDINATES[f]['city']}, {FACTORY_COORDINATES[f]['state']}"
    )
    
    # 7. Define routes
    df_clean["Route State"] = df_clean["Factory"] + " → " + df_clean["State/Province"]
    df_clean["Route Region"] = df_clean["Factory"] + " → " + df_clean["Region"]
    
    rows_out = len(df_clean)
    
    # Structured cleaning log
    cleaning_log = {
        "rows_in": rows_in,
        "rows_removed": rows_removed,
        "rows_missing_dates": rows_missing_dates,
        "rows_negative_lead": rows_negative_lead,
        "rows_out": rows_out,
        "date_range": (
            df_clean["Order Date"].min().strftime("%Y-%m-%d") if not df_clean["Order Date"].isnull().all() else "N/A",
            df_clean["Order Date"].max().strftime("%Y-%m-%d") if not df_clean["Order Date"].isnull().all() else "N/A"
        )
    }
    
    return df_clean, cleaning_log
