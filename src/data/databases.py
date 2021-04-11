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
import sys
import datetime

import features
import data

logger = logging.getLogger(__name__)
#set the lowest-severity log message a logger to be handle to be INFO
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

class MeterDatabase:
    def __init__(self, file, sample_size_reduction, reduce_to_proportion):
        logger.info("loading smart meter dataset... "+ datetime.datetime.now().strftime("%H:%M:%S"))

        self.file = file
        pickle_file = config.smart_meter_data_pickle_path

        # Try to load a cached pickle version 
        try: 
            self.df = pd.read_pickle(pickle_file)
            logger.info("ℹ️ Found a pickled version of smart meter database so loading that instead")
        
        except(FileNotFoundError, AttributeError):
            # Read smart meter dataset by chunks due to large file size
            TextFileReader = pd.read_csv(self.file,chunksize=1000000, low_memory= False)
            dfList = []
            for df in TextFileReader:
                dfList.append(df)
            self.df = pd.concat(dfList,sort=False)
        
            logger.info("✔️ smart meter dataset loaded " + datetime.datetime.now().strftime("%H:%M:%S"))
            
            self.reformat_dataframe()

            if sample_size_reduction:
                self.reduce_sample_size(reduce_to_proportion)
            
            logger.info("ℹ️ Saving dataset to pickle file for faster loading")

            # Save dataset csv as pickle for faster loading in the future
            self.df.to_pickle(pickle_file)

    
    def reformat_dataframe(self):
        logger.info("Reformatting smart meter dataset... "+ datetime.datetime.now().strftime("%H:%M:%S"))

        # Rename columns
        self.df = self.df.rename(columns = {"KWH/hh (per half hour) ": "Consumption"})

        columns_to_extract = [
            "LCLid", "DateTime", "Consumption", "Acorn", "Acorn_grouped"
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

    def reduce_sample_size(self, reduce_to_proportion):

        # Store all LCLids
        LCLid_list = self.df.LCLid.unique().tolist()

        # Specify a list of LCLids within the specified proportion to which the size should reduce
        LCLid_to_keep = LCLid_list[:int(len(LCLid_list)*reduce_to_proportion)]

        # Extract from df only entries with the LCLid within the keep list
        self.df = self.df[self.df.LCLid.isin(LCLid_to_keep)]

        logger.info("✔️ smart meter dataframe size reduced " + datetime.datetime.now().strftime("%H:%M:%S"))

    def get_dataframe(self):
        returned_df = self.df.copy()
        return returned_df

class WeatherDatabase:
    def __init__(self, file):
        logger.info("loading weather dataset... "+ datetime.datetime.now().strftime("%H:%M:%S"))
        self.file = file
        pickle_file = config.weather_pickle_path

        # Try to load a cached pickle version 
        try: 
            self.df = pd.read_pickle(pickle_file)
            logger.info("ℹ️ Found a pickled version of smart meter database so loading that instead")
        
        except(FileNotFoundError, AttributeError):         
            # Read weather dataset
            self.df = pd.read_csv(self.file, skiprows = 2)

            logger.info("ℹ️ Saving dataset to pickle file for faster loading")
                    
            self.reformat_dataframe()
            
            # Save dataset csv as pickle for faster loading in the future
            self.df.to_pickle(pickle_file)

            logger.info("✔️ Weather dataset loaded " + datetime.datetime.now().strftime("%H:%M:%S"))

    def reformat_dataframe(self):
            # Convert time variable into datetime type
            self.df.time = pd.to_datetime(self.df.time, format = "%d/%m/%Y %H:%M")
            self.df = self.df.rename(columns = {"time": "DateTime"})
    
    def get_dataframe(self):
        returned_df = self.df.copy()
        return returned_df

class TrainTestDataset:
    def __init__(self, df):
        logger.info("loading smart meter train and test datasets... "+ datetime.datetime.now().strftime("%H:%M:%S"))

        train_pickle_file = config.train_set_pickle_path
        test_pickle_file = config.test_set_pickle_path

        # Try to load a cached pickle version 
        try: 
            self.train_df = pd.read_pickle(train_pickle_file)
            self.test_df = pd.read_pickle(train_pickle_file)            
            logger.info(f"ℹ️ Found a pickled version of smart meter train and test datasets so loading those instead")
        
        except(FileNotFoundError, AttributeError):   
            # If no pickle found, perform train test split
            self.train_df, self.test_df = data.split_train_test_sets.stratified_train_test_split(df)

            logger.info("ℹ️ Saving train and test datasets to pickle files for faster loading")
                        
            # Save dataset csv as pickle for faster loading in the future
            self.train_df.to_pickle(train_pickle_file)
            self.test_df.to_pickle(test_pickle_file)
    
    def get_dataframe(self):
        returned_train_df = self.train_df.copy()
        returned_test_df = self.test_df.copy()
        return returned_train_df, returned_test_df

class PreprocessedDataset:
    def __init__(self, df, create_features = True, transform_data = True):
        logger.info("loading pre-processed smart meter dataset... "+ datetime.datetime.now().strftime("%H:%M:%S"))
        pickle_file = config.preprossed_data_pickle_path

        # Try to load a cached pickle version 
        try: 
            self.df = pd.read_pickle(pickle_file)
            logger.info("ℹ️ Found a pickled version of pre-processed smart meter database so loading that instead")
        
        except(FileNotFoundError, AttributeError):   
            if create_features:
                # create new features if specified
                df = features.create_features(unprocessed_df)
            if transform_data:
                # Perform transformation pipeline if specified
                pass
    
    def get_dataframe(self):
        returned_df = self.df.copy()
        return returned_df

