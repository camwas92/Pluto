# this is the main function
# todo update read me
# todo add comments
# todo add in commition
from Benchmarking import Evaluate as E
from Benchmarking import TableauPrep as TP
from Classes import Simulation as Sim
from Prediction import Prediction as P
from Setup import Constants as Con
from Setup import Init_System as ISy

# load file paths
Con.print_header_level_1('Initialising System & Loading Stock  Data')
ISy.init_system()
Con.print_sucess_message('Data Prep')

# run predictions
if Con.model_refresh:
    Con.print_header_level_1('Run Predictions')
    P.run_predictions()
    TP.combine_stock_data()
    Con.print_sucess_message('Predictions')

# simulate system
Con.print_header_level_1('Initialising Simulation')
Simulation = Sim.Simulation(init_investment=1000)
Con.print_sucess_message('Simulation Initialisation')

# run simulation
Con.print_header_level_1('Running Simulation')
Simulation.run()
Con.print_sucess_message('Simulation')

# run benchmarking
Con.print_header_level_1('Benchmarking')
E.Evaluate(Simulation)
Con.print_sucess_message('Benchmarking')