from PyQt5.QtWidgets import QApplication
import numpy as np
import sys
from examples import PlotInterface
from examples import Example5
import matplotlib.pyplot as plt
import skgstat as skg
from matplotlib.colors import ListedColormap
import pandas as pd
# https://scikit-gstat.readthedocs.io/en/latest/install.html

class Example1(PlotInterface):
    def __init__(self):
        super().__init__()



if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("styles/darkTheme.qss", "r") as f:
        style = f.read()
        app.setStyleSheet(style)

    window = Example3()
    window.show()
    sys.exit(app.exec_())