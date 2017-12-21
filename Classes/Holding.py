# This class is used to track the stock holding for a single stock, knowing the price it was purchased at

class Holding:
    stock = ''
    purchase_price = 0
    quantity = 0

    def __init__(self, name, price, quantity):
        self.stock = name
        self.purchase_price = price
        self.quantity = quantity
