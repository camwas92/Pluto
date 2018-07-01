# These are all the constants required for the project
import calendar
import logging

import telegram

##################
# Online/Offline #
##################


line = 'Offline'
model_refresh = True
display_graph = False

#############
# Reference #
#############
debugging = False
tableau_output = False

#################################
# Parameters to run the program #
#################################
stock_list = []
stock_data = {}
commision = 0
slipage = 0
init_investment = 10000
paths = []

####################
# Decision Methods #
####################
decision_method = 'random_choice'  # name of the function
# decision_method = 'manual'
# todo make manual run on any prediction value
parameters_decision = {'manual': 'ML_RF'}

######################
# Prediction Methods #
######################
technical_methods = []
# technical_methods = ['tech_per_change']
FE_methods = ['FE_window_7d', 'FE_window_14d', 'FE_window_30d', 'FE_window_60d', 'FE_window_90d', 'FE_window_360d']
# technical_methods = ['FE_momentum','FE_MACD','FE_gradient','FE_window_7d','FE_window_14d','FE_window_30d','FE_window_60d','FE_window_90d','FE_window_360d']
ML_methods = []
# ML_methods = ['ML_LR','ML_RF','ML_NN','ML_LSTM']
parameters_prediction = {}

###################
# Time Parameters #
###################
now = False


###################
# Data Parameters #
###################
# todo set up industry lists
# stocks_for_simulation = 'Test'
stocks_for_simulation = 'Model-Testing'
# stocks_for_simulation = 'asx5'
# stocks_for_simulation = 'asx20'
# stocks_for_simulation = 'asx50'
# stocks_for_simulation = 'asx100'
# stocks_for_simulation = 'asx200'
# stocks_for_simulation = 'asx300'

############git.
# Trackers #
############
buy_count = 0
sell_count = 0
hold_count = 0
good_period_count = 0
bad_period_count = 0
actions = []
skipnum = 0
commision_current = 0
num_to_load = 1

#######################
# Google Drive Output #
#######################
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
outputfile = 'Portfolio Performance'
creds = ''
client = None

# Sim
row_count_sim = 0
column_count_sim = 0
output_dict_sim = {}
sheet_sim = None

# Model
row_count_model = 0
column_count_model = 0
output_dict_model = {}
sheet_model = None

# Trades
row_count_trade = 0
column_count_trade = 0
output_dict_trade = {}
sheet_trade = None

######################
# Google Drive Input #
######################
inputfile = 'Stock Data'

stock_request_text = "=GOOGLEFINANCE(sheetname(),\"all\",\"01/01/1990\",Today(),\"DAILY\")"

sheet_stock = None

###################
# Print Functions #
###################
def send_telegram_message(text):
    if not debugging:
        return
    else:
        bot = telegram.Bot(token='604417883:AAEd4tS3VGgKhnRhXPYpNEWte4_JiRahxA8')
        bot.send_message(chat_id=612638372, text=text)
        logging.info(text)
    return

def print_header_level_1(text):
    length = len(text)
    print ('\n\n'+length*'-')
    print (text)
    print(length*'-')
    send_telegram_message(text)
    return


def print_header_level_2(text):
    length = len(text)
    print('\n')
    print(text)
    print(length * '-')
    send_telegram_message(text)
    return

def print_sucess_message(text=None):
    if text is None:
        text = 'PROCESS COMPLETE - NO ERRORS\n'
        print(text)
    else:
        text = text.upper() + ' COMPLETE - NO ERRORS\n'
        print(text)
    send_telegram_message(text)
    return


def print_state(Portfolio,current_date):
    line = ' '.join([str(current_date.year), str(current_date.month), str(current_date.day), ':',
                     calendar.day_name[current_date.weekday()]])
    line2 = ' '.join(['     C I H = $', str(Portfolio.cash_in_hand)])
    line3 = ' '.join(['     Asset = $', str(Portfolio.assets)])
    text = '\n'.join(['=====================', line, '     Value = $' + str(Portfolio.value),
                      '=====================',
                      line2,
                      '           +             ',
                      line3, '=====================\n\n\n'])
    print(text)
    send_telegram_message(text)
    return



def print_progress(current, end):
    text = ' '.join([current, ''])
    print(text)
    send_telegram_message(text)
    return


def print_error_message(text=None):
    if text is None:
        text = 'ERROR OCCURED!!!!!!!!'
        print(text)
    else:
        print(text)
    send_telegram_message(text)
    return


def clear_lines(num=5):
    print('\n' * num)
    return
