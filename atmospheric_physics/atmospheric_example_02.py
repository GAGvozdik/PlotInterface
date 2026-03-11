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
        self.__param_slider_box2 = self.createSlider(
            -40, 100, init=int(self.__current_param_val2),
            func=self.__on_param_changed,
            name='Surface Temp 2', 
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
        """Динамическое изменение границ и заголовка слайдера в зависимости от режима."""
        slider = getattr(self, "Surface Temp 2 slider", None)
        box = getattr(self, "Surface Temp 2 Slider Box", None)
        if not slider: return
        
        # Смена заголовка бокса
        if box:
            box.setTitle(self.__current_mode2)
        
        # Установка новых границ
        limits = {
            'Isotherm': (-80, 50),
            'Potential Temperature': (-20, 150),
            'Saturation Mixing Ratio': (1, 50), # g/kg, мин 1 для избежания ошибок
            'Equivalent Potential Temperature': (-20, 150)
        }
        
        min_val, max_val = limits.get(self.__current_mode2, (-40, 100))
        slider.setRange(min_val, max_val)
        
        # Принудительная корректировка текущего значения под новые границы
        current_val = slider.value()
        new_val = max(min_val, min(max_val, current_val))
        slider.setValue(new_val)
        self.__current_param_val2 = float(new_val)
        
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

        # Фоновые изолинии (согласно запросу, принудительная стилизация)
        dry = self.__skew.plot_dry_adiabats(alpha=0.3)
        dry.set_color('orange')
        dry.set_linewidth(1.5)
        
        moist = self.__skew.plot_moist_adiabats(alpha=0.3)
        moist.set_color('green')
        moist.set_linewidth(1.5)
        
        mixing = self.__skew.plot_mixing_lines(alpha=0.3)
        mixing.set_color('#90EE90') # Salatoviy
        mixing.set_linewidth(1.5)
        
        isotherms = self.__skew.plot_isotherms(alpha=0.3)
        isotherms.set_color('red')
        isotherms.set_linewidth(1.5)
        
        # Изобары (горизонтальные линии)
        self.__ax_skew.grid(True, axis='y', color='black', linewidth=1.5, alpha=0.3)
        
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
                vapor_pressure = mpcalc.vapor_pressure(p_line, w)
                t_line = mpcalc.dewpoint(vapor_pressure)
                color = '#90EE90' # Lightgreen
            elif self.__current_mode2 == 'Equivalent Potential Temperature':
                theta_e = (self.__current_param_val2 + 273.15) * units.kelvin
                t_line = mpcalc.moist_lapse(p_line, theta_e)
                color = 'green'
            
            self.__skew.plot(p_line, t_line, color, linewidth=4.0)
        except Exception as e:
            print(f"Error calculating analytical line: {e}")

        self.__ax_skew.set_xlabel('Temperature (°C)')
        self.__ax_skew.set_ylabel('Pressure (hPa)')
