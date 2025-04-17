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

        # Define the input parameters
        self.v = np.array([1000, 2000, 1500, 5000, 7000, 2500])  # Velocity in m/s
        self.rho = np.array([2500, 2700, 2000, 4500, 4800, 2900])  # Density in kg/m^3
        self.q = np.array([50, 50, 50, 50, 50, 50])  # Quality factor
        self.thk = np.array([100, 70, 100, 250, 300])  # Thickness in meters
        
        self.__dt = 0.015  # Sampling interval in seconds
        self.tmax = 2  # Total modeled time in seconds
        self.__yScale = 0.4
        self.__xScale = 2.9
        
        # Define the dominant frequency for absorption
        self.__fdom = 20  # Dominant frequency in Hz

        self.__tab = self.createTab('Ex01')

        self.createSlider(
            1, 3000, init=int(10 * self.__fdom),
            func=self.updateFDom, 
            name='Dominant frequency', 
            tab=self.__tab,
            label=True
        )
        self.tabAtr('Dominant frequency Slider Label').setText(str(self.__fdom))
        
        self.createSlider(
            20, 500, init=int(self.__dt * 10000),
            func=self.updatedT, 
            name='dT', 
            tab=self.__tab,
            label=True
        )
        self.tabAtr('dT Slider Label').setText(str(self.__dt))
        
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

        self.drawAxes01()
        self.__draw()

        
    @PlotInterface.canvasDraw(tab='Ex01')
    def __draw(self):
        self.__ax1.remove()
        self.drawAxes01()
        
        # Call the reflec_from_model function
        self.R, self.V, self.RHO, self.Q, self.THK, self.T = reflec_from_model(self.rho, self.v, self.q, self.thk, self.__dt, self.tmax)

        # Call the add_multiples function
        self.RM = add_multiples(self.R, type=1, R0=-0.5)
        
        self.RL = absorption(self.RM, self.Q, self.__dt, self.__fdom) # do you know why here is RM? 

        self.Rg = add_geometric_spreading(self.RL, self.THK) 

        # Plot the original reflectivity signal
        self.__ax1.plot(self.T, self.R, linewidth=7, color='gray', label='Original Reflectivity')

        # Plot the original and modified reflectivity signals
        self.__ax1.plot(self.T, self.RM, linewidth=6, color='orange', label='Reflectivity with Multiples')

        self.__ax1.plot(self.T, self.RL, linewidth=6, color='darkcyan', label='Reflectivity with Multiples and absorption')
        
        self.__ax1.plot(self.T, self.Rg, linewidth=6, color='Crimson', label='Reflectivity with absorption and geometric_spreading')
        
        self.__ax1.legend(loc=1, fontsize=17)
        

    def updateFDom(self, index):
        self.__fdom = index / 10
        self.__draw()
        self.tabAtr('Dominant frequency Slider Label').setText(str(self.__fdom))
        
    def updatedT(self, index):
        self.__dt = index / 10000
        print(self.__dt)
        self.__draw()
        self.tabAtr('dT Slider Label').setText(f"{self.__dt:.4f}")
        
    def __updatedYScale(self, index):
        self.__yScale = index / 400
        self.__draw()
        self.tabAtr('Y scale 1 Slider Label').setText(str(self.__yScale))
        
    def __updatedXScale(self, index):
        self.__xScale = index / 100
        self.__draw()
        self.tabAtr('X scale 1 Slider Label').setText(str(self.__xScale))
        
        
    @PlotInterface.canvasDraw(tab='Ex01')
    def drawAxes01(self):
        self.__ax1 = self.createAxes(
            self.tabAtr('Ex01Figure'),
            args={
                'pos': 111, 
                'name': 'Reflectivity Comparison',
                'xAxName': 'Time (s)', 
                'yAxName': 'Amplitude',
                'grid': True,
                'fontsize': 26, 
                'fontweight': 'bold', 
                'loc': 'center', 
                'y': 1.05
            }
        )
        # self.__ax1.axis([0, self.tmax, -1, 1])  # Set axis limits
        # self.__ax1.axis([0, self.tmax, -.4, 0.1])  # Set axis limits
        self.__ax1.set_ylim([-self.__yScale, self.__yScale])
        self.__ax1.set_xlim([0.1, self.__xScale])
        
