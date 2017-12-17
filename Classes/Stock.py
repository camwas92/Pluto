import pandas as pd
import datetime as dt

class Stock:
    name = ''
    df = ''
    start_date = None
    end_date = None

    def __init__(self, name, data):
        data['Date']=pd.to_datetime((data['Date']))
        self.name = name
        self.df = data
        self.start_date = min(data['Date'])
        self.end_date = max(data['Date'])

