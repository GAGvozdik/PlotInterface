import sys
import time
import numpy as np
from PyQt5.QtCore import Qt, QDir
from .graphObjects import GraphObjects
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTabWidget, QPushButton, QVBoxLayout,
    QBoxLayout, QFileDialog, QMessageBox, QHBoxLayout, QLabel, QSlider,
    QGridLayout, QGroupBox, QDial, QSizePolicy, QSpacerItem, QMenu,
    QRadioButton, QButtonGroup
)

class PlotInterface(GraphObjects):
    def __init__(self):
        super().__init__()  

        self.setWindowTitle("Module plot interface")
        self.setGeometry(250, 50, 2100, 1300)

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Вернём аккуратные внешние отступы
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(5)

        self.tabs = QTabWidget()
        self.tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.tabs, 0, 0)

        self.windowColor = '#2E2E2E'   
        self.widgetColor = '#6e6e6e'
        self.graphColor = '#4c4c4c'
        self.ticksColor = '#b5b5b5'
        self.gridColor = '#6e6e6e'
        self.ticksWidth = 2.5

        self.darkMode = True
        self.fileName = None

        self.dark_mode = True  # Текущая тема

        self.app = QApplication.instance()
        


    def initThemeSwitcher(self):
        """Создание радиокнопок для переключения темы."""
        themeBox = QGroupBox("Theme")
        themeBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        themeLayout = QVBoxLayout()
        themeBox.setLayout(themeLayout)

        darkRadio = QRadioButton("Dark")
        lightRadio = QRadioButton("Light")
        darkRadio.setChecked(True)

        themeGroup = QButtonGroup()
        themeGroup.addButton(darkRadio)
        themeGroup.addButton(lightRadio)

        darkRadio.toggled.connect(self.switchTheme)
        lightRadio.toggled.connect(self.switchTheme)

        themeLayout.addWidget(darkRadio)
        themeLayout.addWidget(lightRadio)
            
        return themeBox
            
    def switchTheme(self):
        sender = self.sender()
        if isinstance(sender, QRadioButton):
            theme_name = sender.text().lower()
            qss_path = Path(__file__).parent.parent / "styles" / f"{theme_name}Theme.qss"

            # Обновляем цвета для matplotlib
            if theme_name == "dark":
                self.windowColor = '#2E2E2E'   
                self.widgetColor = '#6e6e6e'
                self.graphColor = '#4c4c4c'
                self.ticksColor = '#b5b5b5'
                self.gridColor = '#6e6e6e'
                self.ticksWidth = 2.5
            else:
                self.windowColor = '#d6d6d6'   
                self.gridColor = 'grey'
                self.widgetColor = 'black'
                self.graphColor = '#d6d6d6'
                self.ticksColor = 'black'
                self.ticksWidth = 1

            # Применяем QSS стиль
            try:
                with open(qss_path, "r") as f:
                    QApplication.instance().setStyleSheet(f.read())
            except Exception as e:
                print(f"Ошибка при загрузке стиля: {e}")

            # Обновляем фигуры и canvas
            for i in range(self.tabs.count()):
                tab_name = self.tabs.tabText(i)
                fig = getattr(self, f"{tab_name}Figure", None)
                canvas = getattr(self, f"{tab_name}Canvas", None)

                if fig is not None and canvas is not None:
                    fig.patch.set_facecolor(self.windowColor)
                    for ax in fig.axes:
                        self.updateAxesStyle(ax)
                    canvas.draw()
                    
    def updateAxesStyle(self, ax):
        ax.set_facecolor(self.graphColor)
        ax.title.set_color(self.ticksColor)
        ax.xaxis.label.set_color(self.ticksColor)
        ax.yaxis.label.set_color(self.ticksColor)

        for spine in ax.spines.values():
            spine.set_color(self.widgetColor)
            spine.set_linewidth(self.ticksWidth)

        ax.tick_params(axis='both', labelcolor=self.ticksColor,
                    color=self.widgetColor, width=self.ticksWidth, length=6, labelsize=12)

        # Обновим сетку, если она уже была включена
        gridlines = ax.get_xgridlines() + ax.get_ygridlines()
        if any(line.get_visible() for line in gridlines):
            ax.grid(True, color=self.gridColor)



    def createTab(self, name):
        tab = QWidget()
        layout = QGridLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        tab.setLayout(layout)
        self.tabs.addTab(tab, name)
        layout.setObjectName(name)

        graphBox = self.createBox(layout, "Graph box", [0, 0, 0, 2])
        graphBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        setattr(self, f"{name}GraphBox", graphBox)

        sliderBox = self.createBox(layout, "Sliders box", [0, 2])
        sliderBox.setFixedWidth(300)
        sliderBox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        setattr(self, f"{name}SliderBox", sliderBox)

        figure, canvas = self.createFigure(name, graphBox)
        setattr(self, f"{name}Figure", figure)
        setattr(self, f"{name}Canvas", canvas)

        saveButton = QPushButton("Save picture")
        saveButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        saveButton.setFixedHeight(60)
        saveButton.clicked.connect(self.saveFile)
        self.addToBox(sliderBox, saveButton)

        loadButton = QPushButton("Load file")
        loadButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        loadButton.setFixedHeight(60)
        loadButton.clicked.connect(self.get_file_way)
        self.addToBox(sliderBox, loadButton)

        themeBox = self.initThemeSwitcher()
        self.addToBox(sliderBox, themeBox)

        spacer = QSpacerItem(20, 60, QSizePolicy.Minimum, QSizePolicy.Expanding)
        sliderBox.layout().addItem(spacer)

        return layout

    def tabAtr(self, name):
        return getattr(self, f"{name}")

    def createSlider(self, min, max, tab, init=0, func='none', name='', label=False):
        sliderBox = self.createBox(tab, name, size=['auto', 100], v=True)
        sliderBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(min)
        slider.setMaximum(max)
        slider.setValue(init)
        slider.setSingleStep(1)
        slider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        slider.setFixedHeight(40)

        if func != 'none':
            slider.valueChanged.connect(func)
        self.addToBox(sliderBox, slider)

        if label:
            label_widget = QLabel(str(init))
            setattr(self, f"{name} Slider Label", label_widget)
            self.addToBox(sliderBox, label_widget)

        setattr(self, f"{name} slider", slider)

        self.addToBox(self.tabAtr(f'{tab.objectName()}SliderBox'), sliderBox)

        return sliderBox

    def createQDial(self, min, max, init, tab, func='none', name='', label=False):
        dialBox = self.createBox(tab, name, size=['auto', 210])
        dialBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        dial = QDial(self)
        dial.move(0, 0)
        dial.setFixedSize(225, 150)
        dial.setRange(min, max)
        dial.setSingleStep(1)

        if func != 'none':
            dial.valueChanged.connect(func)

        self.addToBox(dialBox, dial)
        if label:
            label_widget = QLabel(str(init))
            setattr(self, f"{name} QDial Label", label_widget)
            self.addToBox(dialBox, label_widget)

        setattr(self, f"{name} QDial", dial)

        self.addToBox(self.tabAtr(f'{tab.objectName()}SliderBox'), dialBox)

        return dialBox

    def createBox(self, tab, title='', position=[], size=['none', 'none'], v=True):
        box = QGroupBox(title)

        if isinstance(size[0], int) and isinstance(size[1], int):
            box.setFixedSize(size[0], size[1])
        elif size[0] == 'auto' and isinstance(size[1], int):
            box.setFixedHeight(size[1])
        elif isinstance(size[0], int) and size[1] == 'auto':
            box.setFixedWidth(size[0])

        # По умолчанию – растягиваемый блок
        if size == ['none', 'none']:
            box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        tab.addWidget(box, *position)

        if v == True:
            layout = QVBoxLayout()
            layout.setContentsMargins(5, 5, 5, 5)
            layout.setSpacing(18)
            box.setLayout(layout)
        elif v == 'center':
            layout = QBoxLayout(QBoxLayout.LeftToRight)
            layout.setAlignment(Qt.AlignCenter)
            layout.setSpacing(18)
            box.setLayout(layout)
        else:
            layout = QHBoxLayout()
            layout.setContentsMargins(5, 5, 5, 5)
            layout.setSpacing(18)
            box.setLayout(layout)

        return box

    def addToBox(self, box, widget):
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        box.layout().addWidget(widget)

    ##############################################
    ##############################################
    ##############################################
    ##############################################
    ##############################################
    
    
    def canvasDraw(tab):
        def decorator(func):
            def wrapper(self, *args, **kwargs):
                result = func(self, *args, **kwargs)
                self.tabAtr(f'{tab}Canvas').draw()  
                return result
            return wrapper
        return decorator
    

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


