import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QGridLayout, QGroupBox, QDial
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure 
from matplotlib.colors import ListedColormap
from .graphObjects import GraphObjects

class PlotInterface(GraphObjects):
    def __init__(self):
        super().__init__()  
        
        self.setWindowTitle("Sine Function Slider")
        self.setGeometry(500, 130, 1800, 1100) # (x, y, width, height)
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs, 0, 0)       

        self.windowColor = '#2E2E2E'   
        self.gridColor = '#6e6e6e'
        self.widgetColor = '#6e6e6e'
        self.graphColor = '#4c4c4c'
        self.ticksColor = '#b5b5b5'

    def createTab(self, name):
        tab = QWidget()
        layout = QGridLayout()
        tab.setLayout(layout)
        self.tabs.addTab(tab, name)

        sliderBox = self.createBox(layout, "Sliders box", [0, 6, 1, 1], ['auto', 300])
        setattr(self, f"{name}SliderBox", sliderBox)

        graphBox = self.createBox(layout, "Graph box", [0, 0, 1, 6])
        setattr(self, f"{name}GraphBox", graphBox)

        figure, canvas = self.createFigure(name, graphBox)

        return layout

    def tabAtr(self, name):
        return getattr(self, f"{name}")

    def createSlider(self, min, max, init, tab, func='none', name=''):
        sliderBox = self.createBox(tab, name, size=[240, 100])
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(min)
        slider.setMaximum(max)
        slider.setValue(init)
        if func != 'none':
            slider.valueChanged.connect(func)
        self.addToBox(sliderBox, slider)

        return sliderBox

    def createQDial(self, min, max, init, tab, func='none', name=''):
        dialBox = self.createBox(tab, name, size=[240, 200])
        dial = QDial(self)
        dial.move(30, 50)
        dial.setRange(min, max)
        if func != 'none':
            dial.valueChanged.connect(func)
        self.addToBox(dialBox, dial)
        return dialBox
    
    def createBox(self, tab, title='', position=[], size=['none', 'none'], v=True):
        box = QGroupBox(title)

        if size[0] == 'auto':
            box.setFixedWidth(size[1]) 
        elif size[1] == 'auto':
            box.setFixedHeight(size[0])   
        elif isinstance(size[0], int) and isinstance(size[1], int):
            box.setFixedSize(size[0], size[1]) 

        tab.addWidget(box, *position)

        if v:
            box.setLayout(QVBoxLayout())
        else:
            box.setLayout(QHBoxLayout())

        return box

    def addToBox(self, box, widget):
        box.layout().addWidget(widget)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = PlotInterface()
    window.show()

    sys.exit(app.exec_())


