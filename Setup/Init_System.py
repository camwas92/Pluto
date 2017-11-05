from pathlib import Path
from Setup import Constants as Con
import datetime as dt

def init_system():
    Con.paths = collect_paths()
    Con.now = get_date()
    return


def collect_paths():
    basePath = Path(__file__).parents[2]  # get base path
    paths = {'Base': basePath, 'Input': (basePath / 'Input'), 'Output': (basePath / 'Output')}
    data = Path(__file__).parents[3]
    paths['Stocks'] = paths['Input'] / 'Stocks'
    return paths

def get_date():
    now = dt.datetime.now()
    return(dt.datetime(now.year, now.month, now.day))
