from interface import PlotInterface
from PyQt5.QtWidgets import QApplication
import numpy as np
import sys
import matplotlib.cm as cm
import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# INTERFACE 1
class Example1(PlotInterface):
    def __init__(self):
        super().__init__()

        self.tab1 = self.createTab('Ex1')
        self.slider1 = self.createSlider(0, 500, 1, func=self.updatePoint, name='Parameter 1', tab=self.tab1)
        self.addToBox(self.tabAtr('Ex1SliderBox'), self.slider1)
        self.qdial1 = self.createQDial(1, 99, 1, func=self.updateScatter, name='Parameter 2', tab=self.tab1)
        self.addToBox(self.tabAtr('Ex1SliderBox'), self.qdial1)

        self.ax11 = self.createAxes(111, 'plot 1', 'x', 'y', True, self.tabAtr('Ex1Figure'))

        self.x = np.linspace(-np.pi, np.pi, 100)
        self.y = np.sin(self.x)
        self.line = self.plotLine(self.x, self.y, self.ax11, zorder=0)

        self.pointRamEx1 = self.plotPoint(0, 0, self.ax11, color='#bfbfbf', markerSize=12, zorder=2)
        self.pointEx1 = self.plotPoint(0, 0, self.ax11, color='Crimson', markerSize=9, zorder=3)

        self.xS = np.linspace(-np.pi, np.pi, 10)
        self.yS = np.sin(self.xS)

        self.scatterPointsRam = self.plotScatter(self.xS, self.yS, self.ax11, '#bfbfbf', zorder=1, s=80)
        self.scatterPoints = self.plotScatter(self.xS, self.yS, self.ax11, 'ForestGreen', zorder=2, s=40)

    @PlotInterface.canvasDraw(tab='Ex1')
    def updatePoint(self, index):
        
        x = index * 2 * np.pi / 499 - np.pi
        self.pointRamEx1.set_data([x], [np.sin(x)])
        self.pointEx1.set_data([x], [np.sin(x)])

    @PlotInterface.canvasDraw(tab='Ex1')
    def updateScatter(self, index):

        self.xS = np.linspace(-np.pi, np.pi, index)
        self.yS = np.sin(self.xS)

        self.scatterPoints.set_offsets(
            np.c_[self.xS, self.yS]
        )
        self.scatterPointsRam.set_offsets(
            np.c_[self.xS, self.yS]
        )

# INTERFACE 2
class Example2(Example1):
    def __init__(self):
        super().__init__()
        self.tab2 = self.createTab('Ex2')
        self.ax21 = self.createAxes(111, 'plot 1', 'x', 'y', True, self.tabAtr('Ex2Figure'))
        self.plotHist(np.array([random.random() for i in range(10000)]), bins=25, ax=self.ax21)

# INTERFACE 3
class Example3(Example2):
    def __init__(self):
        super().__init__()

        self.tab3 = self.createTab('Ex3')
        self.ax41 = self.createAxes(221, 'plot 1', 'x', 'y', True, self.tabAtr('Ex3Figure'))
        self.ax42 = self.createAxes(222, 'plot 2', 'x', 'y', True, self.tabAtr('Ex3Figure'))
        self.ax43 = self.createAxes(223, 'plot 3', 'x', 'y', True, self.tabAtr('Ex3Figure'))
        self.ax44 = self.createAxes(224, 'plot 4', 'x', 'y', True, self.tabAtr('Ex3Figure'))


# INTERFACE 4
class Example4(Example3):
    def __init__(self):
        super().__init__()

        self.tab4 = self.createTab('Ex4')
        self.ax41 = self.createAxes(111, 'plot 1', 'x', 'y', True, self.tabAtr('Ex4Figure'))
        file = open('data.csv', 'r')

        x = []
        y = []
        parameter = []

        for line in file:
            dataString = line.split(' ')
            if len(dataString) == 3 and dataString[0][0] != '#':
                x.append(float(dataString[0]))
                y.append(float(dataString[1]))
                parameter.append(float(dataString[2]))
        
        parameter_normalized = (parameter - np.min(parameter)) / (np.max(parameter) - np.min(parameter))
        colors = cm.rainbow(parameter_normalized)

        for pointX, pointY, c in zip(x, y, colors):
            self.pointRam = self.plotPoint(pointX, pointY, self.ax41, color='#e3e3e3', markerSize=12)
            self.point = self.plotPoint(pointX, pointY, self.ax41, color=c, markerSize=9)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("darkTheme.qss", "r") as f:
        style = f.read()
        app.setStyleSheet(style)

    window = Example4()
    window.show()
    sys.exit(app.exec_())