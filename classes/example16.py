from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog
import numpy as np
import sys
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import pandas as pd
import geone as gn
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget
from PyQt5.QtWidgets import QGridLayout
from matplotlib.colors import LinearSegmentedColormap
from pathlib import Path
from .interface import PlotInterface

class Example16(PlotInterface):
    def __init__(self):
        super().__init__()

        self.tab16 = self.createTab('Ex16')

        self.slider16 = self.createSlider(
            1, 3000, init=3000,
            func=self.updatePoint16, 
            name='Parameter 1', 
            tab=self.tab16,
            label=True
        )

        self.qdial16 = self.createQDial(
            1, 3000, 3000, 
            func=self.updateScatter16, 
            name='Number of points', 
            tab=self.tab16,
            label=True
        )

        self.n16 = 3000
        self.x16 = [np.random.rand() for i in range(self.n16)]
        self.y16 = [np.random.rand() for i in range(self.n16)]
        self.c16 = [np.random.rand() for i in range(self.n16)]
        
        self.drawAxes16()
        self.draw16()
        self.drawColorbar16()

    @PlotInterface.canvasDraw(tab='Ex16')
    def drawAxes16(self):
        self.ax16 = self.createAxes(
            self.tabAtr('Ex16Figure'),
            args={
                'pos': 111, 
                'name': 'plot 1',
                'xAxName': 'x', 
                'yAxName': 'y',
                'grid': True
            }
        )
        self.ax16.set_xlim([-0.05, 1.05])
        self.ax16.set_ylim([-0.05, 1.05])
        
    @PlotInterface.canvasDraw(tab='Ex16')
    def draw16(self):
        self.scatterArgsEx16 = {
            'x': self.x16,
            'y': self.y16,
            'c': self.c16,
            's': 150,
            'cmap': ListedColormap(["Crimson", "orange", 'lightblue', 'azure', 'coral']),
            'zorder': 4
        }
        self.points16 = self.ax16.scatter(**self.scatterArgsEx16)

    @PlotInterface.canvasDraw(tab='Ex16')
    def drawColorbar16(self):
        self.createColorbar(
            self.tabAtr('Ex16Figure'), 
            self.points16, 
            name='Quantiles', 
            cmap=self.scatterArgsEx16['cmap']
        )
        
    def updateScatter16(self, index):
        if self.n16 < index:
            for i in range(index - self.n16):
                self.x16.append(np.random.rand())
                self.y16.append(np.random.rand())
                self.c16.append(np.random.rand())
        else:
            for i in range(self.n16 - index):
                self.x16.pop(1)
                self.y16.pop(1)
                self.c16.pop(1)
        self.n16 = index
        self.points16.remove()
        self.draw16()
        self.tabAtr('Number of points QDial Label').setText(str(index))
        self.tabAtr('Parameter 1 slider').setValue(index)
        self.tabAtr('Parameter 1 Slider Label').setText(str(index))

    # @PlotInterface.canvasDraw(tab='Ex16')
    def redraw16(self):
        # self.tabAtr('Ex16Figure').clf()
        # self.draw16()
        
        # self.points16.remove()
        # x = [np.random.rand() for i in range(self.n16)]
        # y = [np.random.rand() for i in range(self.n16)]
        # self.points16.set_offsets(np.c_[x, y])
        pass

    def loadFile16(self):
        pass
    
    def updatePoint16(self, index):
        
        self.tabAtr('Number of points QDial Label').setText(str(index))
        self.tabAtr('Number of points QDial').setValue(index)
        self.tabAtr('Parameter 1 Slider Label').setText(str(index))



