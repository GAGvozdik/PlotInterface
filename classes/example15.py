from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QTabWidget
from PyQt5.QtWidgets import QGridLayout
import numpy as np
import pandas as pd
import geone as gn
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap
from .interface import PlotInterface


class Example15(PlotInterface):
    def __init__(self):
        super().__init__()

        self.tab15 = self.createTab('Ex15')
        self.loadData()

        self.ncla15 = 20
        self.alpha15 = 45

        self.qdial15 = self.createQDial(0, 360, 
            init=self.alpha15, 
            func=self.updateAlpha15, 
            name='Alpha', 
            tab=self.tab15,
            label=True
        )

        self.slider15 = self.createSlider(1, 200, 
            func=self.updatNCLA15, 
            name='NCLA top', 
            tab=self.tab15,
            label=True
        )

        self.drawAxes15()
        self.plot2DirVariogram15()   

    def plot2DirVariogram15(self):

        (hexp1, gexp1, cexp1), (hexp2, gexp2, cexp2) = gn.covModel.variogramExp2D(
            self.xy_data, 
            self.v, 
            alpha=self.alpha15, 
            ncla=(20, self.ncla15), 
            hmax=(10000, 10000), 
            make_plot=False
        )

        self.ax15_1.plot(hexp1, gexp1, 'crimson')
        self.ax15_2.plot(hexp2, gexp2, 'orange')

        self.ax15_3.plot(hexp1, gexp1, 'crimson')
        self.ax15_3.plot(hexp2, gexp2, 'orange')
        
        self.drawArrows15()


    def drawArrows15(self):

        angle_rad = np.radians(-self.alpha15)

        x_end = np.cos(angle_rad)  
        y_end = np.sin(angle_rad)  

        self.ax15_4.arrow(0, 0, 
            x_end, 
            y_end, 
            head_width=0.1, 
            head_length=0.1, 
            linewidth=2, 
            color='crimson', 
            length_includes_head=True,
            zorder=1
        )

        angle_rad = np.radians(-(self.alpha15 + 90))
        x_end = np.cos(angle_rad)  
        y_end = np.sin(angle_rad)  

        self.ax15_4.arrow(0, 0, 
            x_end, 
            y_end, 
            head_width=0.1, 
            head_length=0.1, 
            linewidth=2, 
            color='orange', 
            length_includes_head=True,
            zorder=1
        )

        self.ax15_4.arrow(0, 0, 1, 0, 
            head_width=0.1, 
            head_length=0.1, 
            linewidth=2, 
            color='grey', 
            length_includes_head=True,
            zorder=0
        )

        self.ax15_4.arrow(0, 0, 0, 1, 
            head_width=0.1, 
            head_length=0.1, 
            linewidth=2, 
            color='grey', 
            length_includes_head=True,
            zorder=0
        )



    def loadData(self):
        file = open('data/artic135_subsample.txt', 'r')
        x, y, self.v = np.loadtxt(file, unpack=True)
        self.xy_data = np.array((x, y)).T

    def drawAxes15(self):
        self.ax15_1 = self.createAxes(self.tabAtr('Ex15Figure'), args={'pos': 221})
        self.ax15_1.set_position([0.05, 0.57, 0.4, 0.4]) 
        self.ax15_1.set_xlim(0, 10000)
        self.ax15_1.set_ylim(0, 40000)

        self.ax15_2 = self.createAxes(self.tabAtr('Ex15Figure'), args={'pos': 222})
        self.ax15_2.set_position([0.55, 0.57, 0.4, 0.4]) 
        self.ax15_2.set_xlim(0, 10000)
        self.ax15_2.set_ylim(0, 40000)

        self.ax15_3 = self.createAxes(self.tabAtr('Ex15Figure'), args={'pos': 223})
        self.ax15_3.set_position([0.05, 0.05, 0.4, 0.4]) 
        self.ax15_3.set_xlim(0, 10000)
        self.ax15_3.set_ylim(0, 40000)

        self.ax15_4 = self.createAxes(self.tabAtr('Ex15Figure'), args={'pos': 224})
        self.ax15_4.set_position([0.55, 0.05, 0.4, 0.4]) 
        self.ax15_4.set_aspect(1)
        self.ax15_4.set_xlim(-1.1, 1.1)
        self.ax15_4.set_ylim(-1.1, 1.1)

    @PlotInterface.canvasDraw(tab='Ex15')
    def updatNCLA15(self, ncla):
        self.ncla15 = ncla
        self.tabAtr('Ex15Figure').clf()
        self.drawAxes15()
        self.plot2DirVariogram15()
        self.tabAtr('NCLA top Slider Label').setText(str(ncla))

    @PlotInterface.canvasDraw(tab='Ex15')
    def updateAlpha15(self, alpha):
        self.alpha15 = alpha
        self.tabAtr('Ex15Figure').clf()
        self.drawAxes15()
        self.plot2DirVariogram15()
        self.tabAtr('Alpha QDial Label').setText(str(alpha))


