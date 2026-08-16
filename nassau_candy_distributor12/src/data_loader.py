"""
Data loader module for Nassau Candy Distributor dataset.
Handles loading raw data with robust path resolution and fallback mechanisms.
"""

import os
import pandas as pd


def get_default_data_path() -> str:
    """Returns the default path for the Nassau Candy CSV dataset."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    local_path = os.path.join(base_dir, "data", "nassau_candy.csv")
    if os.path.exists(local_path):
        return local_path
    
    # Fallback to Downloads folder if local project file is missing
    downloads_path = os.path.expanduser(r"~\Downloads\Nassau Candy Distributor.csv")
    if os.path.exists(downloads_path):
        return downloads_path
        
    raise FileNotFoundError("Nassau Candy Distributor dataset not found in data/ or Downloads.")


def load_raw_data(filepath: str = None) -> pd.DataFrame:
    """
    Loads raw CSV data into a pandas DataFrame.
    
    Parameters:
        filepath (str, optional): Custom path to CSV file. Defaults to standard path.
        
    Returns:
        pd.DataFrame: Raw dataset.
    """
    if filepath is None:
        filepath = get_default_data_path()
        
    df = pd.read_csv(filepath, encoding="utf-8-sig")
    return df
