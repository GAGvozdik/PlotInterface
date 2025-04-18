
import numpy as np
import sys
import pandas as pd
import geone as gn
from pathlib import Path
import os

from classes.examples import AllExamples
from seismic_examples.all_seismic_examples import AllSeismicExamples

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# class MainApp(AllExamples):
class MainApp(AllSeismicExamples, AllExamples):
    def __init__(self):
        super().__init__()

        self.__tab = self.createTab('Test')

        self.createSlider(
            1, 3000, init=3000,
            func=self.__updatePoint, 
            name='Slider value', 
            tab=self.__tab,
            label=True
        )   

        self.createQDial(
            1, 3000, 3000, 
            func=self.__updateScatter, 
            name='QDial value', 
            tab=self.__tab,
            label=True
        )
        
        self.__n = 3000
        self.__x = [np.random.rand() for i in range(self.__n)]
        self.__y = [np.random.rand() for i in range(self.__n)]
        self.__c = [np.random.rand() for i in range(self.__n)]
        
        self.__drawAxes()
        self.__draw()
        self.__drawColorbar()

    @AllExamples.canvasDraw(tab='Test')
    def __drawAxes(self):
        self.__ax = self.createAxes(
            self.tabAtr('TestFigure'),
            args={
                'pos': 111, 
                'name': 'plot 1',
                'xAxName': 'x', 
                'yAxName': 'y',
                'grid': True
            }
        )
        self.__ax.set_xlim([-0.05, 1.05])
        self.__ax.set_ylim([-0.05, 1.05])
        
    @AllExamples.canvasDraw(tab='Test')
    def __draw(self):
        self.__scatterArgsEx = {
            'x': self.__x,
            'y': self.__y,
            'c': self.__c,
            's': 150,
            'cmap': ListedColormap(["Crimson", "orange", 'lightblue', 'azure', 'coral']),
            'zorder': 4
        }
        self.__points = self.__ax.scatter(**self.__scatterArgsEx)

    @AllExamples.canvasDraw(tab='Test')
    def __drawColorbar(self):
        self.createColorbar(
            self.tabAtr('TestFigure'), 
            self.__points, 
            name='Quantiles', 
            cmap=self.__scatterArgsEx['cmap']
        )
        
    def __updateScatter(self, index):
        if self.__n < index:
            for i in range(index - self.__n):
                self.__x.append(np.random.rand())
                self.__y.append(np.random.rand())
                self.__c.append(np.random.rand())
        else:
            for i in range(self.__n - index):
                self.__x.pop(1)
                self.__y.pop(1)
                self.__c.pop(1)
        self.__n = index
        self.__points.remove()
        self.__draw()
        self.tabAtr('QDial value QDial Label').setText(str(index))
        self.tabAtr('Slider value slider').setValue(index)
        self.tabAtr('Slider value Slider Label').setText(str(index))

    # @AllExamples.canvasDraw(tab='Test')
    def __redraw(self):
        # self.tabAtr('TestFigure').clf()
        # self.__draw()
        
        # self.__points.remove()
        # x = [np.random.rand() for i in range(self.n18)]
        # y = [np.random.rand() for i in range(self.n18)]
        # self.__points.set_offsets(np.c_[x, y])
        pass

    def __loadFile(self):
        pass
    
    def __updatePoint(self, index):
        
        self.tabAtr('QDial value QDial Label').setText(str(index))
        self.tabAtr('QDial value QDial').setValue(index)
        self.tabAtr('Slider value Slider Label').setText(str(index))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    with open(Path(__file__).parent.resolve()  / "styles" / "darkTheme.qss", "r") as f:
        style = f.read()
        app.setStyleSheet(style)
        
    # with open(resource_path("styles/darkTheme.qss"), "r") as f:
    #     app.setStyleSheet(f.read())
    
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
    
    

