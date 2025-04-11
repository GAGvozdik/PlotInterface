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

# INTERFACE 3
class SeismicExample03(PlotInterface):
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


        self.tab03 = self.createTab('Ex03')

        self.slider03 = self.createSlider(
            1, 3000, init=int(10 * self.fdom),
            func=self.updateFDom03, 
            name='Dominant frequency 2', 
            tab=self.tab03,
            label=True
        )
        self.tabAtr('Dominant frequency 2 Slider Label').setText(str(self.fdom))
        
        self.slider03 = self.createSlider(
            20, 500, init=int(self.dt * 10000),
            func=self.updatedT03, 
            name='dT 2', 
            tab=self.tab03,
            label=True
        )
        self.tabAtr('dT 2 Slider Label').setText(str(self.dt))
        

        self.drawAxes03()
        self.draw03()

        
    @PlotInterface.canvasDraw(tab='Ex03')
    def draw03(self):
        self.ax03_1.remove()
        self.ax03_2.remove()
        self.ax03_3.remove()
        self.ax03_4.remove()
        self.drawAxes03()
        
        # Call the reflec_from_model function
        self.R, self.V, self.RHO, self.Q, self.THK, self.T = reflec_from_model(self.rho, self.v, self.q, self.thk, self.dt, self.tmax)

        # Call the add_multiples function
        self.RM = add_multiples(self.R, type=1, R0=-0.5)
        
        self.RL = absorption(self.RM, self.Q, self.dt, self.fdom) # do you know why here is RM? 

        self.Rg = add_geometric_spreading(self.RL, self.THK) 

        # Plot the original reflectivity signal
        self.ax03_1.plot(self.R, self.T, linewidth=3, color='darkcyan', label='Original Reflectivity')

        # Plot the original and modified reflectivity signals
        self.ax03_2.plot(self.RM, self.T, linewidth=3, color='orange', label='Reflectivity with Multiples')

        self.ax03_3.plot(self.RL, self.T, linewidth=3, color='Crimson', label='Reflectivity with Multiples and absorption')
        
        self.ax03_4.plot(self.Rg, self.T, linewidth=1, color='mediumseagreen', label='Reflectivity with absorption and geometric_spreading')
        
        # self.ax03_1.legend(loc=4, fontsize=17)
        # self.ax03_2.legend(loc=4, fontsize=17)
        # self.ax03_3.legend(loc=4, fontsize=17)
        # self.ax03_4.legend(loc=4, fontsize=17)
        

    def updateFDom03(self, index):
        self.fdom = index / 10
        self.draw03()
        self.tabAtr('Dominant frequency 2 Slider Label').setText(str(self.fdom))
        
    def updatedT03(self, index):
        self.dt = index / 10000
        print(self.dt)
        self.draw03()
        self.tabAtr('dT 2 Slider Label').setText(f"{self.dt:.4f}")

    @PlotInterface.canvasDraw(tab='Ex03')
    def drawAxes03(self):
        # self.tabAtr('Ex03Figure').tight_layout(pad=0, w_pad=0, h_pad=0, rect=[0, 0, 1, 1])
        self.tabAtr('Ex03Figure').subplots_adjust(
            left=0.07,    # немного отступ слева
            right=0.92,   # немного отступ справа
            top=0.92,     # немного отступ сверху
            bottom=0.07,  # немного отступ снизу
            wspace=0.65,   # расстояние между subplot'ами по ширине
            hspace=0.4    # расстояние между subplot'ами по высоте
        )

        self.ax03_1 = self.createAxes(
            self.tabAtr('Ex03Figure'),
            args={
                'pos': 141, 
                'name': 'Original Reflectivity',
                'xAxName': 'Amplitude',
                'yAxName': 'Time (s)', 
                'grid': True,
                'fontsize': 26, 
                'fontweight': 'bold', 
                'loc': 'center', 
                'y': 1.05
            }
        )
        self.ax03_1.axis([-0.4, 0.4,-0.08, self.tmax])  # Set axis limits
        # self.ax03_1.axis([-0.08, self.tmax, -1, 1])  # Set axis limits
        # self.ax03_1.set_ylim([-1, 1])
        # self.ax03_1.set_xlim([-0.08, 2.9])
        
        self.ax03_2 = self.createAxes(
            self.tabAtr('Ex03Figure'),
            args={
                'pos': 142, 
                'name': 'with Multiples',
                'xAxName': 'Amplitude',
                'yAxName': 'Time (s)', 
                'grid': True,
                'fontsize': 26, 
                'fontweight': 'bold', 
                'loc': 'center', 
                'y': 1.05
            }
        )
        self.ax03_2.axis([-0.4, 0.4,-0.08, self.tmax])  # Set axis limits
        
        self.ax03_3 = self.createAxes(
            self.tabAtr('Ex03Figure'),
            args={
                'pos': 143, 
                'name': 'Multiples & absorption',
                'xAxName': 'Amplitude',
                'yAxName': 'Time (s)', 
                'grid': True,
                'fontsize': 26, 
                'fontweight': 'bold', 
                'loc': 'center', 
                'y': 1.05
            }
        )
        self.ax03_3.axis([-0.4, 0.4,-0.08, self.tmax])  # Set axis limits
        
        self.ax03_4 = self.createAxes(
            self.tabAtr('Ex03Figure'),
            args={
                'pos': 144, 
                'name': 'Absorption & geometric_spreading',
                'xAxName': 'Amplitude',
                'yAxName': 'Time (s)', 
                'grid': True,
                'fontsize': 26, 
                'fontweight': 'bold', 
                'loc': 'center', 
                'y': 1.05
            }
        )
        self.ax03_4.axis([-0.005, 0.005, -0.08, self.tmax])  # Set axis limits
        self.ax03_4.tick_params(axis='both', labelsize=10)

        
