# These are all the constants required for the project
import calendar
import logging

##################
# Online/Offline #
##################


line = 'Offline'
model_refresh = False
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
init_investment = 1000
paths = []

####################
# Decision Methods #
####################
# decision_method = 'random_choice'  # name of the function
# decision_method = 'manual'
# parameters_decision = {
#   'manual': 'ML_LSTM'}  # options 'ML_RF', 'ML_LSTM', 'tech_per_change', 'ML_NN', 'FE_window_7d', 'FE_window_14d'
decision_method = 'deep_q_learning'
parameters_decision = {'gamma': 0.05,
                       # aka decay or discount rate, to calculate the future discounted reward.  #default 0.95
                       'epsilon': 1.0,
                       # aka exploration rate, this is the rate in which an agent randomly decides its action rather than prediction. # default 1
                       'epsilon_min': 0.05,  # we want the agent to explore at least this amount. # default 0.01
                       'epsilon_decay': 0.995,
                       # we want to decrease the number of explorations as it gets good at playing games. # default 0.995
                       'learning_rate': 0.001,
                       # Determines how much neural net learns in each iteration. # default 0.001
                       'reward_function': 'reward + self.gamma *(scaled_predition)',
                       'num_layers': 2,
                       'model_shape': '24d,24d',  # numnode(type),
                       'drop_out': 0  # fraction of input units to drop
                       }
episodes = 100

######################
# Prediction Methods #
######################
technical_methods = []
# technical_methods = ['tech_per_change']
FE_methods = []
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
stocks_for_simulation = None

list_of_stocks = ['Model-Testing'  # 0
    , 'asx5'  # 1
    , 'asx20'  # 2
    , 'asx50'  # 3
    , 'asx100'  # 4
    , 'asx200'  # 5
    , 'asx300'  # 6
    , 'Telcom'  # 7
    , 'Consumer Staples'  # 8
    , 'Consumer Discretionary'  # 9
    , 'Materials'  # 10
    , 'Real Estate'  # 11
    , 'Information Technology'  # 12
    , 'Utilities'  # 13
    , 'Industrials'  # 14
    , 'Financials'  # 15
    , 'Health Care'  # 16
    , 'Energy']  # 17

list_of_manual_methods = ['ML_RF',
                          'ML_LSTM',
                          'tech_per_change',
                          'FE_window_7d',
                          'FE_window_14d',
                          'FE_window_30d',
                          'FE_window_60d',
                          'FE_window_90d',
                          'FE_window_360d',
                          ]


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
num_of_stocks = 0
stock_encode = None
stock_decode = None
num_columns = 0
columns_used = None
current_episode = 0

# Q Learning States #
state = None
action = None
agent = None
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
        # bot = telegram.Bot(token='604417883:AAEd4tS3VGgKhnRhXPYpNEWte4_JiRahxA8')
        # bot.send_message(chat_id=612638372, text=text)
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
