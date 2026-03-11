from .atmospheric_example_01 import AtmosphericExample01
from .atmospheric_example_02 import AtmosphericExample02

class AllAtmosphericExamples(AtmosphericExample01, AtmosphericExample02):
    def init_atmospheric_tabs(self):
        """Инициализация всех вкладок раздела Atmospheric Physics."""
        self.init_atmospheric_01()
        self.init_atmospheric_02()
