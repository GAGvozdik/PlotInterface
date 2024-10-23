import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QPushButton, QVBoxLayout, QBoxLayout
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSlider, QGridLayout, QGroupBox, QDial
from PyQt5.QtCore import Qt
from .graphObjects import GraphObjects

class PlotInterface(GraphObjects):
    def __init__(self):
        super().__init__()  
        
        self.setWindowTitle("Module plot interface")
        self.setGeometry(500, 130, 1800, 1100) # (x, y, width, height)
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs, 0, 0)       

        self.windowColor = '#2E2E2E'   
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

        setattr(self, f"{name}Figure", figure)
        setattr(self, f"{name}Canvas", canvas)

        return layout

    def tabAtr(self, name):
        return getattr(self, f"{name}")

    def createSlider(self, min, max, tab, init=0, func='none', name='', label=False):
        sliderBox = self.createBox(tab, name, size=[240, 100], v=False)
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(min)
        slider.setMaximum(max)
        slider.setValue(init)
        slider.setSingleStep(1)
        if func != 'none':
            slider.valueChanged.connect(func)
        self.addToBox(sliderBox, slider)

        if label:
            label = QLabel(str(init))
            setattr(self, f"{name} Slider Label", label)
            self.addToBox(sliderBox, self.tabAtr(f"{name} Slider Label"))

        setattr(self, f"{name} slider", slider)
        return sliderBox

    def createQDial(self, min, max, init, tab, func='none', name='', label=False):
        dialBox = self.createBox(tab, name, size=[240, 250])
        dial = QDial(self)
        dial.move(30, 50)
        dial.setFixedSize(190, 150)
        dial.setRange(min, max)
        dial.setSingleStep(1)

        if func != 'none':
            dial.valueChanged.connect(func)

        self.addToBox(dialBox, dial)
        if label:
            label = QLabel(str(init))
            setattr(self, f"{name} QDial Label", label)
            self.addToBox(dialBox, self.tabAtr(f"{name} QDial Label"))

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

        if v == True:
            box.setLayout(QVBoxLayout())
        elif v == 'center':
            box.setLayout(QBoxLayout(QBoxLayout.LeftToRight))
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


