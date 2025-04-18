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
class SeismicExample04(PlotInterface):
    def __init__(self):
        super().__init__()

        np.random.seed(10)
        self.__dt = 0.001
        self.__tmax = 0.1
        self.__fdom = 20
        self.__leftx = 0.1
        
        self.__tab = self.createTab('Ex04')

        self.createSlider(
            25, 3000, init=int(10 * self.__fdom),
            func=self.__updateFDom, 
            name='Dominant frequency 4', 
            tab=self.__tab,
            label=True
        )
        self.tabAtr('Dominant frequency 4 Slider Label').setText(str(self.__fdom))
        
        self.createSlider(
            10, 500, init=int(self.__dt * 10000),
            func=self.__updatedT, 
            name='dT 4', 
            tab=self.__tab,
            label=True
        )
        self.tabAtr('dT 4 Slider Label').setText(str(self.__dt))
        
        self.createSlider(
            1, 20, init=int(self.__leftx * 100),
            func=self.__updatedLeftX, 
            name='Left Xlim 4', 
            tab=self.__tab,
            label=True
        )
        self.tabAtr('Left Xlim 4 Slider Label').setText(str(self.__leftx))
        
        self.__drawAxes()
        self.__draw()
        

    @PlotInterface.canvasDraw(tab='Ex04')
    def __draw(self):
        self.__ax1.remove()
        self.__ax2.remove()
        self.__ax3.remove()
        self.__drawAxes()
        
        # Set random seed
        np.random.seed(10)
        self.__ax1.axis([-0.7, 0.7, 0, self.__leftx])
        self.__ax2.axis([-0.7, 0.7, 0, self.__leftx])
        self.__ax3.axis([-0.7, 0.7, 0, self.__leftx])
        
        self.__t_caus = np.arange(0, self.__tmax, self.__dt)
        self.__wavem = np.exp(-(np.pi * self.__fdom * self.__t_caus) ** 2) * np.sin(2 * np.pi * self.__fdom * self.__t_caus)  # Ricker-like wavelet

        # Normalize wavelet to avoid numerical issues
        self.__wavem = self.__wavem / np.max(np.abs(self.__wavem))

        # Generate reflectivity series
        self.__T = np.arange(0, self.__tmax, self.__dt)
        self.__R = np.zeros_like(self.__T)
        self.__R[::10] = np.random.rand(len(self.__R[::10])) * 0.8 - 0.4  # Random spikes every 10 samples

        # Convolve with wavelet (add some noise to make it realistic)
        self.__RASW = convolve(self.__R, self.__wavem, mode='same')
        self.__RASW = self.__RASW[:len(self.__T)]  # Ensure same length
        #RASW += np.random.normal(0, 0.01, len(RASW))  # Add noise

        self.__wiener_result = wiener_deconvolution(self.__RASW, self.__wavem, noise_level=0.00)

        self.__ax1.plot(self.__R, self.__T, linewidth=3, color='darkcyan', label='Original Reflectivity')
        self.__ax2.plot(self.__RASW, self.__T, linewidth=3, color='orange', label='Convolved Reflectivity')
        self.__ax3.plot(self.__wiener_result, self.__T, linewidth=3, color='Crimson', label='Wiener Deconvolution')

        
    def __updatedLeftX(self, index):
        self.__leftx = index / 100
        self.__draw()
        self.tabAtr('Left Xlim 4 Slider Label').setText(str(self.__leftx))
        
        
    def __updateFDom(self, index):
        self.__fdom = index / 10
        self.__draw()
        self.tabAtr('Dominant frequency 4 Slider Label').setText(str(self.__fdom))
        
    def __updatedT(self, index):
        self.__dt = index / 10000
        self.__draw()
        self.tabAtr('dT 4 Slider Label').setText(f"{self.__dt:.4f}")


    @PlotInterface.canvasDraw(tab='Ex04')
    def __drawAxes(self):
        
        self.tabAtr('Ex04Figure').subplots_adjust(
            left=0.07,    
            right=0.92,   
            top=0.92,     
            bottom=0.07,  
            wspace=0.65,   
            hspace=0.4    
        )

        titles = [
            'Original Reflectivity',
            'Convolved Output (with noise)',
            'Deconvolution Results'
        ]

        axes = []
        for i, title in enumerate(titles, start=1):
            ax = self.createAxes(
                self.tabAtr('Ex04Figure'),
                args={
                    'pos': 130 + i,  
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
            ax.axis([-0.7, 0.7, 0, self.__leftx])  # Set axis limits
            axes.append(ax)

        self.__ax1, self.__ax2, self.__ax3 = axes




        


