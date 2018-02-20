# This class is used to track the stock holding for a single stock, knowing the price it was purchased at

class Holding:
    stock = ''
    quantity = 0

    def __init__(self, name, quantity):
        self.stock = name
        self.quantity = quantity
