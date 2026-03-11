import numpy as np
from classes.interface import PlotInterface
import matplotlib.pyplot as plt

try:
    from metpy.plots import SkewT
    from metpy.units import units
    import metpy.calc as mpcalc
    METPY_AVAILABLE = True
except ImportError:
    METPY_AVAILABLE = False

class AtmosphericExample02:
    def init_atmospheric_02(self):
        self.__tab_name2 = "Atmosphere 02"
        self.__tab2 = self.createTab(self.__tab_name2)
        
        # Параметры по умолчанию
        self.__surface_temp2 = 20.0  # Celsius
        self.__pressure_range2 = (100, 1000)
        
        # Слайдер температуры (Заглушка)
        self.createSlider(
            -40, 50, init=int(self.__surface_temp2),
            func=self.__stub_func,
            name='Surface Temp 2',
            tab=self.__tab2,
            label=True
        )
        
        # Range Slider для давления (Заглушка)
        self.createRangeSlider(
            100, 1050, init=self.__pressure_range2,
            func=self.__stub_func,
            name='Pressure Range 2',
            tab=self.__tab2,
            label=True
        )
        
        # Группа радиокнопок для изолиний (Заглушка)
        self.createRadioGroup(
            ['All', 'None', 'Temp Only'],
            tab=self.__tab2,
            func=self.__stub_func,
            name='Isolines 2'
        )
        
        self.__draw_skewt()

    @PlotInterface.canvasDraw(tab="Atmosphere 02")
    def __draw_skewt(self):
        figure = self.tabAtr(f'{self.__tab_name2}Figure')
        figure.clear()

        if not METPY_AVAILABLE:
            ax = figure.add_subplot(1, 1, 1)
            ax.text(0.5, 0.5, "MetPy not installed", ha='center')
            return

        # Инициализация Skew-T
        self.__skew = SkewT(figure, rotation=45)
        self.__ax_skew = self.__skew.ax
        self.updateAxesStyle(self.__ax_skew)
        
        # Установка границ ДО отрисовки изолиний важна для MetPy
        self.__ax_skew.set_ylim(1050, 100)
        self.__ax_skew.set_xlim(-40, 50)

        # Стандартные изолинии
        self.__skew.plot_dry_adiabats(alpha=0.25, color='orange')
        self.__skew.plot_moist_adiabats(alpha=0.25, color='blue')
        self.__skew.plot_mixing_lines(alpha=0.25, color='green')
        
        # Тестовый профиль
        p = np.linspace(1000, 100, 50) * units.hPa
        t = (20 - 0.0065 * (1000 - p.m)) * units.degC
        self.__skew.plot(p, t, 'r', linewidth=2)

        self.__ax_skew.set_xlabel('Temperature (°C)')
        self.__ax_skew.set_ylabel('Pressure (hPa)')

    def __stub_func(self, *args):
        """Заглушка для виджетов."""
        print(f"Widget changed, but logic is not connected yet. Args: {args}")
