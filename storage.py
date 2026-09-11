from datetime import datetime

# TODO: finish class 

class Storage:
    def __init__(self, meta_path: str, df_path: str):
        self.meta_path = meta_path
        self.df_path = df_path

        # read meta data

        # read dataframe

    # returns a generator for missing dates
    def missing_dates(self, start_data: datetime, end_date: datetime):
        pass

    # updates the storage, cleans up and updates meta data
    def update_storage(df):
        pass