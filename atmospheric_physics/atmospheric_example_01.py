import numpy as np
from classes.interface import PlotInterface
import matplotlib.pyplot as plt

try:
    import metpy.calc as mpcalc
    from metpy.units import units
    METPY_AVAILABLE = True
except ImportError:
    METPY_AVAILABLE = False

class AtmosphericExample01:
    def init_atmospheric_01(self):
        self.__tab_name = "Atmosphere 01"
        self.__tab = self.createTab(self.__tab_name)
        
        # Параметры по умолчанию
        self.__surface_temp = 15.0  # Celsius
        self.__lapse_rate = 6.5    # C/km
        
        # Слайдеры
        self.createSlider(
            -50, 50, init=int(self.__surface_temp),
            func=self.__update_surface_temp,
            name='Surface Temperature',
            tab=self.__tab,
            label=True
        )
        self.tabAtr('Surface Temperature Slider Label').setText(f"{self.__surface_temp} °C")
        
        self.createSlider(
            1, 15, init=int(self.__lapse_rate * 2),
            func=self.__update_lapse_rate,
            name='Lapse Rate (C/km)',
            tab=self.__tab,
            label=True
        )
        self.tabAtr('Lapse Rate (C/km) Slider Label').setText(f"{self.__lapse_rate} °C/km")
        
        self.__draw_axes()
        self.__draw_plot()

    @PlotInterface.canvasDraw(tab='Atmosphere 01')
    def __draw_axes(self):
        figure = self.tabAtr(f'{self.__tab_name}Figure')
        self.__ax = self.createAxes(
            figure,
            args={
                'pos': 111,
                'name': 'Atmospheric Profile',
                'xAxName': 'Temperature (°C)',
                'yAxName': 'Altitude (km)',
                'grid': True,
                'fontsize': 14,
                'fontweight': 'bold',
                'loc': 'center',
                'y': 1.05
            }
        )

    @PlotInterface.canvasDraw(tab='Atmosphere 01')
    def __draw_plot(self):
        self.__ax.clear()
        self.updateAxesStyle(self.__ax)
        
        altitude = np.linspace(0, 15, 100) # km
        temperature = self.__surface_temp - self.__lapse_rate * altitude
        
        self.__ax.plot(temperature, altitude, linewidth=3, color='orange', label='Temperature Profile')
        
        if METPY_AVAILABLE:
            # Демонстрация использования MetPy (простой расчет точки росы)
            try:
                # В реальном приложении здесь были бы более сложные расчеты
                p = np.linspace(1000, 200, 100) * units.hPa
                t = (self.__surface_temp + 273.15) * units.kelvin
                # Просто для примера, что MetPy работает
                pass
            except:
                pass

        self.__ax.set_xlabel('Temperature (°C)')
        self.__ax.set_ylabel('Altitude (km)')
        self.__ax.legend()
        self.__ax.set_title(f'Profile (Lapse Rate: {self.__lapse_rate} °C/km)')

    def __update_surface_temp(self, val):
        self.__surface_temp = float(val)
        self.tabAtr('Surface Temperature Slider Label').setText(f"{self.__surface_temp} °C")
        self.__draw_plot()

    def __update_lapse_rate(self, val):
        self.__lapse_rate = val / 2.0
        self.tabAtr('Lapse Rate (C/km) Slider Label').setText(f"{self.__lapse_rate} °C/km")
        self.__draw_plot()
