from .atmospheric_example_01 import AtmosphericExample01


class AllAtmosphericExamples(AtmosphericExample01):
    def init_atmospheric_tabs(self):
        """Инициализация всех вкладок раздела Atmospheric Physics."""
        self.init_atmospheric_01()
        # self.init_atmospheric_02()
