# portfolio is seen as the person (their holdings) The systems current state. Any information a buyer would
# have on that day is keep
from Setup import Constants as Con

class Portfolio:
    holdings = {}  # list of stocks
    value = 0
    cash_in_hand = 0
    assets = 0
    day = None
    actions = []
    commision_costs = None

    def __init__(self, current_date, holdings=None, cash_in_hand=0, assets=0, actions=[]):
        self.day = current_date
        if cash_in_hand < 0:
            cash_in_hand = 0
        self.cash_in_hand = cash_in_hand
        self.holdings = holdings
        if assets < 0:
            assets = 0
        self.assets = assets
        self.commision_costs = Con.commision_current
        #calculate Value
        self.value = cash_in_hand + assets
        self.actions = actions
        if self.value <= 0:
            print('All portfolio values have gone below 0;\n', 'Value:', self.value, 'Assets', self.assets,
                  'Cash In Hand', self.cash_in_hand)
            self.value = 0
