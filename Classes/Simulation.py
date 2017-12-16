# the simulation class defines the parameters and settings for the simualtion. The portolio will track the history thorugh time and benchmark calcualted once conlucded
from Setup import Constants as Con

class Simulation:
    commision = 0
    start_period = False
    end_period = False
    current_date = False
    available_stocks = [] # list of stock class
    portfolio = [] # Current Holdings
    benchmark = False # Bench Marking Values
    init_investment = 0

#initialise the simulation class
def init_simulation(self,commision=0,start_period=None,end_period=None,current_date=None,available_stocks=Con.stock_data,init_investment=Con.init_investment,decision_method=None):
    # start should be max date and min date
    if start_period is None:
        start_period = min(x.start_date for x in available_stocks)
    if end_period is None:
        end_period = max(x.end_date for x in available_stocks)
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


    return

def run(self):
    while self.current_date == self.end_period:
        if check_valid_transaction_day():
            self.calculate_decision()
            self.complete_transaction()
        self.increment_period()
    return True


def increment_period(self):
    self.current_date = self.current_date + 1
    return

def complete_transaction(self):
    return

def calculate_decision(self):
    return

def check_valid_transaction_day(self):
    return  True