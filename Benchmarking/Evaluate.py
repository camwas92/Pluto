from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.plotly as py
import plotly.graph_objs as go


def Evaluate (Simulation):
    # performance evaluation
    calculate_profit(Simulation)
    graph_performance(Simulation)
    # - graph over time

    #action evaluation
    # - number of trades
    # - number of good trades

    return

def calculate_profit (Simulation):
    init = Simulation.init_investment
    final = Simulation.portfolio[-1].value
    profit = final - init
    profit_per = (profit/init)*100

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

    #create traces
    valueLine = go.Scatter(
        x = dates,
        y = value,
        mode = 'lines',
        name = 'Value'
    )

    cash_in_handLine = go.Scatter(
        x=dates,
        y=cash_in_hand,
        mode='lines',
        name='Cash In Hand'
    )

    assetsLine = go.Scatter(
        x = dates,
        y = assets,
        mode='lines',
        name = 'Assets'
    )

    data = [valueLine,cash_in_handLine,assetsLine]

    plot(data, filename = 'Performance Graph.html')