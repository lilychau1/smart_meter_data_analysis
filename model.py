import logging
import sys

import databases, preprocessing, config

# Set up a logging interface to catch warnings
logger = logging.getLogger(__name__)
#set the lowest-severity log message a logger to be handle to be INFO
logger.setLevel(logging.INFO)


if __name__ == "__main__":
    smart_meter_df = databases.MeterDatabase(config.smart_meter_data_path).get_dataframe()
    smart_meter_df_preprocessed = preprocessing.reduce_resolution(smart_meter_df)
    smart_meter_df_preprocessed = preprocessing.create_time_features(smart_meter_df_preprocessed)