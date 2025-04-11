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

# INTERFACE 2
class SeismicExample02(PlotInterface):
    def __init__(self):
        super().__init__()

        # Define the input parameters
        self.v = np.array([1000, 2000, 1500, 5000, 7000, 2500])  # Velocity in m/s
        self.rho = np.array([2500, 2700, 2000, 4500, 4800, 2900])  # Density in kg/m^3
        self.q = np.array([50, 50, 50, 50, 50, 50])  # Quality factor
        self.thk = np.array([100, 70, 100, 250, 300])  # Thickness in meters
        
        self.dt = 0.02  # Sampling interval in seconds
        self.tmax = 2  # Total modeled time in seconds

        # Define the dominant frequency for absorption
        self.fdom = 20  # Dominant frequency in Hz


        self.tab02 = self.createTab('Ex02')

        self.slider02 = self.createSlider(
            1, 3000, init=int(10 * self.fdom),
            func=self.updateFDom02, 
            name='Dominant frequency 2', 
            tab=self.tab02,
            label=True
        )
        self.tabAtr('Dominant frequency 2 Slider Label').setText(str(self.fdom))
        
        self.slider03 = self.createSlider(
            20, 500, init=int(self.dt * 10000),
            func=self.updatedT02, 
            name='dT 2', 
            tab=self.tab02,
            label=True
        )
        self.tabAtr('dT 2 Slider Label').setText(str(self.dt))
        

        self.drawAxes02()
        self.draw02()

        
    @PlotInterface.canvasDraw(tab='Ex02')
    def draw02(self):
        self.ax02_1.remove()
        self.ax02_2.remove()
        self.ax02_3.remove()
        self.ax02_4.remove()
        self.drawAxes02()
        
        # Call the reflec_from_model function
        self.R, self.V, self.RHO, self.Q, self.THK, self.T = reflec_from_model(self.rho, self.v, self.q, self.thk, self.dt, self.tmax)

        # Call the add_multiples function
        self.RM = add_multiples(self.R, type=1, R0=-0.5)
        
        self.RL = absorption(self.RM, self.Q, self.dt, self.fdom) # do you know why here is RM? 

        self.Rg = add_geometric_spreading(self.RL, self.THK) 

        # Plot the original reflectivity signal
        self.ax02_1.plot(self.T, self.R, linewidth=3, color='darkcyan', label='Original Reflectivity')

        # Plot the original and modified reflectivity signals
        self.ax02_2.plot(self.T, self.RM, linewidth=3, color='orange', label='Reflectivity with Multiples')

        self.ax02_3.plot(self.T, self.RL, linewidth=3, color='Crimson', label='Reflectivity with Multiples and absorption')
        
        self.ax02_4.plot(self.T, self.Rg, linewidth=1, color='mediumseagreen', label='Reflectivity with absorption and geometric_spreading')
        
        self.ax02_1.legend(loc=4, fontsize=17)
        self.ax02_2.legend(loc=4, fontsize=17)
        self.ax02_3.legend(loc=4, fontsize=17)
        self.ax02_4.legend(loc=4, fontsize=17)
        

    def updateFDom02(self, index):
        self.fdom = index / 10
        self.draw02()
        self.tabAtr('Dominant frequency 2 Slider Label').setText(str(self.fdom))
        
    def updatedT02(self, index):
        self.dt = index / 10000
        print(self.dt)
        self.draw02()
        self.tabAtr('dT 2 Slider Label').setText(f"{self.dt:.4f}")

    @PlotInterface.canvasDraw(tab='Ex02')
    def drawAxes02(self):
        # self.tabAtr('Ex02Figure').tight_layout(pad=0, w_pad=0, h_pad=0, rect=[0, 0, 1, 1])
        self.tabAtr('Ex02Figure').subplots_adjust(
            left=0.07,    # немного отступ слева
            right=0.97,   # немного отступ справа
            top=0.97,     # немного отступ сверху
            bottom=0.07,  # немного отступ снизу
            wspace=0.4,   # расстояние между subplot'ами по ширине
            hspace=0.4    # расстояние между subplot'ами по высоте
        )

        self.ax02_1 = self.createAxes(
            self.tabAtr('Ex02Figure'),
            args={
                'pos': 411, 
                # 'name': 'Reflectivity Comparison',
                'xAxName': 'Time (s)', 
                'yAxName': 'Amplitude',
                'grid': True,
                'fontsize': 26, 
                'fontweight': 'bold', 
                'loc': 'center', 
                'y': 1.05
            }
        )
        self.ax02_1.axis([-0.08, self.tmax, -0.4, 0.4])  # Set axis limits
        # self.ax02_1.axis([-0.08, self.tmax, -1, 1])  # Set axis limits
        # self.ax02_1.set_ylim([-1, 1])
        # self.ax02_1.set_xlim([-0.08, 2.9])
        
        self.ax02_2 = self.createAxes(
            self.tabAtr('Ex02Figure'),
            args={
                'pos': 412, 
                # 'name': 'Reflectivity Comparison',
                'xAxName': 'Time (s)', 
                'yAxName': 'Amplitude',
                'grid': True,
                'fontsize': 26, 
                'fontweight': 'bold', 
                'loc': 'center', 
                'y': 1.05
            }
        )
        self.ax02_2.axis([-0.08, self.tmax, -0.4, 0.4])  # Set axis limits
        
        self.ax02_3 = self.createAxes(
            self.tabAtr('Ex02Figure'),
            args={
                'pos': 413, 
                # 'name': 'Reflectivity Comparison',
                'xAxName': 'Time (s)', 
                'yAxName': 'Amplitude',
                'grid': True,
                'fontsize': 26, 
                'fontweight': 'bold', 
                'loc': 'center', 
                'y': 1.05
            }
        )
        self.ax02_3.axis([-0.08, self.tmax, -0.4, 0.4])  # Set axis limits
        
        self.ax02_4 = self.createAxes(
            self.tabAtr('Ex02Figure'),
            args={
                'pos': 414, 
                # 'name': 'Reflectivity Comparison',
                'xAxName': 'Time (s)', 
                'yAxName': 'Amplitude',
                'grid': True,
                'fontsize': 26, 
                'fontweight': 'bold', 
                'loc': 'center', 
                'y': 1.05
            }
        )
        self.ax02_4.axis([-0.08, self.tmax, -0.005, 0.005])  # Set axis limits

        
