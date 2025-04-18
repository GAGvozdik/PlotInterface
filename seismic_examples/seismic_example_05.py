from classes.interface import PlotInterface
import numpy as np
from pathlib import Path
import numpy as np
import time
import matplotlib.pyplot as plt
import warnings
from scipy.fftpack import fft, ifft  
from scipy.signal import convolve, wiener
from scipy.optimize import minimize
from .seismic_functions.wiener_deconvolution import wiener_deconvolution
from .seismic_functions.convm import convm
from .seismic_functions.wavemin import wavemin
from .seismic_functions.reflect_from_model import reflec_from_model
from .seismic_functions.add_multiples import add_multiples
from .seismic_functions.absorption import absorption
from .seismic_functions.add_geometric_spreading import add_geometric_spreading
from matplotlib.colors import ListedColormap

# INTERFACE 4
class SeismicExample05(PlotInterface):
    def __init__(self):
        super().__init__()

from classes.interface import PlotInterface
import numpy as np
from pathlib import Path
import numpy as np
import time
import matplotlib.pyplot as plt
import warnings
from scipy.fftpack import fft, ifft  
from scipy.signal import convolve, wiener
from scipy.optimize import minimize
from .seismic_functions.wiener_deconvolution import wiener_deconvolution
from .seismic_functions.convm import convm
from .seismic_functions.wavemin import wavemin
from .seismic_functions.reflect_from_model import reflec_from_model
from .seismic_functions.add_multiples import add_multiples
from .seismic_functions.absorption import absorption
from .seismic_functions.add_geometric_spreading import add_geometric_spreading
from matplotlib.colors import ListedColormap

# INTERFACE 1
class SeismicExample01(PlotInterface):
    def __init__(self):
        super().__init__()
from classes.interface import PlotInterface
import numpy as np
from pathlib import Path
import numpy as np
import time
import matplotlib.pyplot as plt
import warnings
from scipy.fftpack import fft, ifft  
from scipy.signal import convolve, wiener
from scipy.optimize import minimize
from .seismic_functions.wiener_deconvolution import wiener_deconvolution
from .seismic_functions.convm import convm
from .seismic_functions.wavemin import wavemin
from .seismic_functions.reflect_from_model import reflec_from_model
from .seismic_functions.add_multiples import add_multiples
from .seismic_functions.absorption import absorption
from .seismic_functions.add_geometric_spreading import add_geometric_spreading
from matplotlib.colors import ListedColormap

# INTERFACE 5
class SeismicExample05(PlotInterface):
    def __init__(self):
        super().__init__()

        self.__tab = self.createTab('Ex05')

        self.__yScale = 0.4
        self.__xScale = 2.9

        self.createSlider(
            1, 500, init=int(self.__yScale * 400),
            func=self.__updatedYScale, 
            name='Y scale 1', 
            tab=self.__tab,
            label=True
        )
        self.tabAtr('Y scale 1 Slider Label').setText(str(self.__yScale))
        
        self.createSlider(
            50, 350, init=int(self.__xScale * 100),
            func=self.__updatedXScale, 
            name='X scale 1', 
            tab=self.__tab,
            label=True
        )
        self.tabAtr('X scale 1 Slider Label').setText(str(self.__yScale))

        self.__drawAxes()
        self.__draw()

        
    @PlotInterface.canvasDraw(tab='Ex05')
    def __draw(self):
        self.__ax.remove()
        self.__drawAxes()
        
    def __updatedYScale(self, index):
        self.__yScale = index / 400
        self.__draw()
        self.tabAtr('Y scale 1 Slider Label').setText(str(self.__yScale))
        
    def __updatedXScale(self, index):
        self.__xScale = index / 100
        self.__draw()
        self.tabAtr('X scale 1 Slider Label').setText(str(self.__xScale))

    @PlotInterface.canvasDraw(tab='Ex05')
    def __drawAxes(self):
        self.__ax = self.createAxes(
            self.tabAtr('Ex05Figure'),
            args={
                'pos': 111, 
                'name': 'Test',
                'xAxName': 'X', 
                'yAxName': 'Y',
                'grid': True,
                'fontsize': 26, 
                'fontweight': 'bold', 
                'loc': 'center', 
                'y': 1.05
            }
        )

        self.__ax.set_ylim([-self.__yScale, self.__yScale])
        self.__ax.set_xlim([0.1, self.__xScale])
        
