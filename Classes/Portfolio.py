# portfolio is seen as the person. Any information they keep on that day or state they know (ie the agend)

from Setup import Constants as Con

class Portfolio:
    holdings = None
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