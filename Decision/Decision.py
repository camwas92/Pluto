import math
import random as rd

import numpy as np
import pandas as pd

from Setup import Constants as Con


def random_choice(Simulation):
    actions = []
    Con.parameters_decision = {'Chance': 'B1:S1:H1:E2'}
    action, stock, quantity = rd.randint(-2, 2), rd.choice(list(Simulation.available_stocks.keys())), -1
    actions.append([action, stock, quantity])
    while Simulation.complete_transaction(action, stock, quantity):
        action, stock, quantity = rd.randint(-2, 2), rd.choice(list(Simulation.available_stocks.keys())), -1
        actions.append([action, stock, quantity])

    return


def testing(Simulation):
    return -2, 'AMP', 0


def manual(Simulation):
    actions = []
    stocks = []
    per_changes = []
    buy_price = []
    df_columns = ['Date', Con.parameters_decision['manual'], 'Close']

    for key in Simulation.available_stocks:
        predict_prices = Simulation.available_stocks[key].df[df_columns]
        current_value = predict_prices['Date'] == Simulation.current_date
        close_value = predict_prices['Date'] == Simulation.current_date
        next_value = current_value.shift(+1).fillna(False)

        close_value = list(predict_prices.Close[close_value].values)
        if len(close_value) < 1:
            buy_price.append(0)
        else:
            buy_price.append(float(close_value[0]))

        current_value = list(predict_prices.ML_RF[current_value].values)
        if len(current_value) < 1:
            current_value = np.nan
        else:
            current_value = current_value[0]

        next_value = list(predict_prices.ML_RF[next_value].values)
        if len(next_value) < 1:
            next_value = np.nan
        else:
            next_value = next_value[0]
        if math.isnan(current_value) or math.isnan(next_value):
            per_change = 0
        else:
            per_change = float(float(next_value) / float(current_value))
        stocks.append(key)
        per_changes.append(per_change)

    df = pd.DataFrame({'stock': stocks, 'per_changes': per_changes, 'buy_price': buy_price})

    df['action'] = np.where(df['per_changes'] < 1, -1, np.where(df['per_changes'] > 1, 1, 0))
    df['action'] = np.where(df['per_changes'] == 0, 0, df['action'])
    df['quantity'] = np.where(df['action'] < 0, -1, 0)

    sell = df[df.action < 0]
    buy = df[df.action > 0]
    buy['Per_Total'] = buy.per_changes / buy.per_changes.sum()
    hold = df[df.action == 0]

    sellactions = sell[['action', 'stock', 'quantity']].values.tolist()
    print(sellactions)

    for x in sellactions:
        action, stock, quantity = list(x)
        actions.append([action, stock, quantity])
        Simulation.complete_transaction(action, stock, quantity)
        # todo figure out why double sell

    buy['cash_in_hand'] = Simulation.temp_portfolio.cash_in_hand
    buy['dollar_value'] = buy['Per_Total'] * buy['cash_in_hand']
    try:
        buy['quantity'] = buy['dollar_value'] / buy['buy_price']
    except ZeroDivisionError:
        buy['quantity'] = 0

    buyactions = buy[['action', 'stock', 'quantity']].values.tolist()
    print(buyactions)

    for x in buyactions:
        action, stock, quantity = list(x)
        actions.append([action, stock, quantity])
        Simulation.complete_transaction(action, stock, quantity)
        # todo figure out why you can make negative purchases on AMP

    holdactions = hold[['action', 'stock', 'quantity']].values.tolist()

    for x in holdactions:
        action, stock, quantity = list(x)
        actions.append([action, stock, quantity])

    # print('Sell', sell, '\nbuy', buy, '\nhold', hold)

    # end day
    Simulation.complete_transaction(2, 'ERR', -1)

    return


def validate_list_of_actions(actions):
    if not actions:
        return False
    for x in actions[:-1]:
        if x[0] != 1 or x[0] != -1:
            return False

    return True
