# These are all the constants required for the project
import calendar
#################################
# Parameters to run the program #
#################################
stock_list = []
stock_data = {}
commision = 0
slipage = 0
init_investment = 10000
paths = []

#######################
# Changing Parameters #
#######################
decision_method = ''

###################
# Time Parameters #
###################
now = False


###################
# Data Parameters #
###################
stocks_for_simulation = 'Test'
#stocks_for_simulation = 'asx20'
# stocks_for_simulation = 'asx50'
# stocks_for_simulation = 'asx100'
# stocks_for_simulation = 'asx200'
# stocks_for_simulation = 'asx300'

###################
# Print Functions #
###################
def print_header_level_1(text):
    length = len(text)
    print ('\n\n'+length*'-')
    print (text)
    print(length*'-')
    return

def print_header_level_2(text):
    length = len(text)
    print('\n')
    print(text)
    print(length * '-')
    return

def print_sucess_message(text=None):
    if text is None:
        print('PROCESS COMPLETE - NO ERRORS\n')
    else:
        print(text.upper()+' COMPLETE - NO ERRORS\n')
    return

def print_state(Portfolio,current_date):
    print(str(current_date.year), str(current_date.month), str(current_date.day), ':',
          calendar.day_name[current_date.weekday()])
    print('\n     Value = '+str(Portfolio.value),
            '\n     C I H = ' + str(Portfolio.cash_in_hand),
            '\n     Asset = ' + str(Portfolio.assets),
            '\n')
    return