# This function is essential for storing the values and performance of any simulation
# TODO store data in google sheets

import datetime
import pprint

from Setup import Constants as Con


# store metric
def store_metric(name, value):
    Con.output_dict[name] = value
    return


def print_data():
    pp = pprint.PrettyPrinter()
    pp.pprint(Con.output_dict)
    return


# add data to metric
def save_data():
    return


def create_output_dict(start_period, end_period, commision, init_investment):
    now = datetime.datetime.now()
    Con.output_dict = {
        'Date': now.strftime('%Y-%m-%d'),
        'Time': now.strftime('%H:%M'),
        'Stock Options': Con.stocks_for_simulation,
        'Decision Method': Con.decision_method,
        'Inputs': None,
        'Initial Investment': init_investment,
        'Commision': commision,
        'Start Date': start_period.strftime('%Y-%m-%d'),
        'End Date': end_period.strftime('%Y-%m-%d'),
        'Final Portfolio Value': None,
        'Profit': None,
        'Annual Profit': None,
        'Num. Trades': None,
        'Num. Good Trades': None,
        'Num. Buy': None,
        'Num. Sell': None,
        'Num. Hold': None,
        'Profit Percent': None
    }
    return
