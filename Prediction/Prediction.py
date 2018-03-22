# TODO NN
# TODO RF
import datetime as dt
import sys

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from statsmodels.tsa.arima_model import ARIMA

from Benchmarking import Evaluate as E
from Setup import Constants as Con


def run_predictions():
    for key in Con.stock_data:
        data = Con.stock_data[key]
        # add in predictions
        Con.skipnum = int(len(data.df['Close']) / 10)
        print(Con.skipnum)
        for x in Con.technical_methods:
            getattr(sys.modules[__name__], x)(data, x)
            E.Evaluate_Prediction(data, x)

        for x in Con.ML_methods:
            getattr(sys.modules[__name__], x)(data, x)
            E.Evaluate_Prediction(data, x)

        E.graph_model(data.df, key)

        for x in Con.FE_methods:
            getattr(sys.modules[__name__], x)(data, x)

        data.df.to_csv(str(Con.paths['Stocks'] / str(key + '.csv')), index=False)

    return True


# Technical Predictions
def tech_per_change(data, method):
    Con.parameters_prediction = {'Number_Of_Periods': 5}

    tempdf = pd.DataFrame({'Today': data.df['Close']})
    tempdf['Tomorrow'] = tempdf['Today'].shift(+1)
    tempdf['Change from Yesterday'] = tempdf['Today'].subtract(tempdf['Tomorrow'], axis=0)

    tempdf['Running_Sum'] = tempdf['Change from Yesterday'].rolling(
        window=Con.parameters_prediction['Number_Of_Periods'], center=False).sum()
    tempdf['tech_per_change'] = tempdf['Today'].add(tempdf['Running_Sum'])
    tempdf['tech_per_change'] = tempdf['tech_per_change'].shift(+1)
    data.df[method] = tempdf['tech_per_change']
    return True


def FE_momentum(data, method):
    # placeholder
    data.df[method] = 0
    return True


def FE_MACD(data, method):
    # placeholder
    data.df[method] = 0
    return True


def FE_gradient(data, method):
    # placeholder
    data.df[method] = 0
    return True


# ML Predictions
def ML_LR(data, method):
    Con.parameters_prediction = {'Lag_Value': 5,
                                 'Difference_Order': 1,
                                 'Moving_Average': 0}

    X = list(data.df['Close'])
    size = int(len(X) * 0.05)
    train, test = X[0:size], X[size:len(X)]
    history = [x for x in train]
    predictions = list()
    num = len(test)
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
            if t % int(num / Con.skipnum) == 0:
                print(t, 'of', num, 'periods', '@', dt.datetime.now().time())

    df = pd.DataFrame({'Prediction': predictions})

    data.df[method] = df
    data.df[method] = data.df[method].shift(+size)
    return

def ML_RF(data, method):
    Con.parameters_prediction = {}

    X = list(data.df['Close'])
    size = int(len(X) * 0.05)
    train, test = X[0:size], X[size:len(X)]
    history = [x for x in train]
    predictions = list()
    num = len(test)
    for t in range(num):
        model = RandomForestRegressor(random_state=0)
        x = np.asarray(list(range(0, len(history))))
        x = x.reshape(len(x), 1)
        y = np.asarray(history)
        y = y.reshape(len(y), )

        model.fit(x, y)

        yhat = model.predict(len(history) + 1)

        predictions.append(float(yhat))

        obs = test[t]
        history.append(obs)

        if num > 100:
            if t % int(num / Con.skipnum) == 0:
                print(t, 'of', num, 'periods')

    df = pd.DataFrame({'Prediction': predictions})

    data.df[method] = df
    data.df[method] = data.df[method].shift(+size)
    return True


def ML_NN(data, method):
    Con.parameters_prediction = {'hidden_layer_sizes': (100,),
                                 'activation': 'relu',
                                 'solver': 'adam',
                                 'alpha': 0.00001,
                                 'random_state': 0
                                 }

    X = list(data.df['Close'])
    size = int(len(X) * 0.05)
    train, test = X[0:size], X[size:len(X)]
    history = [x for x in train]
    predictions = list()
    num = len(test)
    for t in range(num):
        model = MLPRegressor(hidden_layer_sizes=Con.parameters_prediction['hidden_layer_sizes'],
                             activation=Con.parameters_prediction['activation'],
                             solver=Con.parameters_prediction['solver'],
                             alpha=Con.parameters_prediction['alpha'],
                             random_state=Con.parameters_prediction['random_state'])
        x = np.asarray(list(range(0, len(history))))
        x = x.reshape(len(x), 1)
        y = np.asarray(history)
        y = y.reshape(len(y), )

        model.fit(x, y)

        yhat = model.predict(len(history) + 1)

        predictions.append(float(yhat))

        obs = test[t]
        history.append(obs)

        if num > 100:
            if t % int(num / Con.skipnum) == 0:
                print(t, 'of', num, 'periods')

    df = pd.DataFrame({'Prediction': predictions})

    data.df[method] = df
    data.df[method] = data.df[method].shift(+size)
    return True
