# https://scikit-gstat.readthedocs.io/en/latest/install.html
import skgstat as skg
from .seismic_example_01 import SeismicExample01
from .seismic_example_02 import SeismicExample02
from .seismic_example_03 import SeismicExample03
from .seismic_example_04 import SeismicExample04

from classes.interface import PlotInterface

class AllSeismicExamples(
        SeismicExample01,
        SeismicExample02,
        SeismicExample03,
        SeismicExample04
    ):


    def __init__(self):
        super().__init__()


