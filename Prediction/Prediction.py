# creates and appends all predictions for the stucks
import datetime as dt
import sys

import numpy as np
import pandas as pd
from keras.layers import Dense
from keras.layers import LSTM
from keras.models import Sequential
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from statsmodels.tsa.arima_model import ARIMA

from Benchmarking import Evaluate as E
from Setup import Constants as Con
from Setup import Init_System as IS


# run all predictions
def run_predictions():
    count = 0
    skip = False
    skip_to = 'SAR'
    for key in Con.stock_data:
        count += 1
        if skip:
            if skip_to == key:
                skip = False
                print('Skipping', key)
                print('Ending Skipping')
            else:
                print('Skipping', key)
        else:
            print_str = 'Preparing ' + key + ' #' + str(count)
            Con.print_header_level_1(print_str)
            data = Con.stock_data[key]
            # add in predictions
            Con.skipnum = int(len(data.df['Close']) / 100)  # used to print progress

            # run and evaluate all technical methods
            for x in Con.technical_methods:
                getattr(sys.modules[__name__], x)(data, x)
                IS.connect_google_sheets()
                E.Evaluate_Prediction(data, x)

            # run and evaluate all Machine learning methods
            for x in Con.ML_methods:
                getattr(sys.modules[__name__], x)(data, x)
                IS.connect_google_sheets()
                E.Evaluate_Prediction(data, x)

            E.graph_model(data.df, key)

            # run feature engineering methods
            for x in Con.FE_methods:
                getattr(sys.modules[__name__], x)(data, x)

            # Store stock
            data.df.to_csv(str(Con.paths['Stocks'] / str(key + '.csv')), index=False)

    return True


# Technical Predictions
def tech_per_change(data, method):
    Con.print_header_level_2('Percent Change')
    # define parameters
    Con.parameters_prediction = {'Number_Of_Periods': 5}

    tempdf = pd.DataFrame({'Today': data.df['Close']})
    tempdf['Tomorrow'] = tempdf['Today'].shift(+1)
    tempdf['Change from Yesterday'] = tempdf['Today'].subtract(tempdf['Tomorrow'], axis=0)

    # calculate % change
    tempdf['Running_Sum'] = tempdf['Change from Yesterday'].rolling(
        window=Con.parameters_prediction['Number_Of_Periods'], center=False).sum()
    tempdf['tech_per_change'] = tempdf['Today'].add(tempdf['Running_Sum'])
    tempdf['tech_per_change'] = tempdf['tech_per_change'].shift(+1)
    data.df[method] = tempdf['tech_per_change']
    return True


# stock feature -> Needs to be implemented
def FE_momentum(data, method):
    # placeholder
    data.df[method] = 0
    return True


# stock feature -> Needs to be implemented
def FE_MACD(data, method):
    # placeholder
    data.df[method] = 0
    return True


# stock feature -> Needs to be implemented
def FE_gradient(data, method):
    # placeholder
    data.df[method] = 0
    return True


# Linear Regression
def ML_LR(data, method):
    Con.print_header_level_2('Linear Regression')
    # store parameters
    Con.parameters_prediction = {'Lag_Value': 5,
                                 'Difference_Order': 2,
                                 'Moving_Average': 2}

    # get prices
    X = list(data.df['Close'])
    size = int(len(X) * 0.10)
    # split data set so all predictions are osnly on this history of the data
    train, test = X[0:size], X[size:len(X)]
    history = [x for x in train]
    predictions = list()
    num = len(test)

    # run through each day making a prediction
    for t in range(num):
        model = ARIMA(history, order=(Con.parameters_prediction['Lag_Value'],
                                      Con.parameters_prediction['Difference_Order'],
                                      Con.parameters_prediction['Moving_Average']))

        model_fit = model.fit(disp=0)
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(float(yhat))
        obs = test[t]
        history.append(obs)
        if num > 100:
            if t % int(Con.skipnum) == 0:
                print(t, 'of', num, 'periods', '@', dt.datetime.now().time())

    df = pd.DataFrame({'Prediction': predictions})

    # store prediction
    data.df[method] = df
    data.df[method] = data.df[method].shift(+size)
    return


# Random Forest
def ML_RF(data, method):
    Con.print_header_level_2('Random Forest')
    # store paramaters
    Con.parameters_prediction = {}

    # Get prices
    X = list(data.df['Close'])
    size = int(len(X) * 0.05)

    # split data set so only training on historic data
    train, test = X[0:size], X[size:len(X)]
    history = [x for x in train]
    predictions = list()
    num = len(test)

    # run through each day predicting
    for t in range(num):
        model = RandomForestRegressor(random_state=0)

        # prepare data sets
        x = np.asarray(list(range(0, len(history))))
        x = x.reshape(len(x), 1)
        y = np.asarray(history)
        y = y.reshape(len(y), )

        # train model
        model.fit(x, y)

        # predict tomorrow
        yhat = model.predict(len(history) + 1)

        predictions.append(float(yhat))

        obs = test[t]
        history.append(obs)

        # out put progress
        if num > 100:
            if t % int(Con.skipnum) == 0:
                print(t, 'of', num, 'periods')

    df = pd.DataFrame({'Prediction': predictions})

    # store data
    data.df[method] = df
    data.df[method] = data.df[method].shift(+size)
    return True


# Neural Network
def ML_NN(data, method):
    Con.print_header_level_2('Neural Network')
    # store parameters
    Con.parameters_prediction = {'hidden_layer_sizes': (100,),
                                 'activation': 'relu',
                                 'solver': 'adam',
                                 'alpha': 0.00001,
                                 'random_state': 0
                                 }

    # get price data
    X = list(data.df['Close'])
    size = int(len(X) * 0.05)

    # split data so only training on historic
    train, test = X[0:size], X[size:len(X)]
    history = [x for x in train]
    predictions = list()
    num = len(test)
    # run through each day
    for t in range(num):
        # build model framework
        model = MLPRegressor(hidden_layer_sizes=Con.parameters_prediction['hidden_layer_sizes'],
                             activation=Con.parameters_prediction['activation'],
                             solver=Con.parameters_prediction['solver'],
                             alpha=Con.parameters_prediction['alpha'],
                             random_state=Con.parameters_prediction['random_state'])

        # prepare data
        x = np.asarray(list(range(0, len(history))))
        x = x.reshape(len(x), 1)
        y = np.asarray(history)
        y = y.reshape(len(y), )

        # train model
        model.fit(x, y)

        # predict next day
        yhat = model.predict(len(history) + 1)

        predictions.append(float(yhat))

        obs = test[t]
        history.append(obs)

        # print progress
        if num > 100:
            if t % int(Con.skipnum) == 0:
                string = ' '.join([str(t), 'of', str(num), 'periods'])
                Con.clear_lines(10)
                Con.print_header_level_2(string)

    df = pd.DataFrame({'Prediction': predictions})

    # store data set
    data.df[method] = df
    data.df[method] = data.df[method].shift(+size)
    return True


# Neural Network
def ML_LSTM(data, method):
    Con.print_header_level_2('LSTM')
    # store parameters
    Con.parameters_prediction = {'hidden_layer_sizes1': 100,
                                 'hidden_layer_sizes2': 100,
                                 'loss': 'mae',
                                 'solver': 'adam',
                                 'epochs': 100,
                                 'batch_size': 36,
                                 'activation': 'relu'
                                 }

    # get price data
    X = list(data.df['Close'])
    size = int(len(X) * 1)

    # split data so only training on historic
    train, test = X[0:size], X[size:len(X)]
    history = [x for x in train]
    predictions = list()
    num = len(test)

    # Build model
    model = Sequential()
    model.add(LSTM(Con.parameters_prediction['hidden_layer_sizes1'], return_sequences=True, input_shape=(1, 1),
                   activation=Con.parameters_prediction['activation']))
    model.add(LSTM(Con.parameters_prediction['hidden_layer_sizes2'],
                   activation=Con.parameters_prediction['activation']))
    model.add(Dense(1))
    model.compile(loss=Con.parameters_prediction['loss'], optimizer=Con.parameters_prediction['solver'])


    # run through each day

    # build model framework
    # prepare data
    x = np.asarray(list(range(0, len(history))))
    x = x.reshape(len(x), 1, 1)
    y = np.asarray(history)
    y = y.reshape(len(y), )

    # reset model
    model.reset_states()

    # train model
    model.fit(x, y, epochs=Con.parameters_prediction['epochs'],
              batch_size=Con.parameters_prediction['batch_size'],
              verbose=1, shuffle=False)

    # predict next day
    yhat = list(model.predict(x))

    for i in yhat:
        predictions.append(float(i[0]))




    df = pd.DataFrame({'Prediction': predictions})

    # store data set
    data.df[method] = df
    return True
