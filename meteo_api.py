from datetime import datetime
import pandas as pd
import requests
import time

from utils import date_range, clamp, prepare_df, warn_about_error
from constants import Col

class MeteoAPI:
    def __init__(self, base_url: str, city_code: str, station_code: str):
        self.base_url = base_url
        self.city_code = city_code
        self.station_code = station_code

        self.gather_start = time.time()
        # TODO: might insert cache manager

    def get_observations(self, start_date: datetime, end_date: datetime = None, station_code: str = None) -> pd.DataFrame:
        if end_date < start_date:
            raise Exception("End date can't be smaller than start date")

        if end_date is None:
            end_date = start_date

        if station_code is None:
            station_code = self.station_code 

        gathered_data = []

        self.gather_start = time.time()
        for date in date_range(start_date, end_date):
            formatted_date = date.strftime("%Y-%m-%d")
            url = f"{self.base_url}/stations/{station_code}/observations/{formatted_date}"
            response = self.rate_limit_request(url)

            if response.ok:
                date_df = pd.DataFrame(response.json()["observations"])
                gathered_data.append(date_df)
            else:
                print(f"Error fetching {date.strftime("%Y-%m-%d")}. Status code: {response.status_code}. Response:")
                print(response.json())

        df = pd.concat(gathered_data, axis=0)
        df = df.rename(columns={"observationTimeUtc": Col.TIME_UTC})
        
        return prepare_df(df)

    def get_forecasts(self, city_code: str = None, forecast_type: str = "long-term"):
        if city_code is None:
            city_code = self.city_code

        url = f"{self.base_url}/places/{city_code}/forecasts/{forecast_type}"
        response = self.rate_limit_request(url) 

        if response.ok:
            df = pd.DataFrame(response.json()["forecastTimestamps"])
            df = df.rename(columns={"forecastTimeUtc": Col.TIME_UTC})
            return prepare_df(df)
        else:
            print(f"Error fetching forecasts. Status code: {response.status_code}. Response:")
            print(response.json())
            

    def rate_limit_request(self, url: str, max_retries: int = 6, wait_time: int = 2):
        response = requests.get(url)

        if response.status_code != 429:
            return response

        time_until_reset = time.time() - self.gather_start
        time.sleep(clamp(time_until_reset, 0, 60))

        for _ in range(max_retries):
            response = requests.get(url)

            if response.status_code != 429:
                self.gather_start = time.time()
                return response

            time.sleep(wait_time)
            wait_time *= 2

        return response

    

            

    





    

