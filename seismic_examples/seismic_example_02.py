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



class SeismicExample02(PlotInterface):
    def __init__(self):
        super().__init__()



        # Define the input parameters
        self.v = np.array([1000, 2000, 1500, 5000, 7000, 2500])  # Velocity in m/s
        self.rho = np.array([2500, 2700, 2000, 4500, 4800, 2900])  # Density in kg/m^3

        self.__Quality = 50
        # self.__q = np.array([50, 50, 50, 50, 50, 50])  # Quality factor
        self.__q = np.array([self.__Quality for i in range(6)])  # Quality factor
        self.thk = np.array([100, 70, 100, 250, 300])  # Thickness in meters

        self.__dt = 0.011  # Sampling interval in seconds
        self.tmax = 2  # Total modeled time in seconds
        self.__fdom = 20  # Dominant frequency in Hz

        self.__tab = self.createTab('Ex02')

        self.createQDial(
            1, 3000, init=int(10 * self.__fdom),
            func=self.__updateFDom, 
            name='Dominant frequency 2', 
            tab=self.__tab,
            label=True
        )
        self.tabAtr('Dominant frequency 2 QDial Label').setText(str(self.__fdom))

        self.createQDial(
            20, 500, init=int(self.__dt * 10000),
            func=self.__updatedT, 
            name='dT 2', 
            tab=self.__tab,
            label=True
        )
        self.tabAtr('dT 2 QDial Label').setText(str(self.__dt))

        self.createQDial(
            5, 1000, init=50,
            func=self.__updateQuality, 
            name='Quality 2', 
            tab=self.__tab,
            label=True
        )
        self.tabAtr('Quality 2 QDial Label').setText(str(self.__Quality))

        self.__drawAxes()
        self.__draw()

    @PlotInterface.canvasDraw(tab='Ex02')
    def __draw(self):
        self.__ax1.remove()
        self.__ax2.remove()
        self.__ax3.remove()
        self.__ax4.remove()
        self.__drawAxes()

        self.R, self.V, self.RHO, self.__Q, self.THK, self.T = reflec_from_model(self.rho, self.v, self.__q, self.thk, self.__dt, self.tmax)

        self.RM = add_multiples(self.R, type=1, R0=-0.5)
        self.RL = absorption(self.RM, self.__Q, self.__dt, self.__fdom) # do you know why here is RM? 
        self.Rg = add_geometric_spreading(self.RL, self.THK) 

        self.__ax1.plot(self.R, self.T, linewidth=3, color='darkcyan', label='Original Reflectivity')
        self.__ax2.plot(self.RM, self.T, linewidth=3, color='orange', label='Reflectivity with Multiples')
        self.__ax3.plot(self.RL, self.T, linewidth=3, color='Crimson', label='Reflectivity with Multiples and absorption')
        self.__ax4.plot(self.Rg, self.T, linewidth=1, color='mediumseagreen', label='Reflectivity with absorption and geometric_spreading')

    def __updateFDom(self, index):
        self.__fdom = index / 10
        self.__draw()
        self.tabAtr('Dominant frequency 2 QDial Label').setText(str(self.__fdom))

    def __updatedT(self, index):
        self.__dt = index / 10000
        self.__draw()
        self.tabAtr('dT 2 QDial Label').setText(f"{self.__dt:.4f}")

    def __updateQuality(self, index):
        self.__Quality = index
        self.__q = np.array([self.__Quality for i in range(6)])
        self.__draw()
        self.tabAtr('Quality 2 QDial Label').setText(f"{self.__Quality:.0f}")

    @PlotInterface.canvasDraw(tab='Ex02')
    def __drawAxes(self):
        
        self.tabAtr('Ex02Figure').subplots_adjust(
            left=0.07,    
            right=0.92,   
            top=0.92,     
            bottom=0.07,  
            wspace=0.65,   
            hspace=0.4    
        )

        titles = [
            'Original Reflectivity',
            'with Multiples',
            'Multiples & absorption',
            'Absorption & geometric_spreading'
        ]

        axes = []
        for i, title in enumerate(titles, start=1):
            ax = self.createAxes(
                self.tabAtr('Ex02Figure'),
                args={
                    'pos': 140 + i,
                    'name': title,
                    'xAxName': 'Amplitude',
                    'yAxName': 'Time (s)',
                    'grid': True,
                    'fontsize': 26,
                    'fontweight': 'bold',
                    'loc': 'center',
                    'y': 1.05
                }
            )
            ax.axis([-0.4, 0.4, -0.08, self.tmax])
            axes.append(ax)

        self.__ax1, self.__ax2, self.__ax3, self.__ax4 = axes

        self.__ax4.axis([-0.005, 0.005, -0.08, self.tmax])
        self.__ax4.tick_params(axis='both', labelsize=10)







        


