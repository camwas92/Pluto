# portfolio is seen as the person (their holdings) The systems current state. Any information a buyer would
# have on that day is keep

class Portfolio:
    holdings = {}  # list of stocks
    value = 0
    cash_in_hand = 0
    assets = 0
    day = None

    def __init__(self, current_date, holdings = None,cash_in_hand = 0, assets = 0):
        self.day = current_date
        self.cash_in_hand = cash_in_hand
        self.holdings = holdings
        self.assets = assets

        #calculate Value
        self.value = cash_in_hand + assets