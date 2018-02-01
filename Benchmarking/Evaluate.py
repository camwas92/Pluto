# this function is used to evaluate the perforamnce of the model and produce clear visualisations of the decision method and forecasting accuracy
import matplotlib.pyplot as plt
import pandas as pd

from Output import OutputFile as O


# main function used to call other evalutation functions
def Evaluate(Simulation):
    # performance evaluation
    calculate_profit(Simulation)
    graph_performance(Simulation)
    # - graph over time

    # action evaluation
    # - number of trades
    # - number of good trades

    # Prediction Performance

    # store final output
    O.print_data(1)
    O.save_data(1)  # 1 is simulation
    return


def calculate_profit(Simulation):
    init = Simulation.init_investment
    final = Simulation.portfolio[-1].value
    profit = final - init
    profit_per = (profit / init) * 100

    O.store_metric('Profit', profit)
    O.store_metric('Profit Percent', profit_per)
    O.store_metric('Final Portfolio Value', final)

    print('{0:0.2f}%'.format(profit_per))

    return


def graph_performance(Simulation):
    dates = []
    value = []
    cash_in_hand = []
    assets = []

    # collect all simulation data
    for x in Simulation.portfolio:
        dates.append(x.day)
        value.append(x.value)
        cash_in_hand.append(x.cash_in_hand)
        assets.append(x.assets)

    df = pd.DataFrame({'date': dates, 'value': value, 'cash in hand': cash_in_hand, 'assets': assets})
    df = df.set_index('date')

    stocks = []
    # collect stock data
    for key in Simulation.available_stocks:
        tempdf = pd.DataFrame({'date': Simulation.available_stocks[key].df['Date'],
                               Simulation.available_stocks[key].name: Simulation.available_stocks[key].df['Open']})
        tempdf = tempdf.set_index('date')
        df = pd.merge(df, tempdf, how='outer', left_index=True, right_index=True)

    # plot performance and stocks on the same graph
    # TODO add a case to only include stocks if it is less than 5
    df.plot(secondary_y=['value', 'cash in hand', 'assets'])
    plt.show()
    return
