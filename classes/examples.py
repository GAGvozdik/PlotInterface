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

class AllExamples(Example9, Example8, Example7, Example6, Example5, Example4, Example2):
    def __init__(self):
        super().__init__()



