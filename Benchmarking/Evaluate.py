# this function is used to evaluate the perforamnce of the model and produce clear visualisations of the decision method and forecasting accuracy
import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from Output import OutputFile as O
from Setup import Constants as Con


# Simulation evaluation main function used to call other evalutation functions
def Evaluate(Simulation):
    # performance evaluation
    calculate_profit(Simulation)
    # counts on actual trades
    trade_calculation(Simulation)
    # visualise performance
    graph_performance(Simulation)

    # record the paramters for the decision method
    O.store_metric('Parameters', Con.parameters_decision, 1)

    # store final output
    O.print_data(1)
    O.save_data(1)  # 1 is simulation

    store_actions(Simulation)

    return


# Evaluation of a models prediction
def Evaluate_Prediction(data, method):
    print('Evaluating', data.name, 'for', method)
    # set up dictionary
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
    if undershot <= 0:
        undershot = 0.000001
    if wrong_direction <= 0:
        wrong_direction = 0.000001
    O.store_metric('Direction Ratio', correct_direction / wrong_direction, 2)
    O.store_metric('Shot Ratio', overshot / undershot, 2)


    # output metrics
    O.print_data(2)
    O.save_data(2)  # 2 is model

    return


# profit calculations
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


# storing transaction counts
def trade_calculation(Simulation):
    O.store_metric('Num. Buy', Con.buy_count, 1)
    O.store_metric('Num. Sell', Con.sell_count, 1)
    O.store_metric('Num. Hold', Con.hold_count, 1)
    O.store_metric('Num. Trades', Con.sell_count + Con.buy_count, 1)
    O.store_metric('Num. Good Periods', Con.good_period_count, 1)

    O.store_metric('Num. Bad Periods', Con.bad_period_count, 1)
    if Con.bad_period_count <= 0:
        Con.good_period_count = 0.00001
    O.store_metric('Period Performance Ratio', Con.good_period_count / Con.bad_period_count, 1)

    return


# graph of simulation
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

    # split of up data from and format
    df = pd.DataFrame({'date': dates, 'value': value})
    df = df.set_index('date')
    df3 = pd.DataFrame({'date': dates, 'cash in hand': cash_in_hand, 'assets': assets})
    df3 = df3.set_index('date')

    # prepare individual stocks
    columns = ['date']
    df2 = pd.DataFrame(columns=columns)
    columns = ['date', 'Series', 'value']
    outputtempdf = pd.DataFrame(columns=columns)

    # collect stock data

    for key in Simulation.available_stocks:
        tempdf = pd.DataFrame({'date': Simulation.available_stocks[key].df['Date'],
                               Simulation.available_stocks[key].name: Simulation.available_stocks[key].df['Close']})
        tempdf = tempdf.set_index('date')

        temp2 = tempdf
        temp2['Series'] = key
        temp2.rename(columns={key: 'value'}, inplace=True)
        df2 = pd.merge(df2, tempdf, how='outer', left_index=True, right_index=True)
        outputtempdf = pd.concat([temp2, outputtempdf])
    df2 = df2.drop(columns='date')
    outputtempdf = outputtempdf.drop(columns='date')


    # plot performance and stocks on the same graph
    fig, axes = plt.subplots(nrows=3, ncols=1, sharex=True)
    df.plot(ax=axes[0], style='.')
    df3.plot(ax=axes[1], style='.')
    if len(Simulation.available_stocks) <= 5:
        df2.plot(ax=axes[2])
    plt.savefig(str(Con.paths['Output'] / 'Simulation.png'))
    if Con.display_graph:
        plt.show()

    df['Series'] = 'Value'
    tempdf = df3

    dfa = tempdf.drop(columns=['cash in hand'])
    dfa['Series'] = 'Cash In Hand'
    dfa.columns = ['value', 'Series']
    dfb = tempdf.drop(columns=['assets'])
    dfb['Series'] = 'Assets'
    dfb.columns = ['value', 'Series']
    dfoutput = pd.concat([df, dfa, dfb, outputtempdf])
    dfoutput['date'] = dfoutput.index

    # save all data points as output to be used by tableau
    dfoutput.to_csv(Con.paths['Output'] / 'PerformancePoints.csv', index=False)

    return


# visualisation of the prediction model
def graph_model(df, name):
    tempdf = df.drop(['Open', 'High', 'Low', 'Volume'], axis=1)
    tempdf = tempdf.set_index('Date')
    tempdf.plot()
    plt.title(name)
    plt.savefig(str(Con.paths['Output'] / 'Model.png'))
    if Con.display_graph:
        plt.show()
    return


def store_actions(Simulation):
    actions = []
    for x in Simulation.portfolio:
        for y in x.actions:
            action, stock, value, outcome, quantity, price = y[0], y[1], y[2], y[3], y[4], y[5]
            actions.append([x.day, action, stock, value, outcome, quantity, price])

    date_list, action_list, stock_list, value_list, outcome_list, quantity_list, price_list = list(zip(*actions))
    df = pd.DataFrame(
        {'date': date_list, 'action': action_list, 'stock': stock_list, 'value': value_list, 'outcome': outcome_list,
         'quantity': quantity_list, 'price': price_list})
    df.to_csv(Con.paths['Output'] / 'Actions.csv', index=False)
