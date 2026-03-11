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
        self.__current_param_val2 = 20.0 
        self.__pressure_range2 = (200, 800)
        self.__current_mode2 = 'Isotherm'
        
        # Группа радиокнопок для выбора параметра
        self.createRadioGroup(
            ['Isotherm', 'Potential Temperature', 'Saturation Mixing Ratio', 'Equivalent Potential Temperature'],
            tab=self.__tab2,
            func=self.__on_mode_changed,
            name='Isolines 2'
        )
        
        # Одиночный слайдер для значения параметра
        self.createSlider(
            -40, 100, init=int(self.__current_param_val2),
            func=self.__on_param_changed,
            name='Surface Temp 2', # Переименуем логически позже, пока используем существующее имя
            tab=self.__tab2,
            label=True
        )
        
        # Range Slider для диапазона давления (теперь влияет на график)
        self.createRangeSlider(
            100, 1050, init=self.__pressure_range2,
            func=self.__on_pressure_changed,
            name='Pressure Range 2',
            tab=self.__tab2,
            label=True
        )
        
        self.__update_slider_limits()
        self.__draw_skewt()

    def __on_mode_changed(self, button):
        """Обработчик смены режима (типа аналитической линии)."""
        self.__current_mode2 = button.text()
        self.__update_slider_limits()
        self.__draw_skewt()

    def __on_param_changed(self, val):
        """Обработчик изменения значения параметра."""
        self.__current_param_val2 = float(val)
        label = getattr(self, "Surface Temp 2 Slider Label", None)
        if label:
            label.setText(str(val))
        self.__draw_skewt()

    def __on_pressure_changed(self, val):
        """Обработчик изменения диапазона давления."""
        self.__pressure_range2 = val
        label = getattr(self, "Pressure Range 2 Slider Label", None)
        if label:
            label.setText(f"{val[0]} - {val[1]}")
        self.__draw_skewt()

    def __update_slider_limits(self):
        """Динамическое изменение границ слайдера в зависимости от режима."""
        slider = getattr(self, "Surface Temp 2 slider", None)
        if not slider: return
        
        if self.__current_mode2 == 'Isotherm':
            slider.setRange(-80, 50)
        elif self.__current_mode2 == 'Potential Temperature':
            slider.setRange(-20, 150)
        elif self.__current_mode2 == 'Saturation Mixing Ratio':
            slider.setRange(0, 40) # g/kg
        elif self.__current_mode2 == 'Equivalent Potential Temperature':
            slider.setRange(-20, 150)
        
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
        
        # Установка фиксированных границ
        self.__ax_skew.set_ylim(1050, 100)
        self.__ax_skew.set_xlim(-40, 50)

        # Стандартные изолинии (утолщенные)
        self.__skew.plot_dry_adiabats(alpha=0.15, color='orange', linewidth=1.5)
        self.__skew.plot_moist_adiabats(alpha=0.15, color='blue', linewidth=1.5)
        self.__skew.plot_mixing_lines(alpha=0.15, color='green', linewidth=1.5)
        
        # Аналитическая линия
        p_min, p_max = self.__pressure_range2
        p_line = np.linspace(p_max, p_min, 100) * units.hPa
        
        try:
            if self.__current_mode2 == 'Isotherm':
                t_line = np.full_like(p_line.m, self.__current_param_val2) * units.degC
                color = 'red'
            elif self.__current_mode2 == 'Potential Temperature':
                theta = (self.__current_param_val2 + 273.15) * units.kelvin
                t_line = mpcalc.dry_lapse(p_line, theta)
                color = 'orange'
            elif self.__current_mode2 == 'Saturation Mixing Ratio':
                w = self.__current_param_val2 * units('g/kg')
                t_line = mpcalc.dewpoint_from_mixing_ratio(p_line, w)
                color = 'green'
            elif self.__current_mode2 == 'Equivalent Potential Temperature':
                theta_e = (self.__current_param_val2 + 273.15) * units.kelvin
                t_line = mpcalc.moist_lapse(p_line, theta_e)
                color = 'blue'
            
            self.__skew.plot(p_line, t_line, color, linewidth=4.0)
        except Exception as e:
            print(f"Error calculating analytical line: {e}")

        self.__ax_skew.set_xlabel('Temperature (°C)')
        self.__ax_skew.set_ylabel('Pressure (hPa)')
