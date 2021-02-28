"""
Pre-processes smart meter dataset. 
- Reduce resolution of consumption
- Create time feature
"""

import pandas as pd
import numpy as np
import sklearn

def reduce_resolution(meter_df):

    # Group data by hourly DateTime instead of half-hourly

    # Prepare groupby keys
    keys = [pd.Grouper(freq="1H", key="DateTime")]+ meter_df.columns.drop(["DateTime","Consumption"]).tolist()

    # Group data by hourly DateTime
    meter_df = meter_df.groupby(keys).mean()

    # Reset index to remove multi-index
    meter_df = meter_df.reset_index()

    return meter_df

def create_time_features(meter_df):
    # Create new feature "month"
    meter_df["Month"] = meter_df["DateTime"].dt.month

    # Create new feature "day"
    meter_df["Day"] = meter_df["DateTime"].dt.day

    # Create new feature "weekday"
    meter_df["Weekday"] = meter_df["DateTime"].dt.weekday

    # Create new feature "hour"
    meter_df["Hour"] = meter_df["DateTime"].dt.hour

    return meter_df
