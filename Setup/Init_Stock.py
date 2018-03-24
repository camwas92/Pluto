# These functions are used to load the required stock values as well as the missing data
import datetime as dt

import pandas as pd
import pandas_datareader.data as web
from pandas_datareader._utils import RemoteDataError

from Classes import Stock as S
from Setup import Constants as Con


# connect to tab
def sheets_download_stock():
    Available_Sheets = Con.sheet_stock.worksheets()
    for x in Available_Sheets[1:]:
        data = x.get_all_values()
        headers = data.pop(0)
        df = pd.DataFrame(data, columns=headers)
        try:
            dfinit = pd.read_csv(Con.paths['Stocks'] / str(x.title[-3:] + '.csv'), parse_dates=[0], dayfirst=True)
            df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
            dfinit['Date'] = pd.to_datetime(dfinit['Date'])
            cols_to_use = list(dfinit.columns.difference(df.columns))
            cols_to_use.append('Date')
            result = pd.merge(df, dfinit[cols_to_use], how='left', on=['Date'])
            df = result
        except FileNotFoundError:
            print('No previous file for', x.title[-3:])
        df.to_csv(str(Con.paths['Stocks'] / str(x.title[-3:] + '.csv')), index=False)

    # format data and save as csv

    return True


def sheets_refresh_stock():
    # add
    Con.print_header_level_2('Refreshing Tabs')
    Con.sheet_stock = Con.client.open(Con.inputfile)
    Available_Sheets = Con.sheet_stock.worksheets()

    for x in Available_Sheets[1:]:
        Con.sheet_stock.del_worksheet(x)

    # Add new tabs
    for x in Con.stock_list:
        Con.sheet_stock.add_worksheet('ASX:' + x, 10000, 6)

    # set formula
    Available_Sheets = Con.sheet_stock.worksheets()
    for x in Available_Sheets:
        x.update_cell(1, 1, Con.stock_request_text)

    action = input('Have you clicked the macro on google drive? ')
    if action == 'Y':
        return True
    else:
        return False


def sheets_load_stock():
    for x in Con.stock_list:
        try:
            df = pd.read_csv(Con.paths['Stocks'] / str(x + '.csv'), parse_dates=[0], dayfirst=True)
            Con.stock_data[x] = S.Stock(x, df)
            print('Loading', x, 'from file')
        except FileNotFoundError:
            print('File for', x, 'not found')
            return False

    return True























# main function called. It will initialise all stocks to be loaded
# True flag loads the newest data, false will use only from the file
def load_stock(flag="Offline"):
    print('Loading all stock')
    Con.stock_list = get_stock_list(True)
    if flag == "Online":
        if sheets_refresh_stock():
            sheets_download_stock()
        sheets_load_stock()
        return
    elif flag == "Offline":
        sheets_load_stock()
        return
    else:

        for x in Con.stock_list:
            # load data for stock
            if load_stock_source(x) and flag:
                # refresh stock if not the newest
                if not Con.stock_data[x].df['Date'].iloc[-1] == Con.now:
                    try:
                        start = dt.datetime.strptime(str(Con.stock_data[x].df['Date'].iloc[-1]), '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        start = dt.datetime.strptime(str(Con.stock_data[x].df['Date'].iloc[-1]), '%Y-%m-%d')
                    download_stock_prices(x, start)
    return


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
