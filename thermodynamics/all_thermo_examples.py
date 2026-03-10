from thermodynamics.thermo_example_01 import ThermoExample01
from thermodynamics.thermo_example_02 import ThermoExample02
from classes.interface import PlotInterface

class AllThermoExamples(
        ThermoExample01,
        ThermoExample02,
        PlotInterface
    ):

    def init_thermo_tabs(self):
        """Инициализация всех вкладок термодинамики."""
        self.init_thermo_01()
        self.init_thermo_02()
