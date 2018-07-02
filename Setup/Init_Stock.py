# These functions are used to load the required stock values as well as the missing data
import datetime as dt
import time

import pandas as pd

from Classes import Stock as S
from Setup import Constants as Con
from Setup import Init_System as IS


#########################################
#                                       #
#    ###############################    #
#    # NEW METHOD FOR LOADING DATA #    #
#    ###############################    #
#                                       #
#########################################

# connect to google sheets source and download data once formated
def sheets_download_stock():
    Con.print_header_level_2('Downloading Drive Tabs')
    Con.sheet_stock = Con.client.open(Con.inputfile)
    Available_Sheets = Con.sheet_stock.worksheets()
    Con.print_header_level_1('Downloading...')
    for x in Available_Sheets[1:]:
        Con.print_header_level_2(x.title[-3:])
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

    return True


# create all google drive sheets and replace the content
def sheets_refresh_stock():
    # add

    skip = False
    skip_to = ''
    placeholder_stock_list = Con.stock_list
    chunked_stock_list = list(chunks(Con.stock_list, Con.num_to_load))
    count = 0
    for Con.stock_list in chunked_stock_list:
        if skip:
            if skip_to in Con.stock_list:
                skip = False
                print('Skipping', Con.stock_list)
                print('Ending Skipping')
            else:
                print('Skipping', Con.stock_list)
        else:
            Con.print_header_level_2('Refreshing Tabs')
            Con.sheet_stock = Con.client.open(Con.inputfile)

            Con.print_header_level_1('Preparing sheets...')
            Con.print_header_level_2(Con.stock_list)

            # delete sheets
            Available_Sheets = Con.sheet_stock.worksheets()
            for x in Available_Sheets[1:]:
                Con.sheet_stock.del_worksheet(x)

            # Add new tabs
            for x in Con.stock_list:
                Con.sheet_stock.add_worksheet('ASX:' + x, 5000, 6)

            # set formula
            Available_Sheets = Con.sheet_stock.worksheets()
            for x in Available_Sheets:
                x.update_cell(1, 1, Con.stock_request_text)

            # run macro
            Available_Sheets[0].update_cell(6, 6, 'Run')
            check = Available_Sheets[0].cell(6, 6).value
            wait_length = 10
            waited = 0
            while check != 'Was Run':
                time.sleep(wait_length)
                waited += 10
                print('waited {0:2d}s for macro'.format(waited))
                check = Available_Sheets[0].cell(6, 6).value
            sheets_download_stock()
            count += 1
            if count > 10:
                IS.connect_google_sheets()
                count = 0
        # old method
        # while ctypes.windll.user32.MessageBoxW(0, "Have you run the macro", "Macro Check", 4) != 6:
        #    print('Please run the macro')
        # sheets_download_stock()

    Con.stock_list = placeholder_stock_list
    return


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def test_stock_columns():
    lenths = []
    stock_and_length = {}
    for key in Con.stock_data:
        temp = len(Con.stock_data[key].df.columns)
        lenths.append(temp)
        stock_and_length[key] = temp
    Con.num_columns = list(set(lenths))[0]
    check = len(set(lenths)) == 1
    if not check:
        print(stock_and_length)
        raise TypeError('There are different number of columns in the dfs {0}'.format(set(lenths)))
    else:
        Con.columns_used = list(Con.stock_data[next(iter(Con.stock_data))].df.columns)
        Con.columns_used.remove('Date')
    return



# load all data from file
def sheets_load_stock():
    no_data = []
    for x in Con.stock_list:
        try:
            print('Loading', x, 'from file')
            df = pd.read_csv(Con.paths['Stocks'] / str(x + '.csv'), parse_dates=[0], dayfirst=True)
            try:
                df['Date']
                Con.stock_data[x] = S.Stock(x, df)
            except KeyError:
                print('No Data for', x)
                no_data.append(x)

        except FileNotFoundError:
            print('File for', x, 'not found')

    print('Stocks with no data -> ', no_data)
    Con.stock_list = [x for x in Con.stock_list if x not in no_data]
    Con.num_of_stocks = len(Con.stock_list)
    Con.stock_encode = {k: v for v, k in enumerate(Con.stock_list)}
    Con.stock_decode = {v: k for v, k in enumerate(Con.stock_list)}
    test_stock_columns()


    return True


#########################################
#                                       #
#    ###############################    #
#    # OLD METHOD FOR LOADING DATA #    #
#    ###############################    #
#                                       #
#########################################

# main function called. It will initialise all stocks to be loaded
# True flag loads the newest data, false will use only from the file
def load_stock(flag="Offline"):
    print('Loading all stock')
    Con.stock_list = get_stock_list(True)
    if flag == "Online":
        sheets_refresh_stock()
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

# # get the missing data
# def download_stock_prices(stock,start = dt.datetime(1980, 1, 1)):
#     start = start + dt.timedelta(days=1)
#     try:
#         df = web.DataReader(stock, 'morningstar', start, Con.now)
#     except RemoteDataError:
#         print(stock, 'could not be downloaded')
#         return False
#     df.reset_index(inplace=True)
#     if start != dt.datetime(1980, 1, 2):
#         df = pd.concat([Con.stock_data[stock].df,df])
#     Con.stock_data[stock] = S.Stock(stock,df)
#     df.to_csv(str(Con.paths['Stocks'] / str(stock+'.csv')),index=False)
#     print('Downloaded',stock)
#     return True
