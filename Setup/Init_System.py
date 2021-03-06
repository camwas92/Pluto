# called at the beginning of the program to start a simulation and build all required foundations
import datetime as dt
import logging
from pathlib import Path

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from Setup import Constants as Con
from Setup import Init_Stock as IS


# collect paths and load data
def init_system():
    Con.paths = collect_paths()
    connect_google_sheets()
    Con.now = get_date()
    IS.load_stock(Con.line)  # true load new stock data, false load only from file
    # "Online" loads data from sheets, "Offline" loads data from source
    create_logging_file()
    return


# collect paths
def collect_paths():
    input_1 = Path(__file__).parents[1]
    basePath = Path(__file__).parents[2]  # get base path
    paths = {'Base': basePath, 'Input': (input_1 / 'Input'), 'Output': (basePath / 'Output')}
    data = Path(__file__).parents[3]
    paths['Stocks'] = paths['Input'] / 'Stocks'
    paths['Storage'] = paths['Input'] / 'Storage'
    return paths


def create_logging_file():
    logging.basicConfig(filename=str(Con.paths['Output'] / 'Pluto.log'),
                        level=logging.DEBUG,
                        format='%(asctime)s %(message)s',
                        filemode='w')
    logging.info('Pluto Initiated')

# get most recent date
def get_date():
    now = dt.datetime.now()
    return(dt.datetime(now.year, now.month, now.day))


# connect and prepare google sheets
def connect_google_sheets():
    Con.creds = ServiceAccountCredentials.from_json_keyfile_name(Con.paths['Storage'] / str('client_secret.json'),
                                                                 Con.scope)
    # connect
    Con.client = gspread.authorize(Con.creds)

    # get work sheets
    Con.sheet_sim = Con.client.open(Con.outputfile).get_worksheet(0)
    Con.sheet_model = Con.client.open(Con.outputfile).get_worksheet(1)
    Con.sheet_trade = Con.client.open(Con.outputfile).get_worksheet(2)

    # establish shseets and prepare
    Con.row_count_sim = Con.sheet_sim.row_count
    Con.column_count_sim = Con.sheet_sim.col_count

    Con.row_count_model = Con.sheet_model.row_count
    Con.column_count_model = Con.sheet_model.col_count

    Con.row_count_trade = Con.sheet_trade.row_count
    Con.column_count_trade = Con.sheet_trade.col_count

    if Con.row_count_sim < 1:
        print("\n\nOUTPUT IS NOT CONNECTED\n\n")
    else:
        print("\n\nOutput file is connected\n\n")
        return
