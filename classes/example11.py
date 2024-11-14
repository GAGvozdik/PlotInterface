from .interface import PlotInterface
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt

# INTERFACE 11
class Example11(PlotInterface):
    def __init__(self):
        super().__init__()

        self.tab11 = self.createTab('Ex11')
        
        self.drawAxes11()

        self.plotScatter11('data/data1.txt', self.ax11_1)
        self.plotScatter11('data/data2.txt', self.ax11_2)
        self.plotScatter11('data/data3.txt', self.ax11_3)
        self.plotScatter11('data/data4.txt', self.ax11_4)

    def plotScatter11(self, way, ax):
        file = open(way, 'r')
        x, y, V = np.loadtxt(file, unpack=True)
        cmap = LinearSegmentedColormap.from_list("white_to_Crimson", ["white", "Crimson"])
        scatterArgs = {
            'x': x,
            'y': y,
            'c': V,
            's': 150,
            'cmap': cmap,
            'zorder': 2
        }
        plt.sca(ax)
        ax.scatter(**scatterArgs)
    
    def drawAxes11(self):
        
        axArgs = {
            'xAxName': '$x$ [m]', 
            'yAxName': '$y$ [m]'
        }

        axArgs['pos'], axArgs['name'] = 221, 'data1'
        self.ax11_1 = self.createAxes(self.tabAtr('Ex11Figure'), args=axArgs)
        self.ax11_1.set_aspect(1)

        axArgs['pos'], axArgs['name'] = 222, 'data2'
        self.ax11_2 = self.createAxes(self.tabAtr('Ex11Figure'), args=axArgs)
        self.ax11_2.set_aspect(1)

        axArgs['pos'], axArgs['name'] = 223, 'data3'
        self.ax11_3 = self.createAxes(self.tabAtr('Ex11Figure'), args=axArgs)
        self.ax11_3.set_aspect(1)

        axArgs['pos'], axArgs['name'] = 224, 'data4'
        self.ax11_4 = self.createAxes(self.tabAtr('Ex11Figure'), args=axArgs)
        self.ax11_4.set_aspect(1)

