from thermodynamics.thermo_example_01 import ThermoExample01
from thermodynamics.thermo_example_02 import ThermoExample02
from classes.interface import PlotInterface

class AllThermoExamples(
        ThermoExample01,
        ThermoExample02
    ):

    def __init__(self):
        super().__init__()


