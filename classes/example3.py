from .interface import PlotInterface
from PyQt5.QtWidgets import QApplication
import numpy as np
import sys
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd



# INTERFACE 3
class Example3(PlotInterface):
    def __init__(self):
        super().__init__()

        self.tab3 = self.createTab('Ex3')

        self.ax31 = self.createAxes(self.tabAtr('Ex3Figure'),
            args={
                'pos': 221, 
                'name': 'plot 1',
                'xAxName': 'x', 
                'yAxName': 'y',
                'grid': True
            }
        )
        
        self.ax32 = self.createAxes(self.tabAtr('Ex3Figure'),
            args={
                'pos': 222, 
                'name': 'plot 2',
                'xAxName': 'x', 
                'yAxName': 'y',
                'grid': True
            }
        )
        self.ax33 = self.createAxes(self.tabAtr('Ex3Figure'),
            args={
                'pos': 223, 
                'name': 'plot 3',
                'xAxName': 'x', 
                'yAxName': 'y',
                'grid': True
            }
        )
        self.ax34 = self.createAxes(self.tabAtr('Ex3Figure'),
            args={
                'pos': 224, 
                'name': 'plot 4',
                'xAxName': 'x', 
                'yAxName': 'y',
                'grid': True
            }
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("styles/darkTheme.qss", "r") as f:
        style = f.read()
        app.setStyleSheet(style)

    window = Example3()
    window.show()
    sys.exit(app.exec_())
