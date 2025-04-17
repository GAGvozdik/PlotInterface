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

        np.random.seed(10)
        self.__dt = 0.001
        self.__tmax = 0.1
        self.__fdom = 20

        self.__rho = (np.random.rand(50, 1) * 4 + 2) * 1000  
        self.__v = np.random.rand(50, 1) * 1000 + 2000  
        self.__q = np.random.rand(50, 1) * 90 + 10  
        self.__thk = np.random.rand(49, 1) * 5 + 25  
        self.__leftx = 2
        self.__tab = self.createTab('Ex03')

        self.createSlider(
            25, 3000, init=int(10 * self.__fdom),
            func=self.__updateFDom, 
            name='Dominant frequency 3', 
            tab=self.__tab,
            label=True
        )
        self.tabAtr('Dominant frequency 3 Slider Label').setText(str(self.__fdom))
        
        self.createSlider(
            10, 500, init=int(self.__dt * 10000),
            func=self.__updatedT, 
            name='dT 3', 
            tab=self.__tab,
            label=True
        )
        self.tabAtr('dT 3 Slider Label').setText(str(self.__dt))
        
        self.createSlider(
            5, 100, init=int(self.__leftx * 50),
            func=self.__updatedLeftX, 
            name='Left Xlim 3', 
            tab=self.__tab,
            label=True
        )
        self.tabAtr('Left Xlim 3 Slider Label').setText(str(self.__leftx))
        
        self.__drawAxes()
        self.__draw()
        

    @PlotInterface.canvasDraw(tab='Ex03')
    def __draw(self):
        self.__ax1.remove()
        self.__ax2.remove()
        self.__drawAxes()
                
        self.__ax1.axis([-0.55, 0.55, 0, self.__leftx])
        self.__ax2.axis([-0.55, 0.55, 0, self.__leftx])
        
        self.__wavem, self.__t_caus = wavemin(self.__dt, self.__fdom, self.__tmax)
        self.__R, self.__V, self.__RHO, self.__Q, self.__THK, self.__T = reflec_from_model(self.__rho, self.__v, self.__q, self.__thk, self.__dt, self.__tmax)
        # R = add_multiples(R, type=1, R0=-0.5)
        # Rloss = add_transmission_lossed(R, R0 = 0) 
        
        # self.__fdom = 20  
        self.__RL = absorption(self.__R, self.__Q, self.__dt, self.__fdom)
        self.__Rg = add_geometric_spreading(self.__RL, self.__THK) 

        self.__RASW = convm(self.__R, self.__wavem)

        self.__ax1.plot(self.__R, self.__T, linewidth=3, color='darkcyan', label='Original Reflectivity')
        self.__ax2.plot(self.__RASW, self.__T, linewidth=3, color='orange', label='Reflectivity with convolution')

        
    def __updatedLeftX(self, index):
        self.__leftx = index / 50
        self.__draw()
        self.tabAtr('Left Xlim 3 Slider Label').setText(str(self.__leftx))
        
        
    def __updateFDom(self, index):
        self.__fdom = index / 10
        self.__draw()
        self.tabAtr('Dominant frequency 3 Slider Label').setText(str(self.__fdom))
        
    def __updatedT(self, index):
        self.__dt = index / 10000
        self.__draw()
        self.tabAtr('dT 3 Slider Label').setText(f"{self.__dt:.4f}")


    @PlotInterface.canvasDraw(tab='Ex03')
    def __drawAxes(self):
        
        self.tabAtr('Ex03Figure').subplots_adjust(
            left=0.07,    
            right=0.92,   
            top=0.92,     
            bottom=0.07,  
            wspace=0.65,   
            hspace=0.4    
        )

        titles = [
            'Original Reflectivity',
            'Reflectivity with convolution'
        ]

        axes = []
        for i, title in enumerate(titles, start=1):
            ax = self.createAxes(
                self.tabAtr('Ex03Figure'),
                args={
                    'pos': 120 + i,  
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
            # ax.axis([-0.4, 0.4, -0.08, self.tmax])
            ax.axis([-0.55, 0.5, 0, 2])  # Set axis limits
            axes.append(ax)

        self.__ax1, self.__ax2 = axes
