# this function will calcualte which stocks to invest in
import math
import random as rd

import numpy as np
import pandas as pd

from Setup import Constants as Con


def random_choice(Simulation):
    # set variable for storing actions
    actions = []
    Con.parameters_decision = {'Chance': 'B1:S1:H1:E2'}

    # calculate random action
    action, stock, quantity = rd.randint(-2, 2), rd.choice(list(Simulation.available_stocks.keys())), -1
    actions.append([action, stock, quantity])

    # continue to calculate and do random action until exit signal is given
    while Simulation.complete_transaction(action, stock, quantity):
        action, stock, quantity = rd.randint(-2, 2), rd.choice(list(Simulation.available_stocks.keys())), -1
        actions.append([action, stock, quantity])

    return


# buy proportion when predicted to go up, sell all when predicted to go down
def manual(Simulation):
    # establish storage variables
    Con.actions = []
    stocks = []
    per_changes = []
    buy_price = []

    df_columns = ['Date', Con.parameters_decision['manual'], 'Close']

    # go through stocks and get RF predictions, formating tem correctly and accessing difference between days
    for key in Simulation.available_stocks:
        # get predicted prices
        predict_prices = Simulation.available_stocks[key].df[df_columns]

        # get only today and tomorrows value
        current_value = predict_prices['Date'] == Simulation.current_date
        close_value = predict_prices['Date'] == Simulation.current_date
        next_value = current_value.shift(+1).fillna(False)

        # clean up and prepare data ensure it is valid
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

    # prepare data frame to calculate actions
    df = pd.DataFrame({'stock': stocks, 'per_changes': per_changes, 'buy_price': buy_price})

    df['action'] = np.where(df['per_changes'] < 1, -1, np.where(df['per_changes'] > 1, 1, 0))
    df['action'] = np.where(df['per_changes'] == 0, 0, df['action'])
    df['quantity'] = np.where(df['action'] < 0, -1, 0)

    # split data frames by action
    sell = df[df.action < 0]
    hold = df[df.action == 0]
    buy = df[df.action > 0]

    # calcualte buy propostions
    pd.options.mode.chained_assignment = None
    buy_total = buy.per_changes / buy.per_changes.sum()
    buy['Per_Total'] = buy_total
    cash_in_hand = Simulation.temp_portfolio.cash_in_hand
    buy['cash_in_hand'] = cash_in_hand
    dollar_value = buy['Per_Total'] * buy['cash_in_hand']
    buy['dollar_value'] = dollar_value
    try:
        quantity = buy['dollar_value'] / buy['buy_price']
        buy['quantity'] = quantity
    except ZeroDivisionError:
        buy['quantity'] = 0

    # convert actions to list
    sellactions = sell[['action', 'stock', 'quantity']].values.tolist()
    buyactions = buy[['action', 'stock', 'quantity']].values.tolist()
    holdactions = hold[['action', 'stock', 'quantity']].values.tolist()

    # run actions
    run_action_list(sellactions, Simulation)
    run_action_list(buyactions, Simulation)
    if len(holdactions) > 0:
        run_action_list(holdactions, Simulation)


    # print('Sell', sell, '\nbuy', buy, '\nhold', hold)

    # end day
    Simulation.complete_transaction(2, 'ERR', -1)

    return


# todo deep q learning
def deep_q_learning(Simulation):
    environment_array = get_environment(Simulation)

    actions = None
    sellactions, buyactions, holdactions = format_actions_for_dl(actions)
    # run actions
    run_action_list(sellactions, Simulation)
    run_action_list(buyactions, Simulation)
    if len(holdactions) > 0:
        run_action_list(holdactions, Simulation)

    # print('Sell', sell, '\nbuy', buy, '\nhold', hold)

    # end day
    Simulation.complete_transaction(2, 'ERR', -1)

    return


def get_environment(Simulation):
    stock_states = []
    for key in Con.stock_encoded:
        # get id
        id = Con.stock_encoded[key]
        # get quantity
        quantity = Simulation.portfolio[-1].holdings[key].quantity
        # get data
        try:
            data = Simulation.available_stocks[key].df.loc[
                       Simulation.available_stocks[key].df['Date'] == Simulation.current_date].iloc[0, 1:].tolist()
            # get value
            value = data[0] * quantity
        except IndexError:
            data = list([0] * (Con.num_columns - 1))
            # get value
            value = data[0] * quantity
        state = [id, quantity, value]
        stock_states.append(state + data)
    stock_states_array = np.nan_to_num(np.asarray(stock_states), copy=False)
    return stock_states_array


def format_actions_for_dl(actions):
    sell = None
    buy = None
    hold = None

    # convert actions to list
    sellactions = sell[['action', 'stock', 'quantity']].values.tolist()
    buyactions = buy[['action', 'stock', 'quantity']].values.tolist()
    holdactions = hold[['action', 'stock', 'quantity']].values.tolist()

    return sellactions, buyactions, holdactions

# do the required action
def run_action_list(list, Simulation):
    for x in list:
        action, stock, quantity = x
        Simulation.complete_transaction(action, stock, quantity)
    return


# check actions list is valid
def validate_list_of_actions(actions):
    if not actions:
        return False
    for x in actions[:-1]:
        if x[0] != 1 or x[0] != -1 or x[0] != 0:
            return False

    return True
