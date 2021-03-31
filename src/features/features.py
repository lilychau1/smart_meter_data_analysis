"""
- Create time feature
- Create temperature feature from UK temperature dataset
"""
import logging
import sys
import datetime

# Set up a logging interface to catch warnings
logger = logging.getLogger(__name__)
#set the lowest-severity log message a logger to be handle to be INFO
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

def create_time_features(meter_df):
    # Create new feature "month"
    meter_df["Month"] = meter_df["DateTime"].dt.month

    # Create new feature "day"
    meter_df["Day"] = meter_df["DateTime"].dt.day

    # Create new feature "weekday"
    meter_df["Weekday"] = meter_df["DateTime"].dt.weekday

    # Create new feature "hour"
    meter_df["Hour"] = meter_df["DateTime"].dt.hour
    
    logger.info("✔️ Time features created " + datetime.datetime.now().strftime("%H:%M:%S"))

    return meter_df

def create_weather_features(meter_df, temp_df):

    # Create weather features including temperature, precipitation, irradiance, snowfall, snow mass, cloud cover and air density
    meter_df = meter_df.merge(temp_df, on = "DateTime")
    
    logger.info("✔️ Weather features created " + datetime.datetime.now().strftime("%H:%M:%S"))

    return meter_df
