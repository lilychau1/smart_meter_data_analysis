"""
Pre-processes smart meter dataset. 
- Reduce resolution of consumption
"""
import logging
import sys
import datetime

import pandas as pd
import numpy as np
import config

# Set up a logging interface to catch warnings
logger = logging.getLogger(__name__)
#set the lowest-severity log message a logger to be handle to be INFO
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

def reduce_resolution(meter_df):

    # Group data by hourly DateTime instead of half-hourly

    # Prepare groupby keys
    keys = [pd.Grouper(freq="1H", key="DateTime")]+ meter_df.columns.drop(["DateTime","Consumption"]).tolist()

    # Group data by hourly DateTime
    meter_df = meter_df.groupby(keys).mean()

    # Reset index to remove multi-index
    meter_df = meter_df.reset_index()

    logger.info("✔️ Time resolution reduced to hourly " + datetime.datetime.now().strftime("%H:%M:%S"))

    return meter_df

def save_preprocessed_dataset_pickle(preprocessed_df):
    pickle_file = config.preprossed_data_pickle_path
    preprocessed_df.to_pickle(pickle_file)
    logger.info("✔️ Pre-processed smart meter dataset saved as pickle " + datetime.datetime.now().strftime("%H:%M:%S"))

