import gc
import sys

from Benchmarking import Evaluate as E
from Benchmarking import TableauPrep as TP
from Classes import Simulation as Sim
from Prediction import Prediction as P
from Setup import Constants as Con
from Setup import Init_System as ISy

Con.stocks_for_simulation = Con.list_of_stocks[int(sys.argv[1])]
Con.episodes = int(sys.argv[2])
# load file paths
gc.collect()
Con.print_header_level_1('Initialising System & Loading Stock  Data')

ISy.init_system()
Con.print_sucess_message('Data Prep')

# run predictions
if Con.model_refresh:
    Con.print_header_level_1('Run Predictions')
    P.run_predictions()
    TP.combine_stock_data()
    Con.print_sucess_message('Predictions')

# run simulation
Con.print_header_level_1('Running Simulation')

for Con.current_episode in range(Con.episodes):
    Con.print_header_level_1('Episode: {0}/{1}'.format(Con.current_episode, Con.episodes))
    Simulation = Sim.Simulation(init_investment=Con.init_investment)
    Simulation.run()
    Con.agent = Simulation.agent
    E.Evaluate(Simulation)
    Con.print_sucess_message('Simulation')
