# this function is used to evaluate the perforamnce of the model and produce clear visualisations of the decision method and forecasting accuracy
import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from Output import OutputFile as O
from Setup import Constants as Con


# main function used to call other evalutation functions
def Evaluate(Simulation):
    # performance evaluation
    calculate_profit(Simulation)
    trade_calculation(Simulation)
    graph_performance(Simulation)

    O.store_metric('Parameters', Con.parameters_decision, 1)

    # store final output
    O.print_data(1)
    O.save_data(1)  # 1 is simulation
    return


def Evaluate_Prediction(data, method):
    print('Evaluating', data.name, 'for', method)
    O.create_output_dict_model(data.name, method)

    # calcualte Y, Y_dash and movement direction
    tempdf = pd.DataFrame({'Y': data.df['Close'], 'Ydash': data.df[method]})
    tempdf['Y_s(-1)'] = tempdf['Y'].shift(-1)
    tempdf['Ydash_s(-1)'] = tempdf['Ydash'].shift(-1)
    tempdf['Y_direction_temp'] = np.where(tempdf['Y'] >= tempdf['Y_s(-1)'], -1, 1)
    tempdf['Y_direction'] = np.where(tempdf['Y'] == tempdf['Y_s(-1)'], 0, tempdf['Y_direction_temp'])
    tempdf['Ydash_direction_temp'] = np.where(tempdf['Ydash'] >= tempdf['Ydash_s(-1)'], -1, 1)
    tempdf['Ydash_direction'] = np.where(tempdf['Y'] == tempdf['Ydash_s(-1)'], 0, tempdf['Ydash_direction_temp'])
    tempdf['correct'] = np.where(tempdf['Y_direction'] == tempdf['Ydash_direction'], 1, -1)

    # calculate all error values
    errordf = pd.DataFrame()
    errordf['Y-Ydash'] = tempdf['Y'].subtract(tempdf['Ydash'], axis=0)
    errordf['|Y-Ydash|'] = abs(errordf['Y-Ydash'])
    errordf['Y-Ydash/Y'] = errordf['Y-Ydash'].divide(tempdf['Y'], axis=0)
    errordf['|Y-Ydash|/|Y|'] = errordf['|Y-Ydash|'].divide(abs(tempdf['Y']), axis=0)
    errordf['(Y-Ydash)^2'] = errordf['Y-Ydash'] ** 2

    # valuate direction movement
    overshot = errordf[errordf['Y-Ydash'] < 0].count()[0]
    undershot = errordf[errordf['Y-Ydash'] > 0].count()[0]
    correct_direction = tempdf[tempdf['correct'] > 0].count()[0]
    wrong_direction = tempdf[tempdf['correct'] < 0].count()[0]

    # calculate error metrics
    avg_gap = errordf['Y-Ydash'].mean()
    MSE = errordf['(Y-Ydash)^2'].mean()
    RMSE = math.sqrt(MSE)
    MAE = errordf['|Y-Ydash|'].mean()
    MAPE = (errordf['|Y-Ydash|/|Y|'].mean()) * 100
    MPE = (errordf['Y-Ydash/Y'].mean()) * 100

    # store all metrics
    O.store_metric('Num. Correct Direction Per', correct_direction, 2)
    O.store_metric('Num. Wrong Direction Per', wrong_direction, 2)
    O.store_metric('MSE', MSE, 2)
    O.store_metric('RMSE', RMSE, 2)
    O.store_metric('MAE', MAE, 2)
    O.store_metric('MAPE', MAPE, 2)
    O.store_metric('MPE', MPE, 2)
    O.store_metric('Overshot', overshot, 2)
    O.store_metric('Undershot', undershot, 2)
    O.store_metric('Average Gap', avg_gap, 2)

    # output metrics
    O.print_data(2)
    O.save_data(2)  # 2 is model

    return


def calculate_profit(Simulation):
    init = Simulation.init_investment
    final = Simulation.portfolio[-1].value
    profit = final - init
    profit_per = (profit / init) * 100
    length = Simulation.end_period - Simulation.start_period
    length = (length / np.timedelta64(1, 'D')).astype(int)
    annual_profit = (profit_per / length) * 365

    O.store_metric('Profit', profit, 1)
    O.store_metric('Profit Percent', profit_per, 1)
    O.store_metric('Final Portfolio Value', final, 1)
    O.store_metric('Annual Profit', annual_profit, 1)

    print('{0:0.2f}%'.format(profit_per))

    return


def trade_calculation(Simulation):
    O.store_metric('Num. Buy', Con.buy_count, 1)
    O.store_metric('Num. Sell', Con.sell_count, 1)
    O.store_metric('Num. Hold', Con.hold_count, 1)
    O.store_metric('Num. Trades', Con.sell_count + Con.buy_count, 1)
    O.store_metric('Num. Good Periods', Con.good_period_count, 1)
    O.store_metric('Num. Bad Periods', Con.bad_period_count, 1)

    return


def graph_performance(Simulation):

    dates = []
    value = []
    cash_in_hand = []
    assets = []

    # collect all simulation data
    for x in Simulation.portfolio:
        dates.append(x.day)
        value.append(x.value)
        cash_in_hand.append(x.cash_in_hand)
        assets.append(x.assets)

    df = pd.DataFrame({'date': dates, 'value': value})
    df = df.set_index('date')
    df3 = pd.DataFrame({'date': dates, 'cash in hand': cash_in_hand, 'assets': assets})
    df3 = df3.set_index('date')

    columns = ['date']
    df2 = pd.DataFrame(columns=columns)

    # collect stock data
    if len(Simulation.available_stocks) <= 5:
        for key in Simulation.available_stocks:
            tempdf = pd.DataFrame({'date': Simulation.available_stocks[key].df['Date'],
                                   Simulation.available_stocks[key].name: Simulation.available_stocks[key].df['Open']})
            tempdf = tempdf.set_index('date')
            df2 = pd.merge(df2, tempdf, how='outer', left_index=True, right_index=True)
    df2.drop(columns='date')

    # plot performance and stocks on the same graph
    fig, axes = plt.subplots(nrows=3, ncols=1, sharex=True)
    df.plot(ax=axes[0], style='.')
    df3.plot(ax=axes[1], style='.')
    df2.plot(ax=axes[2])
    plt.show()

    df['Series'] = 'Value'
    tempdf = df3

    dfa = tempdf.drop(columns=['cash in hand'])
    dfa['Series'] = 'Cash In Hand'
    dfa.columns = ['value', 'Series']
    dfb = tempdf.drop(columns=['assets'])
    dfb['Series'] = 'Assets'
    dfb.columns = ['value', 'Series']
    dfoutput = pd.concat([df, dfa, dfb])
    dfoutput.to_csv(Con.paths['Output'] / 'PerformacnePoints.csv')

    return


def graph_model(df, name):
    tempdf = df.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis=1)
    tempdf = tempdf.set_index('Date')
    tempdf.plot()
    plt.title(name)
    plt.show()
    return
