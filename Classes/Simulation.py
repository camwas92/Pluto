# the simulation class defines the parameters and settings for the simualtion. The portolio will track the history thorugh time and benchmark calcualted once conlucded
from Setup import Constants as Con
import datetime as dt
from Classes import Portfolio as Port
import calendar

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

        # set initial variables
        self.commision = commision
        self.start_period=start_period
        self.end_period=end_period
        self.current_date = current_date
        self.available_stocks = available_stocks
        self.init_investment = init_investment

        #portfolio is the current state at the beginning of the current day
        self.portfolio.append(Port.Portfolio(self.current_date,None,self.init_investment,0))


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

                self.calculate_decision()
                self.complete_transaction()

            # continue each day

            self.increment_period()

            self.portfolio.append(Port.Portfolio(self.current_date,self.temp_portfolio.holdings,self.temp_portfolio.cash_in_hand,self.temp_portfolio.assets))

            self.output_progress('Y')

        self.output_progress()
        return True


    def increment_period(self):
        self.current_date = self.current_date + dt.timedelta(days=1)

        return

    def complete_transaction(self):
        return

    def calculate_decision(self):
        return

    def check_valid_transaction_day(self):
        if self.current_date.weekday() < 5:
            return True

        # check if week day
        # check if there is data for the day
        print(str(self.current_date.year), str(self.current_date.month), str(self.current_date.day), ':',
              calendar.day_name[self.current_date.weekday()], 'NOT VALID DAY')
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

