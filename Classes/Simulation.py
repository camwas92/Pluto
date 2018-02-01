# the simulation class defines the parameters and settings for the simulation. The portfolio will track the
# history through time and benchmark calculated once concluded
import datetime as dt
import random

from Classes import Portfolio as Port
from Output import OutputFile as O
from Setup import Constants as Con


class Simulation:
    commision = 0
    start_period = False
    end_period = False
    current_date = False
    available_stocks = [] # list of stock class
    portfolio = [] # Current Holdings
    temp_portfolio = None
    benchmark = False # Bench Marking Values
    init_investment = 0

    #initialise the simulation class
    def __init__(self,commision=0,start_period=None,end_period=None,current_date=None,available_stocks=Con.stock_data,init_investment=Con.init_investment,decision_method=None):
        # start should be max date and min date
        if start_period is None:
            start_period = min(available_stocks[x].start_date for x in available_stocks)
        if end_period is None:
            end_period = max(available_stocks[x].end_date for x in available_stocks)
        if current_date is None:
            current_date = start_period
        if decision_method is None:
            Con.decision_method = 'random'
        else:
            Con.decision_method = decision_method
        random.seed(123)

        # set initial variables
        self.commision = commision
        self.start_period=start_period
        self.end_period=end_period
        self.current_date = current_date
        self.available_stocks = available_stocks
        self.init_investment = init_investment

        # portfolio is the current state at the beginning of the current day
        self.portfolio.append(Port.Portfolio(self.current_date,None,self.init_investment,0))

        # establish output
        O.create_output_dict_sim(start_period, end_period, commision, init_investment)

        return


    # run simulations
    def run(self):

        # check still within the looping period
        while self.current_date != self.end_period:

            # get previous days state
            self.temp_portfolio = self.portfolio[-1]

            # check if valid
            if self.check_valid_transaction_day():
                # temp
                self.temp_portfolio.assets += 1
                self.temp_portfolio.cash_in_hand += 1

                decision, stock, quantity = self.calculate_decision()
                self.complete_transaction(decision, stock, quantity)

            # continue each day
            self.increment_period()

            # store previous state
            self.portfolio.append(Port.Portfolio(self.current_date,self.temp_portfolio.holdings,self.temp_portfolio.cash_in_hand,self.temp_portfolio.assets))

            # produce output for tracking progress
            self.output_progress('Y')

        self.output_progress()
        return True

    # increase the day count
    def increment_period(self):
        self.current_date = self.current_date + dt.timedelta(days=1)

        return

    # actually do the transaction, -1 sell, 0 hold, 1 buy
    def complete_transaction(self, action, stock, quantity):
        # TODO build transaction rules
        if action == 1:  # buy
            print('Buying - ', stock)
            # check any available cash
            # calculate required value for purchase
            # if above max cash, then calculate max
            # calculate number being purchased
            return True
        elif action == -1:  # sell
            print('Selling - ', stock)
            # validate have this stock
            # check have enough to sell
            # check
            # convert to cash
            return True
        elif action == 0:  # hold
            print('Holding - ', stock)
            return True
        else:
            return False

    # call the decision method as required
    def calculate_decision(self):
        # all sales, then all purchases
        if Con.decision_method == 'random':
            return [random.randint(-1, 1), random.choice(list(self.available_stocks.keys()))]
        # TODO build decision calls
        return

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

