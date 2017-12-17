import matplotlib.pyplot as plt
import pandas as pd


def Evaluate(Simulation):
    # performance evaluation
    calculate_profit(Simulation)
    graph_performance(Simulation)
    # - graph over time

    # action evaluation
    # - number of trades
    # - number of good trades

    # Prediction Performance

    return


def calculate_profit(Simulation):
    init = Simulation.init_investment
    final = Simulation.portfolio[-1].value
    profit = final - init
    profit_per = (profit / init) * 100

    print('{0:0.2f}%'.format(profit_per))
    return


def graph_performance(Simulation):
    dates = []
    value = []
    cash_in_hand = []
    assets = []
    for x in Simulation.portfolio:
        dates.append(x.day)
        value.append(x.value)
        cash_in_hand.append(x.cash_in_hand)
        assets.append(x.assets)

    df = pd.DataFrame({'date': dates, 'value': value, 'cash in hand': cash_in_hand, 'assets': assets})
    df = df.set_index('date')

    stocks = []
    for key in Simulation.available_stocks:
        tempdf = pd.DataFrame({'date': Simulation.available_stocks[key].df['Date'],
                               Simulation.available_stocks[key].name: Simulation.available_stocks[key].df['Open']})
        tempdf = tempdf.set_index('date')
        df = pd.merge(df, tempdf, how='outer', left_index=True, right_index=True)

    df.plot(secondary_y=['value', 'cash in hand', 'assets'])
    plt.show()
