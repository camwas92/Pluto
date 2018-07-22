# this function will calcualte which stocks to invest in
import math
import random as rd

import numpy as np
import pandas as pd

from Setup import Constants as Con


def take_actions(Simulation, buyactions, holdactions, sellactions):
    # run actions
    run_action_list(sellactions, Simulation)
    run_action_list(buyactions, Simulation)
    if len(holdactions) > 0:
        run_action_list(holdactions, Simulation)
    if Con.debugging:
        print('Sell', sellactions, '\nBuy', buyactions)
        if Con.deep_learning:
            print('Exploring', Simulation.agent.random_value < Simulation.agent.epsilon)

    # end day
    Simulation.complete_transaction(2, 'ERR', -1)

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


def deep_q_learning_exploration(Simulation):
    Simulation.agent.epsilon = 100
    deep_q_learning(Simulation)
    return


def deep_q_learned(Simulation):
    Simulation.agent.epsilon = -100
    deep_q_learning(Simulation)
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

        current_value = list(predict_prices[Con.parameters_decision['manual']].loc[current_value].values)
        if len(current_value) < 1:
            current_value = np.nan
        else:
            current_value = current_value[0]

        next_value = list(predict_prices[Con.parameters_decision['manual']].loc[next_value].values)
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
    # can only buy if you have cash in hand, therefore don't get the money from a sale first
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

    take_actions(Simulation, buyactions, holdactions, sellactions)

    return


def deep_q_learning(Simulation):
    # run the first day of actions
    if not deep_q_learning.has_been_called:
        state = get_environment(Simulation, current=True)  # shape = Con.num_of_stocks*(len(Con.columns_used)+2)
        # get actions
        calcualte_and_do_actions(Simulation, state)
    else:
        next_state = get_environment(Simulation, current=True)
        if Simulation.agent.epsilon < 99 and Simulation.agent.epsilon > 0:
            Simulation.agent.remember(Con.state, Con.action, Simulation.portfolio[-1].value, next_state, False)
        state = next_state
        # train the agent
        if Simulation.agent.epsilon < 99 and Simulation.agent.epsilon > 0:
            Simulation.agent.replay(32)
        calcualte_and_do_actions(Simulation, state)
    deep_q_learning.has_been_called = True
    return


def calcualte_and_do_actions(Simulation, state):
    actions = Simulation.agent.act(state)
    # format actions and complete
    sellactions, buyactions, holdactions = format_actions_for_dl(actions, Simulation)
    take_actions(Simulation, buyactions, holdactions, sellactions)
    Con.state = state
    Con.action = actions
    return


def get_environment(Simulation, current=None, previous=None):
    stock_states = []
    if current:
        selection = -1
    elif previous:
        selection = -2
    else:
        raise ValueError('No Available Date')

    data_colection = -Con.parameters_decision['data_depth'] + selection

    for x in range(data_colection, selection + 1):
        for key in Con.stock_encode:
            # get id
            id = Con.stock_encode[key]
            # get quantity
            # get data
            try:
                quantity = Simulation.portfolio[x].holdings[key].quantity
                temp = Simulation.available_stocks[key].df.loc[
                    Simulation.available_stocks[key].df['Date'] == Simulation.portfolio[x].day]
                data = temp[Con.columns_used].iloc[0, 1:].tolist()
                # get value
                value = data[0] * quantity
            except IndexError:
                quantity = 0
                data = list([0] * (len(Con.columns_used) - 1))
                # get value
                value = data[0] * quantity
            state = [id, quantity, value]
            stock_states.append(state + data)
        temp = np.asarray(stock_states)
        stock_states_array = np.nan_to_num(temp)
    stock_return = stock_states_array.reshape(Con.parameters_decision['data_depth'] + 1,
                                              Con.num_of_stocks * (len(Con.columns_used) + 2))
    return stock_return


def format_actions_for_dl(actions, Simulation):
    sellactions = []
    buyactions = []
    holdactions = []
    actions = list(actions)
    threshold_sell = -.1
    threshold_buy = .1

    for i, value in enumerate(actions):
        if value > threshold_buy:
            buyactions.append([1, Con.stock_decode[i], abs(value)])
        elif value < threshold_sell:
            sellactions.append([-1, Con.stock_decode[i], -1])  # sell all
        else:
            holdactions.append([0, Con.stock_decode[i], abs(value)])

    # calculate quantities
    today = Simulation.current_date
    cash_in_hand = Simulation.portfolio[-1].cash_in_hand
    buy_df = pd.DataFrame((buyactions), columns=['Action', 'Stock', 'Value'])
    prices = []
    for x in buy_df['Stock'].tolist():
        try:
            price = Simulation.available_stocks[x].df.loc[
                Simulation.available_stocks[x].df.Date == today, 'Close'].values[0]
        except IndexError:
            price = 0
        prices.append(price)

    # format buy to be a proportion of available cash
    buy_df['BuyPrice'] = prices
    buy_df['Prop'] = np.where(buy_df['BuyPrice'] == 0, 0, buy_df['Value'])
    buy_df['Spend'] = (buy_df.Prop / buy_df.Prop.sum()) * cash_in_hand
    buy_df['Quantity'] = buy_df['Spend'] / buy_df['BuyPrice']
    buy_df.fillna(0, inplace=True)
    buyactions = buy_df[['Action', 'Stock', 'Quantity']].values.tolist()

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
