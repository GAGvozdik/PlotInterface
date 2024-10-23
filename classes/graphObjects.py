import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QGridLayout, QGroupBox, QDial
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure 
from matplotlib.colors import ListedColormap
import geone as gn
import pandas as pd
import matplotlib.pyplot as plt

class GraphObjects(QWidget):
    def __init__(self):
        super().__init__()  

    def createColorbar(self, fig, scatter, name='', cmap='none'):
        
        if cmap != 'none':
            cbar = fig.colorbar(scatter, cmap=cmap, fraction=0.05, pad=0.09) 
        else:
            cbar = fig.colorbar(scatter, fraction=0.05, pad=0.09) 

        cbar.outline.set_edgecolor(self.widgetColor)
        cbar.outline.set_linewidth(3) 
        cbar.ax.tick_params(labelcolor=self.ticksColor, labelsize=15, width=3, length=6, color=self.widgetColor)
        cbar.ax.set_ylabel(name, color=self.ticksColor, fontsize=18)

        return cbar

    def plotLine(self, ax,
            args = {
                'x': None,
                'y': None,
                'type': '-b',
                'color': 'orange',
                'lineWidth': 2.5,
                'zorder': 0,
            }):
        line, = ax.plot(**args)
        return line

    def plotScatter(self, ax,
            args = {
                'x': None,
                'y': None,
                'c': 'Crimson',
                'zorder': None,
                's': 80,
                'cmap': None
            }):
        return ax.scatter(**args)
    
    def createAxes(self, fig, 
            args={
                'pos': None, 
                'name': '', 
                'xAxName': '', 
                'yAxName': '',  
                'grid': False
            }):

        ax = fig.add_subplot(args['pos'])
        ax.set_title(args['name'], color=self.ticksColor, fontsize = 20, y=1.02)
        ax.set_xlabel(args['xAxName'], color=self.ticksColor, fontsize = 15)
        ax.set_ylabel(args['yAxName'], color=self.ticksColor, fontsize = 15)
        ax.set_facecolor(self.graphColor)
        
        ax.spines[:].set_color(self.widgetColor)
        ax.spines[:].set_linewidth(3.5)

        ax.tick_params(axis='x', labelcolor=self.ticksColor, color=self.widgetColor, width=2.5, length=6, labelsize=12) 
        ax.tick_params(axis='y', labelcolor=self.ticksColor, color=self.widgetColor, width=2.5, length=6, labelsize=12)

        if args['grid']:
            ax.grid(True, color=self.widgetColor)

        return ax
    
    def create3DAxes(self, fig, 
            args={
                'pos': None, 
                'name': '', 
                'xAxName': '', 
                'yAxName': '',  
                'grid': False,
                'projection': '3d'
            }):

        ax = fig.add_subplot(args['pos'], projection=args['projection'])
    
        ax.set_facecolor('#2e2e2e')
        
        ax.spines[:].set_color(self.widgetColor)
        ax.spines[:].set_linewidth(3.5)

        ax.tick_params(axis='x', labelcolor=self.ticksColor, color=self.widgetColor, width=2.5, length=6, labelsize=12) 
        ax.tick_params(axis='y', labelcolor=self.ticksColor, color=self.widgetColor, width=2.5, length=6, labelsize=12)
        ax.tick_params(axis='z', labelcolor=self.ticksColor, color=self.widgetColor, width=2.5, length=6, labelsize=12)

        ax.xaxis.set_pane_color('#4e4e4e') 
        ax.yaxis.set_pane_color('#4e4e4e') 
        ax.zaxis.set_pane_color('#4e4e4e') 

        return ax
    
    def createPolarAxes(self, fig, pos):
        ax = fig.add_subplot(pos, projection='polar')
    
        ax.set_facecolor(self.windowColor)
        ax.set_xlabel('', color=self.ticksColor, fontsize = 15)
        ax.set_ylabel('', color=self.ticksColor, fontsize = 15)
        
        ax.spines[:].set_color(self.widgetColor)
        ax.spines[:].set_linewidth(3.5)

        ax.tick_params(axis='x', labelcolor=self.ticksColor, color=self.widgetColor, width=2.5, length=6, labelsize=12) 
        ax.tick_params(axis='y', labelcolor=self.ticksColor, color=self.widgetColor, width=2.5, length=6, labelsize=12)

        return ax
    
    def createFigure(self, name, canvasBox):
        figure = plt.figure()
        figure.patch.set_facecolor(self.windowColor)
        figure.subplots_adjust(wspace=0.4, hspace=0.5)

        canvas = FigureCanvas(figure)
        self.addToBox(canvasBox, canvas)

        return figure, canvas
    
    def canvasDraw(tab):
        def decorator(func):
            def wrapper(self, *args, **kwargs):
                result = func(self, *args, **kwargs)
                self.tabAtr(f'{tab}Canvas').draw()  
                return result
            return wrapper
        return decorator