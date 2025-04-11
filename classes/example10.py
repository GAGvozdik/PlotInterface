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
from pathlib import Path

class Example10(PlotInterface):
    def __init__(self):
        super().__init__()

        self.tab10 = self.createTab('Ex10')

        self.qdial10_1 = self.createQDial(1, 200, 80, func=self.updateAnis, name='anis', tab=self.tab10, label=True)
        self.qdial10_2 = self.createQDial(1, 200, 0.5, func=self.updateNugget, name='nugget', tab=self.tab10, label=True)
        self.qdial10_3 = self.createQDial(1, 99, 80, func=self.updateRange, name='range', tab=self.tab10, label=True)

        self.rangeOfEX = 80
        self.nugget = 0.5
        self.anis = 80

        self.redraw()

    @PlotInterface.getWorkTime('updateAnis')
    @PlotInterface.canvasDraw(tab='Ex10')
    def updateAnis(self, anis):
        self.anis = anis       
        self.tabAtr('anis QDial Label').setText(str(self.anis))
        self.redraw()

    @PlotInterface.canvasDraw(tab='Ex10')
    def updateNugget(self, nugget):
        self.nugget = nugget / 10   
        self.tabAtr('nugget QDial Label').setText(str(self.nugget))
        self.redraw()

    @PlotInterface.canvasDraw(tab='Ex10')
    def updateRange(self, rangeOfEX):
        self.rangeOfEX = rangeOfEX  
        self.tabAtr('range QDial Label').setText(str(self.rangeOfEX)  )
        self.redraw()


    def redraw(self):
        
        self.tabAtr('Ex10Figure').clf()
        self.drawAxes()

        cov_model_sph1 = gn.covModel.CovModel2D(
            elem=[
                ('spherical', {'w':10.0, 'r':[80, 80]}),   
                ('nugget', {'w':0.0})                     
            ], 
            alpha=0.0, 
            name='spherical'
        )

        cov_model_sph2 = gn.covModel.CovModel2D(
            elem=[
                ('spherical', {'w':10.0, 'r':[self.rangeOfEX, self.anis]}),   
                ('nugget', {'w':self.nugget})                     
            ], 
            alpha=0.0, 
            name='gaussian'
        )
        
        # 0.23
        nx, ny = 400, 420  
        dx, dy = 0.5, 0.5  
        ox, oy = 0.0, 0.0  
        
        np.random.seed(444)

        sph1 = gn.grf.grf2D(cov_model_sph1, (nx, ny), (dx, dy), (ox, oy), nreal=1) 
        sph2 = gn.grf.grf2D(cov_model_sph2, (nx, ny), (dx, dy), (ox, oy), nreal=1) 

        plt.sca(self.ax10_1)

        # 0.07
        cov_model_sph1.plot_model_one_curve(main_axis=1, vario=True, label="$x$ and $y$ model#1, $x$ model#2 ", hmax=90)
        cov_model_sph2.plot_model_one_curve(main_axis=2, vario=True, label="$y$ model#2", hmax=90)
        self.ax10_1.set_ylim((0,21))
        
        vmin = -15 #np.min((np.min(sph), np.min(gau)))
        vmax = +15 #np.min((np.max(sph), np.max(gau)))

        plt.sca(self.ax10_2)

        self.im_sph1 = gn.img.Img(nx, ny, 1, dx, dy, 1., ox, oy, 0., nv=1, val=sph1)
        self.m = gn.imgplot.drawImage2D(self.im_sph1, cmap='terrain', vmin=vmin, vmax=vmax)

        plt.sca(self.ax10_3)
 
        self.im_sph2 = gn.img.Img(nx, ny, 1, dx, dy, 1., ox, oy, 0., nv=1, val=sph2)                                                                     
        gn.imgplot.drawImage2D(self.im_sph2, cmap='terrain', vmin=vmin, vmax=vmax)

    def drawAxes(self):

        axArgs = {
            'xAxName': 'x', 
            'yAxName': 'y',
            'grid': True
        }
        
        axArgs['pos'], axArgs['name'] = 131, "$\\neq$ range along $x$ and $y$ \n(same other param.)"
        self.ax10_1 = self.createAxes(self.tabAtr('Ex10Figure'), args=axArgs)
        self.ax10_1.set_position([0.36, 0.0, 0.35, 0.4]) 
        
        axArgs['pos'], axArgs['name'] = 132, 'default model'
        self.ax10_2 = self.createAxes(self.tabAtr('Ex10Figure'), args=axArgs)
        self.ax10_2.set_position([0.55, 0.55, 0.4, 0.4]) 

        axArgs['pos'], axArgs['name'] = 133, 'model 2'
        self.ax10_3 = self.createAxes(self.tabAtr('Ex10Figure'), args=axArgs)
        self.ax10_3.set_position([0.05, 0.55, 0.4, 0.4])

        

        

        

