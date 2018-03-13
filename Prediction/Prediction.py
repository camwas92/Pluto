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
            getattr(sys.modules[__name__], x)(data, x)
            E.Evaluate_Prediction(data, x)

        for x in Con.ML_methods:
            getattr(sys.modules[__name__], x)(data, x)
            E.Evaluate_Prediction(data, x)

    return True


# Technical Predictions
def tech_momentum(data, method):
    # placeholder
    data.df[method] = 0
    return True


def tech_per_change(data, method):
    # placeholder
    data.df[method] = 0
    return True


def tech_MACD(data, method):
    # placeholder
    data.df[method] = 0
    return True


def tech_gradient(data, method):
    # placeholder
    data.df[method] = 0
    return True


# ML Predictions
def ML_RF(data, method):
    # placeholder
    data.df[method] = 0
    return True


def ML_NN(data, method):
    # placeholder
    data.df[method] = 0
    return True
