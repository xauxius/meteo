from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import requests

class MeteoAPI:
    def __init__(self, base_url: str, city_code: str, station_code: str, requests_per_min=180):
        self.base_url = base_url
        self.city_code = city_code
        self.station_code = station_code
        self.requests_per_min = requests_per_min
        # TODO: might insert cache manager

    def get_observations(self, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        # TODO: check if range is valid, decide what to do if not
        gathered_data = []

        current_date = start_date
        # TODO: rate limitter, robust status handling and more(?)
        while current_date <= end_date:
            date_df = self.get_observation(current_date)
            gathered_data.append(date_df)
            current_date += timedelta(days=1)

        # TODO: set time as DatetimeIndex
        combined_df = pd.concat(gathered_data, axis=0)
        return combined_df

    def get_observation(self, date: datetime) -> pd.DataFrame:
        formatted_date = date.strftime("%Y-%m-%d")
        response = requests.get(f"{self.base_url}/stations/{self.station_code}/observations/{formatted_date}")

        if response.ok:
            return pd.DataFrame(response.json()["observations"])
            
        # TODO: check if reached rate limit

    def get_forecasts(self, forecast_type="long-term"):
        # TODO: rate limitter (might be blocked from earlier fetching) and status code handle
        response = requests.get(f"{self.base_url}/places/{self.city_code}/forecasts/{forecast_type}")

        if response.ok:
            return pd.DataFrame(response.json()["forecastTimestamps"])


    

