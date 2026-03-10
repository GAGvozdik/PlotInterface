
import numpy as np
import sys
import pandas as pd
import geone as gn
from pathlib import Path
import os
import ctypes

# Фикс для корректного отображения иконки в панели задач Windows
try:
    myappid = 'mycompany.myproduct.subproduct.version' # произвольная строка
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

from geostatistics.examples import AllExamples
from seismic_examples.all_seismic_examples import AllSeismicExamples
from thermodynamics.all_thermo_examples import AllThermoExamples
from classes.interface import PlotInterface

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog
from PyQt5.QtGui import QIcon

try:
    import pywinstyles
except ImportError:
    pywinstyles = None

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class MainApp(PlotInterface):

    def __init__(self):
        super().__init__()

        # Настройка иконки и стиля окна
        icon_path = str(Path(__file__).parent.resolve() / "styles" / "custom_icon.ico")
        self.setWindowIcon(QIcon(icon_path))
        
        if pywinstyles:
            try:
                pywinstyles.apply_style(self, "dark")
            except Exception as e:
                print(f"Failed to apply pywinstyles: {e}")

        # Режимы работы (наборы примеров)
        self.modes = {
            "Геостатистика": AllExamples,
            "Сейсмика": AllSeismicExamples,
            "Термодинамика": AllThermoExamples
        }
        
        # Настройка селектора
        self.modeSelector.addItems(list(self.modes.keys()))
        self.modeSelector.currentIndexChanged.connect(self.change_example_mode)
        
        # Инициализация первого режима по умолчанию
        self.change_example_mode()

    def change_example_mode(self):
        """Динамическое переключение набора вкладок."""
        self.clearTabs()
        selected_mode = self.modeSelector.currentText()
        mode_class = self.modes.get(selected_mode)
        
        if mode_class:
            # Вызываем инициализацию миксина. 
            # Благодаря флагу _setup_done в PlotInterface, ядро UI не будет пересоздано.
            mode_class.__init__(self)
            print(f"Switched to mode: {selected_mode}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    with open(Path(__file__).parent.resolve()  / "styles" / "darkTheme.qss", "r") as f:
        style = f.read()
        app.setStyleSheet(style)
        
    # with open(resource_path("styles/darkTheme.qss"), "r") as f:
    #     app.setStyleSheet(f.read())
    
    window = MainApp()
    
    if pywinstyles:
        try:
            pywinstyles.apply_style(window, "dark")
        except Exception as e:
            print(f"Failed to apply pywinstyles: {e}")

    window.show()
    sys.exit(app.exec_())

