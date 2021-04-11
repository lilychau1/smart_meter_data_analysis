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

from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

# Set up a logging interface to catch warnings
logger = logging.getLogger(__name__)
#set the lowest-severity log message a logger to be handle to be INFO
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

def reduce_resolution(meter_df):

    # Group data by hourly DateTime instead of half-hourly
    logger.info("Reducing smart meter DateTime resolution... "+ datetime.datetime.now().strftime("%H:%M:%S"))

    # Prepare groupby keys
    keys = [pd.Grouper(freq="1H", key="DateTime")]+ meter_df.columns.drop(["DateTime","Consumption"]).tolist()
    
    # Group data by hourly DateTime
    meter_df = meter_df.groupby(keys).mean()

    # Reset index to remove multi-index
    meter_df = meter_df.reset_index()

    logger.info("✔️ Time resolution reduced to hourly " + datetime.datetime.now().strftime("%H:%M:%S"))

    return meter_df

def transform_data(meter_df):
    # Create a data transformation pipeline to transform the dataset
    columns_to_drop = ["LCLid", "DateTime", "Consumption"]
    meter_df = meter_df.drop(columns = columns_to_drop)
    
    # Extract categorical columns from smart meter database
    cat_attribs = ["Acorn_grouped", "Season", "Day_type", "Time_slot", "stdorToU"]
    meter_df_cat = meter_df[cat_attribs]

    # Extract numerical columns from smart meter database
    meter_df_num = meter_df.drop(columns = cat_attribs)
    # create num_attribs as a list of numerical attributes for transformation
    num_attribs = list(meter_df_num)
    
    # Create pipelines respectively for categorical and numerical data transformation
    # Transform categorical data - one hot encoding
    # Transform numerical data - imputation, feature scaling

    # Create transformation pipeline for numerical columns
    num_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy = "median")),  
        ("std_scaler", StandardScaler()),
        ])

    # Create full pipeline of data transformation
    full_pipeline = ColumnTransformer([
        ("num", num_pipeline, num_attribs), 
        ("cat", OneHotEncoder(), cat_attribs), 
        ])
    
    meter_transformed = full_pipeline.fit_transform(meter_df)

    return meter_transformed
  

