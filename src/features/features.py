"""
- Create time feature
- Create weather features from UK weather dataset
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
    # Create new feature "season"
    meter_df = create_season_feature(meter_df)

    # Create new feature "Day_type"
    meter_df = create_day_type_feature(meter_df)

    # Create new feature "time_slot"
    meter_df = create_time_slot_feature(meter_df)
  
    logger.info("✔️ Time features created " + datetime.datetime.now().strftime("%H:%M:%S"))

    return meter_df

def create_season_feature(df):
    # Create a series date contining a numerical representation of the day of DateTime (e.g. the start date of spring, 21 of March = 321)
    date = df.DateTime.dt.month*100 + df.DateTime.dt.day

    # Assign season feature by putting date value into bins
    # Since pd.cut only takes unique bin labels and winter months is across the end and the beginning of the year, added a space  after "Winter" and strip() afterwards

    df['Season'] = pd.cut(date,[0,321,620,922,1220,1300],
                       labels=["Winter","Spring","Summer","Autumn","Winter "]).str.strip()
    return df

def create_day_type_feature(df):
    # Group days of week into (later to improve to include specific bank holidays from the UK 2013 calendar)
    
    # Assign day_type feature by putting day of week value into bins

    df["Day_type"] = pd.cut(df["DateTime"].dt.weekday,[-1,4,5, 6],
                       labels=["Weekday","Day before holiday","Holiday"])
    
    holiday_list = [datetime.datetime(2013, 1, 1), 
                   datetime.datetime(2013, 3, 29), 
                   datetime.datetime(2013, 4, 1), 
                   datetime.datetime(2013, 5, 6), 
                   datetime.datetime(2013, 8, 26), 
                   datetime.datetime(2013, 12, 25), 
                   datetime.datetime(2013, 12, 26)]
    
    day_before_holiday_list = [datetime.datetime(2013, 3, 28),
                              datetime.datetime(2013, 12, 24)]
    
    # Specific bank holidays from the UK 2013 calendar
    df.loc[df["DateTime"].isin(holiday_list), "Day_type"] = "Holiday"
    df.loc[df["DateTime"].isin(day_before_holiday_list), "Day_type"] = "Day before holiday"
    

    return df

def create_time_slot_feature(df):
    # Assign season feature by putting hours in a day into time slot bins (Midnight, early morning, morning, early afternoon, late afternoon, early evening, late evening)
    # Since pd.cut only takes unique bin labels and winter months is across the end and the beginning of the year, added a space  after "Winter" and strip() afterwards

    df["Time_slot"] = pd.cut(df["DateTime"].dt.hour,[-1,3, 6, 11, 14, 17, 20, 23],
                       labels=["Midnight", 
                               "Early morning", 
                               "Morning", 
                               "Early afternoon", 
                               "Late afternoon", 
                               "Early evening", 
                               "Late evening"])
    return df

def create_weather_features(meter_df, weather_df):

    # Create weather features including temperature, precipitation, irradiance, snowfall, snow mass, cloud cover and air density
    meter_df = meter_df.merge(weather_df, on = "DateTime")
    
    logger.info("✔️ Weather features created " + datetime.datetime.now().strftime("%H:%M:%S"))

    return meter_df
