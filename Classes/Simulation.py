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

def init_simulation(self,commision=0,start_period=None,end_period=None,current_date=None,available_stocks=Con.stock_data,init_investment=10000):
    # start should be max date and min date
    start_period = min(x.start_date for x in available_stocks)
    end_period = max(x.end_date for x in available_stocks)

    if current_date is None:
        current_date = start_period

    self.commision = commision
    self.start_period=start_period
    self.end_period=end_period
    self.current_date = current_date
    self.available_stocks = available_stocks
    self.init_investment = init_investment


    return

def run(self):
    return

def increment_period(self):
    return

def complete_transaction():