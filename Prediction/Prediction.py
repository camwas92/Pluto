# TODO NN
# TODO RF
# TODO Manual Methods
import sys

from Benchmarking import Evaluate as E
from Setup import Constants as Con


def run_predictions():
    for key in Con.stock_data:
        data = Con.stock_data[key]
        # add in predictions
        for x in Con.technical_methods:
            getattr(sys.modules[__name__], x)(data)
            E.Evaluate_Prediction(data, x)

        for x in Con.ML_methods:
            getattr(sys.modules[__name__], x)(data)
            E.Evaluate_Prediction(data, x)

    return True


# Technical Predictions
def tech_momentum(data):
    # placeholder
    data.df['momentum'] = 0
    return True


def tech_per_change(data):
    # placeholder
    data.df['per_change'] = 0
    return True


def tech_MACD(data):
    # placeholder
    data.df['MACD'] = 0
    return True


def tech_gradient(data):
    # placeholder
    data.df['gradient'] = 0
    return True


# ML Predictions
def ML_RF(data):
    # placeholder
    data.df['RF'] = 0
    return True


def ML_NN(data):
    # placeholder
    data.df['NN'] = 0
    return True
