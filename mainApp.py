
import numpy as np
import sys
import pandas as pd
import geone as gn
from pathlib import Path

from classes.examples import AllExamples
from seismic_examples.all_seismic_examples import AllSeismicExamples

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog

# class MainApp(AllExamples):
class MainApp(AllSeismicExamples):
    def __init__(self):
        super().__init__()

        self.tab18 = self.createTab('Ex18')

        self.__slider = self.createSlider(
            1, 3000, init=3000,
            func=self.updatePoint18, 
            name='Slider value', 
            tab=self.tab18,
            label=True
        )   

        self.__qdial = self.createQDial(
            1, 3000, 3000, 
            func=self.updateScatter18, 
            name='QDial value', 
            tab=self.tab18,
            label=True
        )
        
        self.n18 = 3000
        self.x18 = [np.random.rand() for i in range(self.n18)]
        self.y18 = [np.random.rand() for i in range(self.n18)]
        self.c18 = [np.random.rand() for i in range(self.n18)]
        
        self.drawAxes18()
        self.draw18()
        self.drawColorbar18()

    @AllExamples.canvasDraw(tab='Ex18')
    def drawAxes18(self):
        self.ax18 = self.createAxes(
            self.tabAtr('Ex18Figure'),
            args={
                'pos': 111, 
                'name': 'plot 1',
                'xAxName': 'x', 
                'yAxName': 'y',
                'grid': True
            }
        )
        self.ax18.set_xlim([-0.05, 1.05])
        self.ax18.set_ylim([-0.05, 1.05])
        
    @AllExamples.canvasDraw(tab='Ex18')
    def draw18(self):
        self.scatterArgsEx18 = {
            'x': self.x18,
            'y': self.y18,
            'c': self.c18,
            's': 150,
            'cmap': ListedColormap(["Crimson", "orange", 'lightblue', 'azure', 'coral']),
            'zorder': 4
        }
        self.points18 = self.ax18.scatter(**self.scatterArgsEx18)

    @AllExamples.canvasDraw(tab='Ex18')
    def drawColorbar18(self):
        self.createColorbar(
            self.tabAtr('Ex18Figure'), 
            self.points18, 
            name='Quantiles', 
            cmap=self.scatterArgsEx18['cmap']
        )
        
    def updateScatter18(self, index):
        if self.n18 < index:
            for i in range(index - self.n18):
                self.x18.append(np.random.rand())
                self.y18.append(np.random.rand())
                self.c18.append(np.random.rand())
        else:
            for i in range(self.n18 - index):
                self.x18.pop(1)
                self.y18.pop(1)
                self.c18.pop(1)
        self.n18 = index
        self.points18.remove()
        self.draw18()
        self.tabAtr('QDial value QDial Label').setText(str(index))
        self.tabAtr('Slider value slider').setValue(index)
        self.tabAtr('Slider value Slider Label').setText(str(index))

    # @AllExamples.canvasDraw(tab='Ex18')
    def redraw18(self):
        # self.tabAtr('Ex18Figure').clf()
        # self.draw18()
        
        # self.points18.remove()
        # x = [np.random.rand() for i in range(self.n18)]
        # y = [np.random.rand() for i in range(self.n18)]
        # self.points18.set_offsets(np.c_[x, y])
        pass

    def loadFile18(self):
        pass
    
    def updatePoint18(self, index):
        
        self.tabAtr('QDial value QDial Label').setText(str(index))
        self.tabAtr('QDial value QDial').setValue(index)
        self.tabAtr('Slider value Slider Label').setText(str(index))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # with open("styles/darkTheme.qss", "r") as f:
    with open(Path(__file__).parent.resolve()  / "styles" / "darkTheme.qss", "r") as f:
        style = f.read()
        app.setStyleSheet(style)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())

