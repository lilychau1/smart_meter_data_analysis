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
    # Load smart meter database
    smart_meter_df = databases.MeterDatabase(config.smart_meter_data_path, sample_size_reduction = True, reduce_to_proportion = 0.33).get_dataframe()
    # Load weather database
    weather_df = databases.WeatherDatabase(config.weather_data_path).get_dataframe()

    # Add time features (e.g.: month, weekday, hour)
    smart_meter_df_processed = features.create_time_features(smart_meter_df)

    # Add weather features (e.g.: temperature, precipitation, snowfall)
    smart_meter_df_processed = features.create_weather_features(smart_meter_df_processed, weather_df)

    # Save processed database as a pickle file for analysis convenience
    preprocessing.save_processed_dataset_pickle(smart_meter_df_processed)
