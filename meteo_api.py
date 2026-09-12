from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import functools
import requests
import math
import time

from utils import date_range, clamp, set_time_index

class MeteoAPI:
    def __init__(self, base_url: str, city_code: str, station_code: str):
        self.base_url = base_url
        self.city_code = city_code
        self.station_code = station_code

        self.gather_start = time.time()
        # TODO: might insert cache manager

    def get_observations(self, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        # TODO: check if range is valid, decide what to do if not
        gathered_data = []

        self.gather_start = time.time()
        for date in date_range(start_date, end_date):
            formatted_date = date.strftime("%Y-%m-%d")
            url = f"{self.base_url}/stations/{self.station_code}/observations/{formatted_date}"
            response = self.rate_limit_request(url)

            if response.ok:
                date_df = pd.DataFrame(response.json()["observations"])
                gathered_data.append(date_df)
            else:
                pass
                # TODO: handle other status codes

        df = pd.concat(gathered_data, axis=0)
        df = df.rename(columns={"observationTimeUtc": "timeUtc"})
        df = set_time_index(df)
        return df

    def get_forecasts(self, forecast_type="long-term"):
        url = f"{self.base_url}/places/{self.city_code}/forecasts/{forecast_type}"
        response = self.rate_limit_request(url) 

        if response.ok:
            df = pd.DataFrame(response.json()["forecastTimestamps"])
            df = df.rename(columns={"forecastTimeUtc": "timeUtc"})
            df = set_time_index(df)
            return df
        else:
            pass
            # TODO: handle other status codes


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
            

    





    

