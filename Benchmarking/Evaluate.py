# this function is used to evaluate the perforamnce of the model and produce clear visualisations of the decision method and forecasting accuracy
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


    # store final output
    O.print_data(1)
    O.save_data(1)  # 1 is simulation
    return


def Evaluate_Prediction(data, method):
    # todo implement prediction evaluation
    print('Evaluating', data.name, 'for', method)
    O.create_output_dict_model(data.name, method)
    # https://stats.stackexchange.com/questions/114752/forecast-accuracy-calculation

    error = 0

    correct_direction = 0
    wrong_direction = 0
    avg_gap = 0
    RMSE = 0
    MAE = 0
    MSE = 0
    MAPE = 0
    SMAPE = 0
    MPE = 0
    total_error_per = 0

    O.store_metric('Num. Correct Direction Per', correct_direction, 2)
    O.store_metric('Num. Wrong Direction Per', wrong_direction, 2)
    O.store_metric('MSE', MSE, 2)
    O.store_metric('RMSE', RMSE, 2)
    O.store_metric('MAE', MAE, 2)
    O.store_metric('MAPE', MAPE, 2)
    O.store_metric('SMAPE', SMAPE, 2)
    O.store_metric('MPE', MPE, 2)
    O.store_metric('Total Error Per', total_error_per, 2)

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
