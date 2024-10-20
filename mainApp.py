from PyQt5.QtWidgets import QApplication
import numpy as np
import sys
from classes.examples import AllExamples
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import pandas as pd
# https://scikit-gstat.readthedocs.io/en/latest/install.html

class MainApp(AllExamples):
    def __init__(self):
        super().__init__()

        self.tab1 = self.createTab('Main')

        self.ax8 = self.createAxes(self.tabAtr('MainFigure'),
            args={
                'pos': 111, 
                'name': 'Variogram',
                'xAxName': '', 
                'yAxName': '',
                'grid': False
            }
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("styles/darkTheme.qss", "r") as f:
        style = f.read()
        app.setStyleSheet(style)

    window = MainApp()
    window.show()
    sys.exit(app.exec_())