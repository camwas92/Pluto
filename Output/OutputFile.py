# This function is essential for storing the values and performance of any simulation

import datetime
import pprint

from Setup import Constants as Con


# store metric
def store_metric(name, value):
    Con.output_dict_sim[name] = value
    return


def select_Data(option):
    if option == 1:
        return (Con.output_dict_sim)
    else:
        return (Con.output_dict_model)


def get_headers(option):
    if option == 1:
        headers = (Con.sheet_sim.row_values(1))
    else:
        headers = (Con.sheet_model.row_values(1))

    count = list(range(1, len(headers) + 1))

    return dict(zip(count, headers))


def get_column_count(option):
    if option == 1:
        return (Con.column_count_sim)
    else:
        return (Con.column_count_model)


def print_data(option):
    pp = pprint.PrettyPrinter()
    pp.pprint(select_Data(option))


def write_row(option, line):
    if option == 1:
        Con.sheet_sim.insert_row(line, 2)
    else:
        Con.sheet_model.insert_row(line, 2)
    return

# add data to metric
def save_data(option):
    data = select_Data(option)
    headers = get_headers(option)
    # produce line of data
    line = []
    for i in range(1, get_column_count(option) + 1):
        line.append(data[headers[i]])
    write_row(option, line)
    return


def create_output_dict_sim(start_period, end_period, commision, init_investment):
    now = datetime.datetime.now()
    Con.output_dict_sim = {
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
