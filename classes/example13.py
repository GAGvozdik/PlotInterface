from PyQt5.QtWidgets import QApplication
import numpy as np
import sys
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import pandas as pd
import geone as gn
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure 
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget
from PyQt5.QtWidgets import QGridLayout
from .interface import PlotInterface

class Example13(PlotInterface):
    def __init__(self):
        super().__init__()


        self.tab13 = self.createTab('Ex13')

        self.slider13_1 = self.createSlider(1, 99, func=self.updateNCLA13, name='ncla', tab=self.tab13, label=True)
        self.slider13_2 = self.createSlider(1, 99, func=self.updateHMAX13, name='hmax', tab=self.tab13, label=True)

        self.hmax13 = 30
        self.ncla13 = 13

        self.redraw13()


    def drawOneVar(self, way, ax, name):

        file = open(way, 'r')
        x, y, v = np.loadtxt(file, unpack=True)
        xy_data = np.array((x, y)).T

        hexp_raw, gexp_raw, cexp_raw = gn.covModel.variogramExp1D(
            xy_data, 
            v, 
            ncla=self.ncla13, 
            make_plot=False, 
            hmax=self.hmax13
        )

        ax.plot(hexp_raw, gexp_raw, label=name)

    @PlotInterface.canvasDraw(tab='Ex13')
    def redraw13(self):
        
        self.tabAtr('Ex13Figure').clf()
        self.drawAxes13()

        self.drawOneVar('data/data1.txt', self.ax13_1, 'data 1')
        self.drawOneVar('data/data2.txt', self.ax13_1, 'data 2')
        self.drawOneVar('data/data3.txt', self.ax13_1, 'data 3')
        self.drawOneVar('data/data4.txt', self.ax13_1, 'data 4')

        self.ax13_1.legend(loc=1, fontsize=20, markerscale=2)


    def drawAxes13(self):
        self.ax13_1 = self.createAxes(self.tabAtr('Ex13Figure'),
            args={
                'pos': 111, 
                'name': 'Experimental variogram',
                'xAxName': '$x$ [m]', 
                'yAxName': '$y$ [m]',
                'grid': True
            }
        )
        self.ax13_1.set_ylim(0, 1.4)


    def updateNCLA13(self, ncla):
        self.hmax13 = 30
        self.ncla13 = ncla
        self.redraw13()
        self.tabAtr('ncla Slider Label').setText(str(ncla))

    def updateHMAX13(self, hmax):
        self.hmax13 = hmax
        self.redraw13()
        self.tabAtr('hmax Slider Label').setText(str(hmax))


