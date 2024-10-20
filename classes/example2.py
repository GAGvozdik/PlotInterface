from .interface import PlotInterface
from PyQt5.QtWidgets import QApplication
import numpy as np
import sys
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd



# INTERFACE 2
class Example2(PlotInterface):
    def __init__(self):
        super().__init__()
        self.tab2 = self.createTab('Ex2')

        self.qdial2 = self.createQDial(10, 99, 40, func=self.updateBins, name='bins', tab=self.tab2)
        self.addToBox(self.tabAtr('Ex2SliderBox'), self.qdial2)

        self.ax21 = self.createAxes(self.tabAtr('Ex2Figure'),
            args={
                'pos': 111, 
                'name': 'plot 1',
                'xAxName': '', 
                'yAxName': '',
                'grid': True
            }
        )
        self.ax21.set_ylim(0, 800)

        self.histData = np.array(np.random.normal(0, 1, 10000))
        self.hist1 = self.ax21.hist(self.histData, bins=100, color='Crimson', zorder=2)

    @PlotInterface.canvasDraw(tab='Ex2')
    def updateBins(self, index):

        self.ax21.remove()
        self.ax21 = self.createAxes(self.tabAtr('Ex2Figure'),
            args={
                'pos': 111, 
                'name': 'plot 1',
                'xAxName': '', 
                'yAxName': '',
                'grid': True
            }
        )
        self.ax21.set_ylim(0, 800)
        self.hist1 = self.ax21.hist(self.histData, bins=index, color='Crimson', zorder=2)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("styles/darkTheme.qss", "r") as f:
        style = f.read()
        app.setStyleSheet(style)

    window = Example2()
    window.show()
    sys.exit(app.exec_())
