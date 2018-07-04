# the simulation class defines the parameters and settings for the simulation. The portfolio will track the
# history through time and benchmark calculated once concluded
import datetime as dt

from Classes import Holding as H
from Classes import Portfolio as Port
from Decision import Agent
from Decision import Decision as D
from Output import OutputFile as O
from Setup import Constants as Con


class Simulation:
    commision = 0
    start_period = False
    end_period = False
    current_date = False
    available_stocks = {}  # dictionary of available stocks, with key stock code
    portfolio = [] # Current Holdings
    temp_portfolio = None
    benchmark = False # Bench Marking Values
    init_investment = 0
    agent = None

    #initialise the simulation class
    def __init__(self, commision=0, start_period=None, end_period=None, current_date=None,
                 available_stocks=Con.stock_data, init_investment=Con.init_investment):
        # start should be max date and min date
        if start_period is None:
            start_period = min(available_stocks[x].start_date for x in available_stocks)
        if end_period is None:
            end_period = max(available_stocks[x].end_date for x in available_stocks)
        if current_date is None:
            current_date = start_period

        # set initial variables
        self.commision = commision
        self.start_period=start_period
        self.end_period=end_period
        self.current_date = current_date
        self.available_stocks = available_stocks
        self.init_investment = init_investment

        holding_dict = {}

        for key in self.available_stocks.keys():
            holding_dict[key] = H.Holding(key, 0)

        # portfolio is the current state at the beginning of the current day

        self.portfolio.append(Port.Portfolio(self.current_date, holding_dict, self.init_investment, 0, []))

        # establish output
        O.create_output_dict_sim(start_period, end_period, commision, init_investment)
        O.create_output_dict_trade()

        D.deep_q_learning.has_been_called = False
        # create agent
        if Con.current_episode == 0:
            if Con.decision_method == 'deep_q_learning':
                state_size = Con.num_of_stocks * (len(Con.columns_used) + 2)
                action_size = Con.num_of_stocks
                self.agent = Agent.DQNAgent(state_size, action_size)
        else:
            self.agent = Con.agent

        return

    def save_agent(self):
        Con.print_header_level_1('Saving Model')
        file_name = '_'.join([Con.stocks_for_simulation, str(Con.current_episode),
                              dt.datetime.now().strftime('%Y%m%d%H%M')]) + '.pkl'
        file_loc = str(Con.paths['Output'] / 'Models' / file_name)
        self.agent.model.save(file_loc)
        return


    # run simulations
    def run(self):

        # check still within the looping period
        while self.current_date != self.end_period:

            # get previous days state
            self.temp_portfolio = self.portfolio[-1]

            # check if valid
            if self.check_valid_transaction_day():
                # establish list of actions and do them
                getattr(D, Con.decision_method)(self)


            # store previous state
            self.portfolio.append(
                Port.Portfolio(self.current_date, self.temp_portfolio.holdings, self.temp_portfolio.cash_in_hand,
                               self.temp_portfolio.assets, Con.actions))
            Con.actions = []
            # increment performance counts
            if self.portfolio[-1].value > self.portfolio[-2].value:
                Con.good_period_count += 1
            else:
                Con.bad_period_count += 1

            # produce output for tracking progress
            self.output_progress('Y')

            # go to next day
            self.increment_period()

        self.output_progress()
        return True

    # increase the day count
    def increment_period(self):
        self.current_date = self.current_date + dt.timedelta(days=1)

        return

    # actually do the transaction, -1 sell, 0 hold, 1 buy
    def complete_transaction(self, action, stock, quantity):

        # BUY STOCK
        if action == 1:  # buy
            # check any available cash and stock data available
            if self.temp_portfolio.cash_in_hand > 0 and self.available_stocks[stock].start_date <= self.current_date:
                # find price
                price = list(self.available_stocks[stock].df.loc[
                                 self.available_stocks[stock].df['Date'] == self.current_date, 'Close'])
                if len(price) > 0:
                    try:
                        price = float(price[0])
                    except TypeError:
                        print("Error Raised")
                        return True
                    # calculate required value for purchase
                    max_quantity = float(self.temp_portfolio.cash_in_hand / price)
                    if quantity > max_quantity or quantity < 0:
                        quantity = max_quantity
                    # do transaction
                    self.temp_portfolio.holdings[stock].quantity += quantity
                    self.temp_portfolio.cash_in_hand -= price * quantity
                    Con.commision_current += self.commision
                    Con.actions.append([action, stock, -(price * quantity), 'COMPLETED', quantity, price])
                    Con.buy_count += 1
                    if Con.debugging:
                        print('Action', action, 'Stock', stock, 'Quantity', quantity)
                else:
                    Con.actions.append([action, stock, 0, 'NO PRICE', quantity, 0])
            else:
                Con.actions.append([action, stock, 0, 'NO DATA OR NO CASH', quantity, 0])
            return True

        # SELL STOCK
        elif action == -1:  # sell
            # check any available cash and stock data available
            if self.temp_portfolio.holdings[stock].quantity > 0 and self.available_stocks[
                stock].start_date <= self.current_date:
                # find price
                price = list(self.available_stocks[stock].df.loc[
                                 self.available_stocks[stock].df['Date'] == self.current_date, 'Close'])
                if len(price) > 0:
                    try:
                        price = float(price[0])
                    except TypeError:
                        print("Error Raised")
                        return True
                    # ccalculate quantity of sale
                    if quantity < 0 or quantity > self.temp_portfolio.holdings[stock].quantity:
                        quantity = float(self.temp_portfolio.holdings[stock].quantity)
                    # do transaction
                    self.temp_portfolio.holdings[stock].quantity -= quantity
                    self.temp_portfolio.cash_in_hand += price * quantity
                    Con.commision_current += self.commision
                    Con.actions.append([action, stock, (price * quantity), 'COMPLETED', quantity, price])
                    Con.sell_count += 1
                    if Con.debugging:
                        print('Action', action, 'Stock', stock, 'Quantity', quantity)
                else:
                    Con.actions.append([action, stock, 0, 'NO PRICE', quantity, 0])
            else:
                Con.actions.append([action, stock, 0, 'NO DATA OR NO ASSET', quantity, 0])
            return True

        # HOLD STOCK
        elif action == 0:  # hold
            if self.available_stocks[stock].start_date <= self.current_date:
                Con.hold_count += 1
                Con.actions.append([action, stock, quantity, 'COMPLETED', quantity, 0])
            return True

        # MOVE TO NEXT DAY
        else:
            if Con.debugging:
                print('\n\nFINIHING DAY DAY', self.current_date, '\n\n')
            temp = self.temp_portfolio.assets
            self.temp_portfolio.assets = 0

            # go through all stocks and get price
            for key in self.temp_portfolio.holdings:
                price = list(self.available_stocks[key].df.loc[
                                 self.available_stocks[key].df['Date'] == self.current_date, 'Close'])
                if len(price) > 0:
                    try:
                        price = float(price[0])
                    except TypeError:
                        print("Error Raised")
                        return True
                else:
                    price = 0
                # calculate value of the stock being held
                quantity = float(self.temp_portfolio.holdings[key].quantity)
                self.temp_portfolio.assets += price * quantity

            # Error case
            if self.temp_portfolio.assets == 0 and self.temp_portfolio.cash_in_hand == 0:
                self.temp_portfolio.assets = temp
            return False

    # make sure trades are only taking place on days that are valid
    def check_valid_transaction_day(self):
        if self.current_date.weekday() < 5:
            return True

        # check if week day check if there is data for the day print(str(self.current_date.year),
        # str(self.current_date.month), str(self.current_date.day), ':',calendar.day_name[self.current_date.weekday(
        # )], 'NOT VALID DAY')
        return False


    # outputs progress as you go, but will show daily/monthly/yearly ('D','M','Y')
    def output_progress(self,period='D'):
        if period == 'D':
            Con.print_state(self.portfolio[-1], self.current_date)
            return
        else:
            tempdate = self.current_date + dt.timedelta(days=1)
            if period == 'M' and tempdate.month != self.current_date.month:

                Con.print_state(self.portfolio[-1], self.current_date)
                return
            if period == 'Y' and tempdate.year != self.current_date.year:
                Con.print_state(self.portfolio[-1], self.current_date)
                return

