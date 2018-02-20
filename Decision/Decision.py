import random as rd


def random_choice(available_stocks, portfolio):
    return rd.randint(-2, 2), rd.choice(list(available_stocks.keys())), -1


def testing(available_stocks, portfolio):
    return -2, 'CBA', 0
