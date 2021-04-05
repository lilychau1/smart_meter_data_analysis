"""
Pre-processes smart meter dataset. 
- Reduce resolution of consumption
"""

import pandas as pd
import numpy as np
import config

def reduce_resolution(meter_df):

    # Group data by hourly DateTime instead of half-hourly

    # Prepare groupby keys
    keys = [pd.Grouper(freq="1H", key="DateTime")]+ meter_df.columns.drop(["DateTime","Consumption"]).tolist()

    # Group data by hourly DateTime
    meter_df = meter_df.groupby(keys).mean()

    # Reset index to remove multi-index
    meter_df = meter_df.reset_index()

    return meter_df

def save_preprocessed_dataset_pickle(preprocessed_df):
    pickle_file = config.preprossed_data_pickle_path
    preprocessed_df.to_pickle(pickle_file)