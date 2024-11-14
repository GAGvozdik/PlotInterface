from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog
import numpy as np
import geone as gn
from matplotlib.colors import LinearSegmentedColormap
from .interface import PlotInterface
import matplotlib.pyplot as plt

class Example14(PlotInterface):
    def __init__(self):
        super().__init__()
        
        self.hmax14 = 20000
        self.ncla14 = 30
        
        self.tab14 = self.createTab('Ex14')
        
        self.loadButton = QPushButton("Load file")
        self.loadButton.clicked.connect(self.loadFile)
        self.addToBox(self.tabAtr('Ex14SliderBox'), self.loadButton)


        self.drawAxes14()


    def loadFile(self):
        self.x, self.y, self.v = self.load_file()
        self.xy_data = np.array((self.x, self.y)).T

        self.plotScatter14()
        self.plotVariogram14()
        self.plotHist()
        self.plotVariogramRose14()
        
        self.tabAtr('Ex14Canvas').draw()

    def plotScatter14(self):
        cmap = LinearSegmentedColormap.from_list("white_to_Crimson", ["white", "Crimson"])
        self.scatterArgs14 = {
            'x': self.x,
            'y': self.y,
            'c': self.v,
            's': 100,
            'cmap': cmap,
            'zorder': 2
        }
        self.scatter5 = self.ax14_1.scatter(**self.scatterArgs14)

    def plotHist(self):
        self.hist14 = self.ax14_3.hist(self.v, bins=25, color='Crimson', zorder=2, edgecolor="black")


    def plotVariogram14(self):
        plt.sca(self.ax14_2)
        hexp_raw, gexp_raw, cexp_raw = gn.covModel.variogramExp1D(
            self.xy_data, self.v, 
            ncla=self.ncla14, 
            make_plot=False, 
            hmax=self.hmax14, 
            label='Variogr'
        )
        self.ax14_2.plot(hexp_raw, gexp_raw)


    def plotVariogramRose14(self):
        plt.sca(self.ax14_4)
        self.rose14 = gn.covModel.variogramExp2D_rose(
            self.xy_data, 
            self.v, 
            set_polar_subplot=False,
            r_max=30000, 
            r_ncla=12, 
            phi_ncla=12,
            cmap="viridis"
        )

    def drawAxes14(self):
        self.ax14_1 = self.createAxes(self.tabAtr('Ex14Figure'), args={'pos': 221})
        self.ax14_2 = self.createAxes(self.tabAtr('Ex14Figure'), args={'pos': 222})
        self.ax14_3 = self.createAxes(self.tabAtr('Ex14Figure'), args={'pos': 223})
        self.ax14_4 = self.createPolarAxes(self.tabAtr('Ex14Figure'), 224)
    


# a 3
# b 1
# c 2
# d 4

# range of data2 > rage data 1