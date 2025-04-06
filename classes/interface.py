import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QPushButton, QVBoxLayout, QBoxLayout, QFileDialog, QMessageBox
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSlider, QGridLayout, QGroupBox, QDial
from PyQt5.QtCore import Qt
from .graphObjects import GraphObjects
import time
import numpy as np
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QMenu


class PlotInterface(GraphObjects):
    def __init__(self):
        super().__init__()  
        
        # menuBar = self.menuBar()
        # # Creating menus using a QMenu object
        # fileMenu = QMenu("&File", self)
        # menuBar.addMenu(fileMenu)
        # # Creating menus using a title
        # editMenu = menuBar.addMenu("&Edit")
        # helpMenu = menuBar.addMenu("&Help")

        # self.menu = QTabWidget()
        # menuItem = QWidget()
        # layout = QGridLayout()
        # menuItem.setLayout(layout)
        # self.menu.addTab(menuItem, 'List')
        
        # self.layout.addWidget(self.menu, 0, 0, 0, 1)  



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

        self.darkMode = True
        # self.changeMode()

        self.fileName = None

    def createTab(self, name):
        tab = QWidget()
        layout = QGridLayout()
        tab.setLayout(layout)
        self.tabs.addTab(tab, name)

        layout.setObjectName(name)

        sliderBox = self.createBox(layout, "Sliders box", [1, 2], [300, 1100])
        setattr(self, f"{name}SliderBox", sliderBox)

        graphBox = self.createBox(layout, "Graph box", [0, 0, 0, 2], [1500, 1100])
        setattr(self, f"{name}GraphBox", graphBox)

        figure, canvas = self.createFigure(name, graphBox)

        setattr(self, f"{name}Figure", figure)
        setattr(self, f"{name}Canvas", canvas)

        saveButton = QPushButton("Save picture")
        saveButton.clicked.connect(self.saveFile)
        self.addToBox(sliderBox, saveButton)

        loadButton = QPushButton("Load file")
        loadButton.clicked.connect(self.get_file_way)
        self.addToBox(sliderBox, loadButton)

        # darkMode = QPushButton("Dark mode")
        # darkMode.clicked.connect(self.changeMode)
        # self.addToBox(sliderBox, darkMode)


        return layout
    
    def changeMode(self):
        self.darkMode = not self.darkMode
        
        if self.darkMode == True:
            self.windowColor = '#2E2E2E'   
            self.widgetColor = '#6e6e6e'
            self.graphColor = '#4c4c4c'
            self.ticksColor = '#b5b5b5'
        else:
            self.windowColor = 'white'   
            self.widgetColor = 'grey'
            self.graphColor = 'white'
            self.ticksColor = 'black'


    def saveFile(self):
        try:
            current_index = self.tabs.currentIndex()
            current_tab_name = self.tabs.tabText(current_index)
            figure_name = f"{current_tab_name}Figure"
            figure = getattr(self, figure_name, None)
            way = self.save_file()
            if way != None:
                figure.savefig(way, transparent=True, dpi=400)
        except:
            pass



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

        self.addToBox(self.tabAtr(f'{tab.objectName()}SliderBox'), sliderBox)

        return sliderBox

    def createQDial(self, min, max, init, tab, func='none', name='', label=False):
        dialBox = self.createBox(tab, name, size=[240, 250])
        dial = QDial(self)
        dial.move(0, 0)
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

        setattr(self, f"{name} QDial", dial)
        self.addToBox(self.tabAtr(f'{tab.objectName()}SliderBox'), dialBox)

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

    def canvasDraw(tab):
        def decorator(func):
            def wrapper(self, *args, **kwargs):
                result = func(self, *args, **kwargs)
                self.tabAtr(f'{tab}Canvas').draw()  
                return result
            return wrapper
        return decorator
    

    def getWorkTime(name):
        def decorator(func):
            def wrapper(self, *args, **kwargs):
                start_time = time.time() 

                result = func(self, *args, **kwargs)

                end_time = time.time()
                method_time = end_time - start_time


                print(f"Max {name} method work time: {method_time:.4f} s")

 
                return result
            return wrapper
        return decorator


    def load_file(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(
            self, 
            "Choose the file", 
            "", 
            "Text Files (*.txt);;All Files (*)", 
            options=options
        )

        if fileName:
            try:
                x, y, v = np.loadtxt(fileName, unpack=True)
                QMessageBox.information(self, "Sucess", "File uploaded")
                print(x[:5], y[:5], v[:5])
                return x, y, v
            
            except:
                QMessageBox.critical(self, "Error", f"Can`t upload file")
                return [], [], []
        else:
            QMessageBox.critical(self, "Error", f"Can`t find file")
            return [], [], []

    def get_file_way(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(
            self, 
            "Choose the file", 
            "", 
            "All Files (*)", 
            options=options
        )

        if fileName:
            self.fileName = fileName
        else:
            QMessageBox.critical(self, "Error", f"Can`t find file")


    def save_file(self):
        try:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getSaveFileName(
                self,
                "Choose the file",
                QDir.currentPath(),
                "PNG Images (*.png);;All Files (*)",
                options=options
            )

            if fileName:
                QMessageBox.information(self, "Sucess", "file was choosen")
                return fileName
            else:
                QMessageBox.critical(self, "Error", "file wasn`t choosen")
                return None
        except:
            return None

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = PlotInterface()
    window.show()

    sys.exit(app.exec_())


