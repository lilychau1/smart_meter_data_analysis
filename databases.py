"""
Reads the smart meter database excel file and returns a dataframe containing all the relevant data
"""

import os
import tarfile
import urllib
import logging
import pandas as pd
import numpy as np
import sklearn
import datetime
import pickle
import hashlib
import binascii
import config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class MeterDatabase:
    def __init__(self, file):
        self.file = file
        pickle_file = config.smart_meter_data_pickle_path

        # Try to load a cached pickle version 
        try: 
            self.df = pd.read_pickle(pickle_file)
            logger.debug("ℹ️ Found a pickled version of smart meter database so loading that instead")
        
        except(FileNotFoundError, AttributeError):
            # Read smart meter dataset by chunks due to large file size
            TextFileReader = pd.read_csv(self.file,chunksize=1000000, low_memory= False)
            dfList = []
            for df in TextFileReader:
                dfList.append(df)
            self.df = pd.concat(dfList,sort=False)
            logger.debug("ℹ️ Saving dataset to pickle file for faster loading")
        
            logger.info("✔️ smart meter dataset loaded " + datetime.datetime.now().strftime("%H:%M:%S"))
            
            self.reformat_dataframe()
            
            # Save dataset csv as pickle for faster loading in the future
            self.df.to_pickle(pickle_file)

    
    def reformat_dataframe(self):
        logger.info("Reformatting smart meter dataset... "+ datetime.datetime.now().strftime("%H:%M:%S"))

        # Rename columns
        self.df = self.df.rename(columns = {"KWH/hh (per half hour) ": "Consumption", "Unnamed: 0": "id"})

        columns_to_extract = [
            "id", "DateTime", "Consumption", "Acorn", "Acorn_grouped"
        ]

        # Extract necessary columns
        self.df = self.df.filter (columns_to_extract)

        # Warn 
        columns_not_in_df = [
           column for column in columns_to_extract if column not in self.df.columns.tolist()
        ]

        if len(columns_not_in_df)>0:
            logger.warning("⚠️ These columns are not in the smart meter database: {0}".format(", ".join(columns_not_in_df)))

        # Convert DateTime to datetime format
        self.df["DateTime"] = pd.to_datetime(self.df["DateTime"], format = "%Y-%m-%d %H:%M:%S.%f")

        # Convert Consumption to float format
        self.df["Consumption"] = pd.to_numeric(
            self.df["Consumption"],errors='coerce'
            )

        logger.info("✔️ smart meter dataframe reformatted " + datetime.datetime.now().strftime("%H:%M:%S"))

    def get_dataframe(self):
        returned_df = self.df.copy()
        return returned_df

class TemperatureDatabase:
    def __init__(self, file):
            self.file = file
            # Read temperature dataset
            self.df = pd.read_csv(self.file, skiprows = 2)
            logger.info("✔️ temperature dataset loaded")

            self.reformat_dataframe()

    def reformat_dataframe(self):
            # Convert time variable into datetime type
            self.df.time = pd.to_datetime(self.df.time, format = "%d/%m/%Y %H:%M")
    
    def get_dataframe(self):
        returned_df = self.df.copy()
        return returned_df
