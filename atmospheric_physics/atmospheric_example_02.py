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
            if self.__current_mode2 == 'Saturation Mixing Ratio':
                label.setText(f"{val/10000.0:.4f} g/kg")
            else:
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
            'Saturation Mixing Ratio': (1, 500000), # 0.0001 - 50.0 g/kg
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
        
        ref_p = 1000 * units.hPa

        # 1. Сухие адиабаты (Dry Adiabats) - Оранжевые
        t0_dry = np.arange(-100, 200, 10) * units.degC
        dry = self.__skew.plot_dry_adiabats(t0=t0_dry, alpha=0.45, linestyle='-')
        dry.set_color('orange')
        dry.set_linewidth(2.0)
        
        # Подписи для сухих адиабат (Приоритет 250 hPa)
        p_levels_dry = [250, 300, 400, 500, 600, 700, 850]
        for t0 in t0_dry[::2]:
            for p_val in p_levels_dry:
                try:
                    p_label = p_val * units.hPa
                    t = mpcalc.dry_lapse(p_label, t0, reference_pressure=ref_p).to('degC').m
                    if -44 <= t <= 46:
                        t_near = mpcalc.dry_lapse(p_label - 10 * units.hPa, t0, reference_pressure=ref_p).to('degC').m
                        p1 = self.__ax_skew.transData.transform((t, p_val))
                        p2 = self.__ax_skew.transData.transform((t_near, p_val - 10))
                        angle = np.degrees(np.arctan2(p2[1]-p1[1], p2[0]-p1[0]))
                        # Нормализация угла для читаемости (всегда головой вверх)
                        if angle > 90: angle -= 180
                        elif angle < -90: angle += 180
                        
                        self.__ax_skew.text(t, p_val, f'{t0.m:.0f}', color='orange', fontsize=7,
                                            ha='center', va='center', rotation=angle, clip_on=True,
                                            bbox=dict(facecolor=self.graphColor, edgecolor='none', alpha=1.0, pad=0.2))
                        break
                except: continue

        # 2. Влажные адиабаты (Moist Adiabats) - Зеленые
        t0_moist = np.arange(-100, 100, 5) * units.degC
        moist = self.__skew.plot_moist_adiabats(t0=t0_moist, alpha=0.45, linestyle='-')
        moist.set_color('green')
        moist.set_linewidth(2.0)
        
        # Подписи для влажных адиабат (Приоритет 400 hPa)
        p_levels_moist = [400, 500, 600, 700, 850, 300]
        for t0 in t0_moist[::4]:
            for p_val in p_levels_moist:
                try:
                    p_label = p_val * units.hPa
                    t = mpcalc.moist_lapse(p_label, t0, reference_pressure=ref_p).to('degC').m
                    if -44 <= t <= 46:
                        t_near = mpcalc.moist_lapse(p_label - 10 * units.hPa, t0, reference_pressure=ref_p).to('degC').m
                        p1 = self.__ax_skew.transData.transform((t, p_val))
                        p2 = self.__ax_skew.transData.transform((t_near, p_val - 10))
                        angle = np.degrees(np.arctan2(p2[1]-p1[1], p2[0]-p1[0]))
                        # Нормализация угла
                        if angle > 90: angle -= 180
                        elif angle < -90: angle += 180
                        
                        self.__ax_skew.text(t, p_val, f'{t0.m:.0f}', color='green', fontsize=7,
                                            ha='center', va='center', rotation=angle, clip_on=True,
                                            bbox=dict(facecolor=self.graphColor, edgecolor='none', alpha=1.0, pad=0.2))
                        break
                except: continue

        # 3. Линии смешивания (Mixing Ratio) - Салатовые
        w_mixing = np.array([0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 2, 5, 10, 20, 30, 50]) * units('g/kg')
        p_all = np.linspace(1050, 100, 65) * units.hPa
        mixing = self.__skew.plot_mixing_lines(pressure=p_all, mixing_ratio=w_mixing, alpha=0.45, linestyle='--')
        if mixing:
            mixing.set_color('#90EE90')
            mixing.set_linewidth(2.0)
            
        # Подписи для линий смешивания (Приоритет 600 hPa)
        p_levels_mix = [600, 700, 850, 500, 400]
        for w in w_mixing:
            for p_val in p_levels_mix:
                try:
                    p_label = p_val * units.hPa
                    v_p = mpcalc.vapor_pressure(p_label, w)
                    t = mpcalc.dewpoint(v_p).to('degC').m
                    if -44 <= t <= 46:
                        v_p_near = mpcalc.vapor_pressure(p_label - 10 * units.hPa, w)
                        t_near = mpcalc.dewpoint(v_p_near).to('degC').m
                        p1 = self.__ax_skew.transData.transform((t, p_val))
                        p2 = self.__ax_skew.transData.transform((t_near, p_val - 10))
                        angle = np.degrees(np.arctan2(p2[1]-p1[1], p2[0]-p1[0]))
                        # Нормализация угла
                        if angle > 90: angle -= 180
                        elif angle < -90: angle += 180
                        
                        label_text = f'{w.m:.0g}' if w.m >= 0.01 else f'{w.m:.4f}'
                        self.__ax_skew.text(t, p_val, label_text, color='#90EE90', fontsize=7,
                                            ha='center', va='center', rotation=angle, clip_on=True,
                                            bbox=dict(facecolor=self.graphColor, edgecolor='none', alpha=1.0, pad=0.2))
                        break
                except: continue
        
        # 4. Сетка (Изотермы и Изобары)
        self.__ax_skew.grid(True, axis='x', color='red', linewidth=1.5, alpha=0.3)
        self.__ax_skew.grid(True, axis='y', color='black', linewidth=1.5, alpha=0.3)
        
        # 5. Аналитическая линия
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
                w = (self.__current_param_val2 / 10000.0) * units('g/kg')
                vapor_pressure = mpcalc.vapor_pressure(p_line, w)
                t_line = mpcalc.dewpoint(vapor_pressure)
                color = '#90EE90'
            elif self.__current_mode2 == 'Equivalent Potential Temperature':
                theta_e = (self.__current_param_val2 + 273.15) * units.kelvin
                t_line = mpcalc.moist_lapse(p_line, theta_e)
                color = 'green'
            
            self.__skew.plot(p_line, t_line, color, linewidth=4.0)
        except Exception as e:
            print(f"Error calculating analytical line: {e}")

        self.__ax_skew.set_xlabel('Temperature (°C)')
        self.__ax_skew.set_ylabel('Pressure (hPa)')
