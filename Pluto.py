# this is the main function
from Setup import Init_System as ISy
from Classes import Simulation as Sim
from Setup import Constants as Con


# load file paths
Con.print_header_level_1('Initialising System & Loading Stock  Data')
ISy.init_system()
Con.print_sucess_message('Data Prep')

# simulate system
Con.print_header_level_1('Initialising Simulation')
Simulation = Sim.Simulation(init_investment=1000)
Con.print_sucess_message('Simulation Initialisation')

Con.print_header_level_1('Running Simulation')
Simulation.run()
Con.print_sucess_message('Simulation')