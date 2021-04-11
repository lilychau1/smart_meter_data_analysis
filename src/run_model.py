import logging
import sys
import datetime

from data import databases, preprocessing, split_train_test_sets
from features import features
import config

# Set up a logging interface to catch warnings
logger = logging.getLogger(__name__)
#set the lowest-severity log message a logger to be handle to be INFO
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

if __name__ == "__main__":
    # Load smart meter database
    smart_meter_df = databases.MeterDatabase(config.smart_meter_data_path, sample_size_reduction = True, reduce_to_proportion = 0.001).get_dataframe()
    # Load weather database
    weather_df = databases.WeatherDatabase(config.weather_data_path).get_dataframe()

    # Load or create train and test sets
    smart_meter_train, smart_meter_test = databases.TrainTestDataset(smart_meter_df).get_dataframe()

    # Try to load pickled pre-processed dataset, if any
    smart_meter_df_preprocessed = databases.PreprocessedDataset(smart_meter_df_train).get_dataframe()

    # Save preprocessed database as a pickle file for analysis convenience
    preprocessing.save_preprocessed_dataset_pickle(smart_meter_df_preprocessed)

    breakpoint()
