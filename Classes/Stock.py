# stores the associated data with a stock, as loaded from the source provider
import numpy as np
import pandas as pd


class Stock:
    name = ''
    df = ''
    start_date = None
    end_date = None

    def __init__(self, name, data):
        data['Date']=pd.to_datetime((data['Date']))
        self.name = name

        # clean and prepare stocks
        # ensure all 0s are nans
        data = data.replace([0], np.nan)
        # remove all duplicates
        data = data.drop_duplicates(keep=False)
        # any blanks will with the value from before
        self.df = data.fillna(method='ffill')

        self.start_date = min(data['Date'])
        self.end_date = max(data['Date'])

