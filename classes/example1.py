from .interface import PlotInterface
from PyQt5.QtWidgets import QApplication
import numpy as np
import sys

# INTERFACE 1
class Example1(PlotInterface):
    def __init__(self):
        super().__init__()

        self.tab1 = self.createTab('Ex1')
        self.slider1 = self.createSlider(0, 500, 1, func=self.updatePoint, name='Parameter 1', tab=self.tab1)
        self.addToBox(self.tabAtr('Ex1SliderBox'), self.slider1)
        self.qdial1 = self.createQDial(1, 99, 1, func=self.updateScatter, name='Parameter 2', tab=self.tab1)
        self.addToBox(self.tabAtr('Ex1SliderBox'), self.qdial1)

        self.ax11 = self.createAxes(self.tabAtr('Ex1Figure'),
            args={
                'pos': 111, 
                'name': 'plot 1',
                'xAxName': 'x', 
                'yAxName': 'y',
                'grid': True
            }
        )

        x = np.linspace(-np.pi, np.pi, 100)
        y = np.sin(x)
        self.line = self.ax11.plot(x, y, color='grey', linewidth=4, zorder=1)

        self.pointRam = self.ax11.scatter(0, 0, color='#bfbfbf', s=120, zorder=4)
        self.point = self.ax11.scatter(0, 0, color='Crimson', s=60, zorder=5)

        self.xS = np.linspace(-np.pi, np.pi, 10)
        self.yS = np.sin(self.xS)

        self.linePointsRam = self.ax11.scatter(self.xS, self.yS, color='#bfbfbf', s=80, zorder=2)
        self.linePoints = self.ax11.scatter(self.xS, self.yS, color='ForestGreen', s=40, zorder=3)

    @PlotInterface.canvasDraw(tab='Ex1')
    def updatePoint(self, index):
        x = index * 2 * np.pi / 499 - np.pi
        self.pointRam.set_offsets([x, np.sin(x)])
        self.point.set_offsets([x, np.sin(x)])

    @PlotInterface.canvasDraw(tab='Ex1')
    def updateScatter(self, index):
        self.xS = np.linspace(-np.pi, np.pi, index)
        self.yS = np.sin(self.xS)
        self.linePoints.set_offsets(np.c_[self.xS, self.yS])
        self.linePointsRam.set_offsets(np.c_[self.xS, self.yS])

if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("styles/darkTheme.qss", "r") as f:
        style = f.read()
        app.setStyleSheet(style)

    window = Example1()
    window.show()
    sys.exit(app.exec_())
