import random as rd


def random_choice(available_stocks, portfolio):
    return rd.randint(-2, 2), rd.choice(list(available_stocks.keys())), -1


def testing(available_stocks, portfolio):
    return -2, 'CBA', 0


def manual(available_stocks, portfolio):
    # TODO implement manual decision
    # based on prediction sell all shares that will go down tomorrow
    # of the shares that will go up tomorrow which will go up the most, split cash value propotionally between the movement
    return 0, 0, 0
