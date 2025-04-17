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

    def createFigure(self, name, parentBox):
        figure = plt.figure()
        figure.patch.set_facecolor(self.windowColor)
        figure.subplots_adjust(wspace=0.4, hspace=0.5)

        canvas = FigureCanvas(figure)
        canvas.setStyleSheet(f"background-color: {self.graphColor};")

        parentBox.layout().addWidget(canvas)
        return figure, canvas

    def createAxes(self, fig, args):
        ax = fig.add_subplot(args.get('pos', 111))
        ax.set_title(args.get('name', ''), color=self.ticksColor, fontsize=20, y=1.02)
        ax.set_xlabel(args.get('xAxName', ''), color=self.ticksColor, fontsize=15)
        ax.set_ylabel(args.get('yAxName', ''), color=self.ticksColor, fontsize=15)
        ax.set_facecolor(self.graphColor)
        
        ax.spines[:].set_color(self.widgetColor)
        ax.spines[:].set_linewidth(2.5)
        
        ax.tick_params(axis='both', labelcolor=self.ticksColor, color=self.widgetColor, width=self.ticksWidth, length=6, labelsize=12)
        if args.get('grid', False):
            ax.grid(True, color=self.gridColor)
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
        ax.set_facecolor(self.windowColor)
        
        ax.spines[:].set_color(self.widgetColor)
        ax.spines[:].set_linewidth(3.5)

        ax.tick_params(axis='x', labelcolor=self.ticksColor, color=self.widgetColor, width=self.ticksWidth, length=6, labelsize=12) 
        ax.tick_params(axis='y', labelcolor=self.ticksColor, color=self.widgetColor, width=self.ticksWidth, length=6, labelsize=12)
        ax.tick_params(axis='z', labelcolor=self.ticksColor, color=self.widgetColor, width=self.ticksWidth, length=6, labelsize=12)

        ax.xaxis.set_pane_color(self.windowColor) 
        ax.yaxis.set_pane_color(self.windowColor) 
        ax.zaxis.set_pane_color(self.windowColor) 

        return ax
    
    def createPolarAxes(self, fig, pos):
        ax = fig.add_subplot(pos, projection='polar')
    
        ax.set_facecolor(self.windowColor)
        ax.set_xlabel('', color=self.ticksColor, fontsize = 15)
        ax.set_ylabel('', color=self.ticksColor, fontsize = 15)
        
        ax.spines[:].set_color(self.widgetColor)
        ax.spines[:].set_linewidth(3.5)

        ax.tick_params(axis='x', labelcolor=self.ticksColor, color=self.widgetColor, width=self.ticksWidth, length=6, labelsize=12) 
        ax.tick_params(axis='y', labelcolor=self.ticksColor, color=self.widgetColor, width=self.ticksWidth, length=6, labelsize=12)

        return ax
    
    def createColorbar(self, fig, scatter, name='', cmap='none'):
        
        if cmap != 'none':
            cbar = fig.colorbar(scatter, cmap=cmap, fraction=0.05, pad=0.09) 
        else:
            cbar = fig.colorbar(scatter, fraction=0.05, pad=0.09) 

        cbar.outline.set_edgecolor(self.widgetColor)
        cbar.outline.set_linewidth(self.ticksWidth) 
        cbar.ax.tick_params(labelcolor=self.ticksColor, labelsize=15, width=self.ticksWidth, length=6, color=self.widgetColor)
        cbar.ax.set_ylabel(name, color=self.ticksColor, fontsize=18)

        return cbar
    
    def canvasDraw(tab):
        def decorator(func):
            def wrapper(self, *args, **kwargs):
                result = func(self, *args, **kwargs)
                self.tabAtr(f'{tab}Canvas').draw()  
                return result
            return wrapper
        return decorator
    
