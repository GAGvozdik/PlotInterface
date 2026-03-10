# https://scikit-gstat.readthedocs.io/en/latest/install.html
import skgstat as skg
from .example1 import Example1
from .example2 import Example2
from .example3 import Example3
from .example4 import Example4
from .example5 import Example5
from .example6 import Example6
from .example7 import Example7
from .example8 import Example8
# from .example9 import Example9
# from .example10 import Example10
# from .example11 import Example11
# from .example12 import Example12
from .example13 import Example13
from .example14 import Example14
from .example15 import Example15
from .example16 import Example16
# from .example17 import Example17

from classes.interface import PlotInterface

class AllExamples(
        Example16, 
        Example15, 
        Example14, 
        Example13, 
        Example8, 
        Example7, 
        Example6, 
        Example5, 
        Example4, 
        Example3, 
        Example2, 
        Example1,
        PlotInterface
    ):

    def init_all_tabs(self):
        """Инициализация всех вкладок геостатистики."""
        self.init_geostat_16()
        self.init_geostat_15()
        self.init_geostat_14()
        self.init_geostat_13()
        self.init_geostat_08()
        self.init_geostat_07()
        self.init_geostat_06()
        self.init_geostat_05()
        self.init_geostat_04()
        self.init_geostat_03()
        self.init_geostat_02()
        self.init_geostat_01()
