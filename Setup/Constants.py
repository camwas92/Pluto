#  TODO fix the over 2 million issue
# These are all the constants required for the project
import calendar

##################
# Online/Offline #
##################
line = 'Online'
model_refresh = False
display_graph = False

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
# decision_method = 'random_choice'  # name of the function
decision_method = 'manual'
parameters_decision = {'manual': 'ML_RF'}

######################
# Prediction Methods #
######################
technical_methods = ['tech_per_change']
# technical_methods = ['tech_per_change']
FE_methods = []
# technical_methods = ['FE_momentum','FE_MACD','FE_gradient']
ML_methods = ['ML_RF']
# ML_methods = ['ML_LR','ML_RF','ML_NN']
parameters_prediction = {}

###################
# Time Parameters #
###################
now = False


###################
# Data Parameters #
###################
# stocks_for_simulation = 'Test'
# stocks_for_simulation = 'Model-Testing'
# stocks_for_simulation = 'asx5'
# stocks_for_simulation = 'asx20'
# stocks_for_simulation = 'asx50'
# stocks_for_simulation = 'asx100'
# stocks_for_simulation = 'asx200'
stocks_for_simulation = 'asx300'

############
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
num_to_load = 20

#######################
# Google Drive Output #
#######################
scope = ['https://spreadsheets.google.com/feeds']
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
    print('=====================',)
    print(str(current_date.year), str(current_date.month), str(current_date.day), ':',
          calendar.day_name[current_date.weekday()])
    print('\n     Value = $'+str(Portfolio.value),
          '\n=====================',
            '\n     C I H = $' + str(Portfolio.cash_in_hand),
          '\n           +             ',
            '\n     Asset = $' + str(Portfolio.assets))
    print('=====================\n\n\n', )
    return


def print_progress(current, end):
    print(current, '')


def print_error_message(text=None):
    if text is None:
        print('ERROR OCCURED!!!!!!!!')
    else:
        print(text)
    return
