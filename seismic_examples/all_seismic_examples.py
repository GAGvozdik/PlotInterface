# https://scikit-gstat.readthedocs.io/en/latest/install.html
import skgstat as skg
from .seismic_example_01 import SeismicExample01
from .seismic_example_02 import SeismicExample02
from .seismic_example_03 import SeismicExample03
from .seismic_example_04 import SeismicExample04
from .seismic_example_05 import SeismicExample05

from classes.interface import PlotInterface

class AllSeismicExamples(
    
        SeismicExample05,
        SeismicExample04,
        SeismicExample03,
        SeismicExample02,
        SeismicExample01
    ):


    def __init__(self):
        super().__init__()


