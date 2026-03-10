from classes.interface import PlotInterface
import numpy as np
from pathlib import Path
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
class SeismicExample05:
    def init_seismic_05(self):
        # Define the input parameters
        self.__v = np.array([1000, 2000, 1500, 5000, 7000, 2500])  # Velocity in m/s
        self.__rho = np.array([2500, 2700, 2000, 4500, 4800, 2900])  # Density in kg/m^3
        self.__q = np.array([50, 50, 50, 50, 50, 50])  # Quality factor
        self.__thk = np.array([100, 70, 100, 250, 300])  # Thickness in meters
        
        self.__dt = 0.0005  # Sampling interval in seconds
        self.__tmax = 2  # Total modeled time in seconds
        
        # Define the dominant frequency for absorption
        self.__fdom = 20  # Dominant frequency in Hz
        self.__noize = 0  # Noise level


        self.__tab = self.createTab('Ex05')

        self.__yScale = 1.25
        self.__xScale = 1

        self.createSlider(
            0, 80, init=int(self.__noize * 1000),
            func=self.__updatedNoize, 
            name='Noize 5', 
            tab=self.__tab,
            label=True
        )
        self.tabAtr('Noize 5 Slider Label').setText(str(self.__noize))
        
        self.createSlider(
            1, 500, init=int(self.__yScale * 400),
            func=self.__updatedYScale, 
            name='Y scale 5', 
            tab=self.__tab,
            label=True
        )
        self.tabAtr('Y scale 5 Slider Label').setText(str(self.__yScale))
        
        self.createSlider(
            50, 350, init=int(self.__xScale * 100),
            func=self.__updatedXScale, 
            name='X scale 5', 
            tab=self.__tab,
            label=True
        )
        self.tabAtr('X scale 5 Slider Label').setText(str(self.__yScale))

        self.createSlider(
            5, 500, init=int(self.__dt * 10000),
            func=self.__updatedT, 
            name='dT 5', 
            tab=self.__tab,
            label=True
        )
        self.tabAtr('dT 5 Slider Label').setText(str(self.__dt))


        self.__drawAxes()
        self.__draw()

        
    @PlotInterface.canvasDraw(tab='Ex05')
    def __draw(self):
        self.__ax.remove()
        self.__drawAxes()
        
        self.__R, self.__V, self.__RHO, self.__Q, self.__THK, self.__T = reflec_from_model(self.__rho, self.__v, self.__q, self.__thk, self.__dt, self.__tmax)
        self.__R += np.random.normal(0, self.__noize, len(self.__R))
        self.__ax.plot(self.__T, self.__R, linewidth=4, color='Crimson', label='Original Reflectivity')
        
    def __updatedYScale(self, index):
        np.random.seed(100)
        self.__yScale = index / 400
        self.__draw()
        self.tabAtr('Y scale 5 Slider Label').setText(str(self.__yScale))
        
    def __updatedXScale(self, index):
        np.random.seed(100)
        self.__xScale = index / 100
        self.__draw()
        self.tabAtr('X scale 5 Slider Label').setText(str(self.__xScale))

    def __updatedNoize(self, index):
        self.__noize = index / 1000
        np.random.seed(None)
        self.__draw()
        self.tabAtr('Noize 5 Slider Label').setText(str(self.__noize))
        
    def __updatedT(self, index):
        np.random.seed(100)
        self.__dt = index / 10000
        self.__draw()
        self.tabAtr('dT 5 Slider Label').setText(f"{self.__dt:.4f}")
        
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
