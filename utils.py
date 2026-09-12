from datetime import datetime, timedelta
import pandas as pd
import requests

from constants import Col, LOCAL_TIMEZONE

def date_range(start_date: datetime, end_date: datetime):
        current_date = start_date
        while current_date <= end_date:
            yield current_date
            current_date += timedelta(days=1)

def clamp(value: float, low: float, high: float):
      return max(low, min(value, high))

def prepare_df(df: pd.DataFrame):
        df[Col.TIME_UTC] = pd.to_datetime(df[Col.TIME_UTC], utc=True)
        df[Col.TIME_LOCAL] = df[Col.TIME_UTC].dt.tz_convert(LOCAL_TIMEZONE)
        df = df.set_index(Col.TIME_UTC)

        return df