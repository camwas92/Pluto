# This function is essential for storing the values and performance of any simulation

import datetime
import pprint

from Setup import Constants as Con


# store metric
def store_metric(name, value, option):
    if option == 1:
        Con.output_dict_sim[name] = value
    elif option == 2:
        Con.output_dict_model[name] = value
    elif option == 3:
        Con.output_dict_trade[name] = value
        return

    return


def select_Data(option):
    if option == 1:
        return (Con.output_dict_sim)
    elif option == 2:
        return (Con.output_dict_model)
    elif option == 3:
        return (Con.output_dict_trade)

def get_headers(option):
    if option == 1:
        headers = (Con.sheet_sim.row_values(1))
    elif option == 2:
        headers = (Con.sheet_model.row_values(1))
    elif option == 3:
        headers = (Con.sheet_trade.row_values(1))
    else:
        headers = 0

    count = list(range(1, len(headers) + 1))

    return dict(zip(count, headers))


def get_column_count(option):
    if option == 1:
        return (Con.column_count_sim)
    elif option == 2:
        return (Con.column_count_model)
    elif option == 3:
        return (Con.column_count_trade)



def print_data(option):
    pp = pprint.PrettyPrinter()
    pp.pprint(select_Data(option))


def write_row(option, line):
    if option == 1:
        Con.sheet_sim.insert_row(line, 2)
    elif option == 2:
        Con.sheet_model.insert_row(line, 2)
    elif option == 3:
        Con.sheet.trade.insert_row(line, 2)
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
    print('Data Saved')
    return


# Create Dic
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
        'Num. Good Periods': None,
        'Num. Bad Periods': None,
        'Num. Buy': None,
        'Num. Sell': None,
        'Num. Hold': None,
        'Profit Percent': None,
        'Parameters': None
    }
    return


def create_output_dict_model(stock, model):
    now = datetime.datetime.now()

    Con.output_dict_model = {
        'Date': now.strftime('%Y-%m-%d'),
        'Time': now.strftime('%H:%M'),
        'Stock': stock,
        'Model': model,
        'Num. Correct Direction Per': None,
        'Num. Wrong Direction Per': None,
        'Average Gap': None,
        'MSE': None,
        'RMSE': None,
        'MAE': None,
        'MAPE': None,
        'MPE': None,
        'Overshot': None,
        'Undershot': None,
        'Parameters': Con.parameters_prediction
    }
    return


def create_output_dict_trade():
    now = datetime.datetime.now()
    Con.output_dict_trade = {
        'Date': now.strftime('%Y-%m-%d'),
        'Time': now.strftime('%H:%M'),
        'Series': None,
        'Value': None
    }
    return
