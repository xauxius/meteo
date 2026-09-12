from datetime import datetime, timedelta
import pandas as pd

from constants import Col, LOCAL_TIMEZONE

def date_range(start_date: datetime, end_date: datetime):
	current_date = start_date
	while current_date <= end_date:
		yield current_date
		current_date += timedelta(days=1)

def clamp(value: float, low: float, high: float):
	return max(low, min(value, high))

def prepare_df(df: pd.DataFrame):
	df[Col.AIR_TEMPERATURE] = df[Col.AIR_TEMPERATURE].astype("Float64")
	if Col.PRECIPITATION in df.columns:
		df[Col.PRECIPITATION] = df[Col.PRECIPITATION].astype("Float64")
	df[Col.RELATIVE_HUMIDITY] = df[Col.RELATIVE_HUMIDITY].astype('Int64')

	df[Col.TIME_UTC] = pd.to_datetime(df[Col.TIME_UTC], utc=True)
	df[Col.TIME_LOCAL] = df[Col.TIME_UTC].dt.tz_convert(LOCAL_TIMEZONE)
	df = df.set_index(Col.TIME_UTC)

	return df