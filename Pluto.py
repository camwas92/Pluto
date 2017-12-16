# this is the main function
from Setup import Init_System as ISy
from Classes import Simulation as Sim


# load file paths
ISy.init_system()

# simulate system
Simulation = Sim.init_simulation(init_investment=1000)
Simulation.run()
