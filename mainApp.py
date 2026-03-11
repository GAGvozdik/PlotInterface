
import numpy as np
import sys
import pandas as pd
from pathlib import Path
import os
import ctypes

# Фикс для корректного отображения иконки в панели задач Windows
try:
    myappid = 'geophysics.plotinterface.v4'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

from geostatistics.examples import AllExamples
from seismic_examples.all_seismic_examples import AllSeismicExamples
from thermodynamics.all_thermo_examples import AllThermoExamples
from atmospheric_physics.all_atmospheric_examples import AllAtmosphericExamples
from classes.interface import PlotInterface

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

try:
    import pywinstyles
except ImportError:
    pywinstyles = None

class MainApp(AllExamples, AllSeismicExamples, AllThermoExamples, AllAtmosphericExamples, PlotInterface):

    def __init__(self):
        # 1. Инициализация базового интерфейса (конструктор ОДИН)
        super().__init__()

        # 2. Настройка окна
        icon_path = str(Path(__file__).parent.resolve() / "styles" / "custom_icon.ico")
        self.setWindowIcon(QIcon(icon_path))
        
        if pywinstyles:
            try:
                pywinstyles.apply_style(self, "dark")
            except Exception as e:
                print(f"Failed to apply pywinstyles: {e}")

        # 3. Настройка селектора в Sidebar (радиокнопки)
        self.modeGroup.buttonClicked.connect(self.change_mode)
        
        # 4. Загрузка начального режима
        self.change_mode()

    def change_mode(self):
        """Переключение набора вкладок через методы унаследованных миксинов."""
        checked_button = self.modeGroup.checkedButton()
        if not checked_button:
            return
            
        selected_text = checked_button.text()
        print(f"Switching to: {selected_text}")
        
        self.clearTabs()
        
        if selected_text == "General":
            self.init_all_tabs()
        elif selected_text == "Seismic":
            self.init_seismic_tabs()
        elif selected_text == "Thermodynamics":
            self.init_thermo_tabs()
        elif selected_text == "Atmospheric Physics":
            self.init_atmospheric_tabs()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    qss_path = Path(__file__).parent.resolve() / "styles" / "darkTheme.qss"
    if qss_path.exists():
        with open(qss_path, "r") as f:
            app.setStyleSheet(f.read())
    
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
