"""
- Create time feature
- Create temperature feature from UK temperature dataset
"""

def create_time_features(meter_df):
    # Create new feature "month"
    meter_df["Month"] = meter_df["DateTime"].dt.month

    # Create new feature "day"
    meter_df["Day"] = meter_df["DateTime"].dt.day

    # Create new feature "weekday"
    meter_df["Weekday"] = meter_df["DateTime"].dt.weekday

    # Create new feature "hour"
    meter_df["Hour"] = meter_df["DateTime"].dt.hour

    return meter_df

def create_temp_features(meter_df, temp_df):
    pass
