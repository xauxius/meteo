from datetime import datetime, timedelta
import pandas as pd

def date_range(start_date: datetime, end_date: datetime):
        current_date = start_date
        while current_date <= end_date:
            yield current_date
            current_date += timedelta(days=1)

def clamp(value: float, low: float, high: float):
      return max(low, min(value, high))

def set_time_index(df: pd.DataFrame, time_col: str = "timeUtc"):
    df[time_col] = pd.to_datetime(df[time_col], utc=True)
    return df.set_index(time_col)