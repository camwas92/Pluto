import glob

import pandas as pd

from Setup import Constants as Con


def combine_stock_data():
    # concat individual stocks

    Con.print_header_level_2('Preparing Tableau File')

    columns = ['series', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    tempdf = pd.DataFrame(columns=columns)
    for x in glob.glob(str(Con.paths['Stocks'] / '*.csv')):
        df = pd.read_csv(x, parse_dates=[0], dayfirst=True)
        df['series'] = x[-7:-4]
        tempdf = pd.concat([tempdf, df])
    tempdf.to_csv(Con.paths['Output'] / 'StockValues.csv', index=False)

    # prepare stock describer file
    columns = ['series', 'Code', 'Company', 'Sector']
    tempdf = pd.DataFrame(columns=columns)
    xl = pd.ExcelFile(str(Con.paths['Input'] / 'StockList.xlsx'))
    for x in xl.sheet_names:
        df = xl.parse(x)
        df['series'] = x
        tempdf = pd.concat([tempdf, df])
    tempdf.to_csv(Con.paths['Output'] / 'StockDescription.csv', index=False)

    return
