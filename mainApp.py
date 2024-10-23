from PyQt5.QtWidgets import QApplication
import numpy as np
import sys
from classes.examples import AllExamples
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import pandas as pd
import geone as gn
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure 
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget
from PyQt5.QtWidgets import QGridLayout

class MainApp(AllExamples):
    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open("styles/darkTheme.qss", "r") as f:
        style = f.read()
        app.setStyleSheet(style)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
