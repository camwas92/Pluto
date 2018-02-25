# These functions are used to load the required stock values as well as the missing data
import datetime as dt

import pandas as pd
import pandas_datareader.data as web
from pandas_datareader._utils import RemoteDataError

from Classes import Stock as S
from Setup import Constants as Con


# TODO Fix up inputs to be accurate
# TODO prevent duplicate data
# TODO make all gaps filled by last value
# main function called. It will initialise all stocks to be loaded
# True flag loads the newest data, false will use only from the file
def load_stock(flag = False):
    print('Loading all stock')

    Con.stock_list = get_stock_list(True)
    for x in Con.stock_list:
        # load data for stock
        if load_stock_source(x) and flag:
        # refresh stock if not the newest
            if not Con.stock_data[x].df['Date'].iloc[-1] == Con.now:
                try:
                    start = dt.datetime.strptime(str(Con.stock_data[x].df['Date'].iloc[-1]),'%Y-%m-%d %H:%M:%S')
                except ValueError:
                    start = dt.datetime.strptime(str(Con.stock_data[x].df['Date'].iloc[-1]), '%Y-%m-%d')
                download_stock_prices(x,start)


# gets list of stocks to be loaded for this simulation
# True returns the list of stocks, false returns the details on the stock
def get_stock_list(flag):
    print('Retreiving Stock List')
    xl = pd.ExcelFile(Con.paths['Input'] / 'StockList.xlsx')
    sheets = xl.sheet_names
    sheet_name = [s for s in sheets if Con.stocks_for_simulation in s]
    temp = xl.parse(sheet_name[0])
    return list(temp['Code'])

# check if a file for stock
def load_stock_source(stock):
    try:
        df = pd.read_csv(Con.paths['Stocks'] / str(stock+'.csv'))
        Con.stock_data[stock] = S.Stock(stock, df)
        print('Loading',stock,'from file')
    except FileNotFoundError:
        print('File for',stock,'not found, downloading new data')
        download_stock_prices(stock)
        return False

    return True


# get the missing data
def download_stock_prices(stock,start = dt.datetime(1980, 1, 1)):
    start = start + dt.timedelta(days=1)
    try:
        df = web.DataReader(stock, 'morningstar', start, Con.now)
    except RemoteDataError:
        print(stock, 'could not be downloaded')
        return False
    df.reset_index(inplace=True)
    if start != dt.datetime(1980, 1, 2):
        df = pd.concat([Con.stock_data[stock].df,df])
    Con.stock_data[stock] = S.Stock(stock,df)
    df.to_csv(str(Con.paths['Stocks'] / str(stock+'.csv')),index=False)
    print('Downloaded',stock)
    return True
