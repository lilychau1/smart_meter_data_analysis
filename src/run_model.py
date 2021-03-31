import logging
import sys
import datetime

from data import databases, preprocessing
from features import features
import config

# Set up a logging interface to catch warnings
logger = logging.getLogger(__name__)
#set the lowest-severity log message a logger to be handle to be INFO
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

if __name__ == "__main__":
    smart_meter_df = databases.MeterDatabase(config.smart_meter_data_path, sample_size_reduction = True, reduce_to_proportion = 0.33).get_dataframe()
    temp_df = databases.TemperatureDatabase(config.temperature_data_path).get_dataframe()
    smart_meter_df_preprocessed = features.create_time_features(smart_meter_df)
    smart_meter_df_preprocessed = features.create_weather_features(smart_meter_df_preprocessed, temp_df)
