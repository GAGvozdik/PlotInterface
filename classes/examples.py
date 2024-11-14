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
from .example9 import Example9
from .example10 import Example10
from .example11 import Example11
from .example12 import Example12
from .example13 import Example13
from .example14 import Example14
from .example15 import Example15
from .interface import PlotInterface

class AllExamples(
        # PlotInterface,
        Example15, 
        Example14, 
        Example13, 
        Example12, 
        # Example11, 
        # Example10, 
        Example9,
        Example8, 
        Example7, 
        # Example6, 
        # Example5, 
        Example4, 
        # Example3, 
        Example2, 
        # Example1
    ):


    def __init__(self):
        super().__init__()


