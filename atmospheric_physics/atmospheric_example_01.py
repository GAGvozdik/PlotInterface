import numpy as np
from classes.interface import PlotInterface
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QListWidget, QPushButton, QHBoxLayout, QSizePolicy, QGridLayout, QVBoxLayout
from PyQt5.QtCore import Qt
import matplotlib.patheffects as path_effects

try:
    from metpy.plots import SkewT
    from metpy.units import units
    import metpy.calc as mpcalc
    METPY_AVAILABLE = True
except ImportError:
    METPY_AVAILABLE = False

class AtmosphericExample01:
    def init_atmospheric_01(self):
        self.__tab_name2 = "01 Atm."
        self.__tab2 = self.createTab(self.__tab_name2, columns=2)
        s_box = self.tabAtr(f"{self.__tab_name2}SliderBox")
        
        # Данные менеджера линий
        self.__lines_data = [] 
        self.__active_line_index = -1
        self.__line_counter = 0
        self.__analytical_line_objs = [] 
        self.__background_line_width = 0.7
        self.__p_min_val = 100
        
        # 1. Основные слайдеры (ПЕРЕНЕСЕНЫ В НАЧАЛО И СДЕЛАНЫ ПОЛНОШИРИННЫМИ)
        temp_box = self.createSlider(
            -200, 1500, init=200, 
            func=self.__on_param_changed,
            name='Surface Temp', 
            tab=self.__tab2,
            label=True
        )

        lw_box = self.createSlider(
            1, 15, init=int(self.__background_line_width * 10), 
            func=self.__on_background_line_width_changed,
            name='Background LineWidth', 
            tab=self.__tab2,
            label=True
        )

        vs_box = self.createSlider(
            1, 6, init=1, 
            func=self.__on_p_min_changed,
            name='Vertical Scale (P min)', 
            tab=self.__tab2,
            label=True
        )

        # 3. Range Slider (СДЕЛАН ПОЛНОШИРИННЫМИ)
        pr_box = self.createRangeSlider(
            100, 1050, init=(100, 1050),
            func=self.__on_pressure_changed,
            name='Pressure Range',
            tab=self.__tab2,
            label=True
        )
        
        # Вставляем их в основной вертикальный лейаут над колонками (они будут растянуты на всю ширину s_box)
        s_box.layout().insertWidget(0, temp_box)
        s_box.layout().insertWidget(1, lw_box)
        s_box.layout().insertWidget(2, vs_box)
        s_box.layout().insertWidget(3, pr_box)

        label = self.tabAtr("Background LineWidth Slider Label")
        if label: label.setText(f"{self.__background_line_width}")
        # -----------------------

        # 2. Группа радиокнопок
        self.createRadioGroup(
            ['None', 'Dry adiabat', 'Saturation Mixing Ratio', 'θe', 'Isotherm', 'Isobar'],
            tab=self.__tab2,
            func=self.__on_mode_changed,
            name='Isolines'
        )
        
        # 4. Блок МЕНЕДЖЕРА ЛИНИЙ
        self.__manager_box = self.createBox(self.__tab2, "LINES MANAGER", size=['auto', 300])
        self.__manager_box.layout().setContentsMargins(10, 10, 10, 10)
        
        self.__list_widget = QListWidget()
        self.__list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__list_widget.setWordWrap(True)
        self.addToBox(self.__manager_box, self.__list_widget)
        
        self.__list_widget.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Expanding)
        self.__list_widget.setMinimumWidth(0)
        self.__list_widget.setMaximumWidth(275)
        
        self.__list_widget.currentRowChanged.connect(self.__on_line_selected)
        
        btn_layout = QHBoxLayout()
        self.__btn_add = QPushButton("Add")
        self.__btn_add.clicked.connect(self.__add_line)
        self.__btn_del = QPushButton("Del")
        self.__btn_del.clicked.connect(self.__delete_line)
        btn_layout.addWidget(self.__btn_add)
        btn_layout.addWidget(self.__btn_del)
        self.__manager_box.layout().addLayout(btn_layout)
        
        self.addToBox(s_box, self.__manager_box)
        
        save_btn, load_btn = None, None
        for i in range(s_box.layout().count()):
            item = s_box.layout().itemAt(i)
            if item and item.widget():
                w = item.widget()
                if isinstance(w, QPushButton) and w.text() == "Save picture": save_btn = w
                if isinstance(w, QPushButton) and w.text() == "Load file": load_btn = w
        
        if save_btn and load_btn:
            layout = s_box.layout()
            if isinstance(layout, QVBoxLayout):
                layout.removeWidget(save_btn); layout.removeWidget(load_btn)
                layout.addStretch(1); layout.addWidget(save_btn); layout.addWidget(load_btn)
        
        self.__add_line()
        self.__draw_skewt()

    def __add_line(self):
        self.__line_counter += 1
        new_line = {'mode': 'None', 'val': 20.0, 'p_range': (100, 1050), 'name': f"[{self.__line_counter:02d}] None"}
        self.__lines_data.append(new_line)
        self.__list_widget.addItem(new_line['name'])
        self.__list_widget.setCurrentRow(len(self.__lines_data) - 1)

    def __delete_line(self):
        row = self.__list_widget.currentRow()
        if row >= 0 and len(self.__lines_data) > 1:
            self.__lines_data.pop(row); self.__list_widget.takeItem(row)
            self.__list_widget.setCurrentRow(max(0, row - 1)); self.__draw_skewt()

    def __on_line_selected(self, index):
        if index < 0 or index >= len(self.__lines_data): return
        self.__active_line_index = index
        data = self.__lines_data[index]
        
        group = self.tabAtr("Isolines Group")
        if group:
            group.blockSignals(True)
            for btn in group.buttons():
                if btn.text() == data['mode']: btn.setChecked(True); break
            group.blockSignals(False)
        
        slider = self.tabAtr("Surface Temp slider")
        if slider:
            slider.blockSignals(True); self.__update_slider_limits()
            if data['mode'] == 'Saturation Mixing Ratio':
                log_val = (np.log10(max(1e-6, data['val'])) - (-4)) / (np.log10(50) - (-4)) * 10000.0
                slider.setValue(int(log_val))
            elif data['mode'] in ['Dry adiabat', 'θe']: slider.setValue(int(data['val'] * 10))
            else: slider.setValue(int(data['val']))
            slider.blockSignals(False)
            
        r_slider = self.tabAtr("Pressure Range slider")
        if r_slider:
            r_slider.blockSignals(True); r_slider.setValue(data['p_range']); r_slider.blockSignals(False)
        self.__draw_skewt()

    def __on_mode_changed(self, button):
        if self.__active_line_index < 0: return
        mode = button.text()
        self.__lines_data[self.__active_line_index]['mode'] = mode
        
        # Обновляем имя в списке с проверкой существования элемента
        item = self.__list_widget.item(self.__active_line_index)
        if item:
            prefix = item.text().split(']')[0] + ']'
            item.setText(f"{prefix} {mode}")
        
        # Обновляем лимиты слайдеров (с блокировкой сигналов внутри)
        self.__update_slider_limits()
        
        # Принудительно вызываем обновление параметров для нового режима
        slider = self.tabAtr("Surface Temp slider")
        if slider:
            self.__on_param_changed(slider.value())
        else:
            self.__draw_skewt()

    def __on_param_changed(self, val):
        if self.__active_line_index < 0: return
        mode = self.__lines_data[self.__active_line_index]['mode']
        if mode == 'Saturation Mixing Ratio': actual_val = 10**(-4 + (val/10000.0) * (np.log10(50) - (-4)))
        elif mode == 'Isobar': actual_val = float(val)
        elif mode in ['Dry adiabat', 'θe']: actual_val = val / 10.0
        else: actual_val = float(val)
        self.__lines_data[self.__active_line_index]['val'] = actual_val
        
        label = self.tabAtr("Surface Temp Slider Label")
        if label:
            if mode == 'Saturation Mixing Ratio': label.setText(f"{actual_val:.4f} g/kg")
            elif mode == 'Isobar': label.setText(f"{actual_val:.0f} hPa")
            elif mode in ['Dry adiabat', 'θe']: label.setText(f"{actual_val:.1f} °C")
            else: label.setText(str(actual_val))
        self.__draw_skewt()

    def __on_pressure_changed(self, val):
        if self.__active_line_index < 0: return
        self.__lines_data[self.__active_line_index]['p_range'] = val
        label = self.tabAtr("Pressure Range Slider Label")
        if label:
            mode = self.__lines_data[self.__active_line_index]['mode']
            unit = "°C" if mode == "Isobar" else "hPa"
            label.setText(f"{val[0]} - {val[1]} {unit}")
        self.__draw_skewt()

    def __on_background_line_width_changed(self, val):
        self.__background_line_width = val / 10
        label = self.tabAtr("Background LineWidth Slider Label")
        if label: label.setText(f"{self.__background_line_width}")
        self.__draw_skewt()

    def __on_p_min_changed(self, val):
        self.__p_min_val = float(100 * val)
        label = self.tabAtr("Vertical Scale (P min) Slider Label")
        if label: label.setText(f"{100 * val} hPa")
        self.__draw_skewt()

    def refresh_atmospheric_01(self):
        self.__draw_skewt()

    def __update_slider_limits(self):
        if self.__active_line_index < 0: return
        slider = self.tabAtr("Surface Temp slider")
        r_slider = self.tabAtr("Pressure Range slider")
        r_slider_box = self.tabAtr("Pressure Range Slider Box")
        box = self.tabAtr("Surface Temp Slider Box")
        mode = self.__lines_data[self.__active_line_index]['mode']
        
        if slider:
            slider.blockSignals(True)
            if box: box.setTitle(mode)
            if r_slider_box:
                r_slider_box.setTitle("Temperature Range" if mode == "Isobar" else "Pressure Range")
                
            is_none = (mode == 'None')
            slider.setEnabled(not is_none)
            
            # Динамическая стилизация
            slider.setProperty("active", "false" if is_none else "true")
            slider.style().unpolish(slider)
            slider.style().polish(slider)
            
            if r_slider: r_slider.setEnabled(not is_none)
            
            if mode == 'Saturation Mixing Ratio': slider.setRange(0, 10000)
            elif mode == 'Isobar': slider.setRange(100, 1050)
            elif mode == 'Dry adiabat': slider.setRange(-200, 1500)
            elif mode == 'θe': slider.setRange(-200, 650)
            else: slider.setRange(-80, 50)
            slider.blockSignals(False)

        if r_slider:
            r_slider.blockSignals(True)
            if mode == "Isobar":
                r_slider.setRange(-80, 80)
                if self.__lines_data[self.__active_line_index]['p_range'][1] > 80:
                    self.__lines_data[self.__active_line_index]['p_range'] = (-40, 40)
                    r_slider.setValue((-40, 40))
            else:
                r_slider.setRange(100, 1050)
                if self.__lines_data[self.__active_line_index]['p_range'][0] < 100:
                    self.__lines_data[self.__active_line_index]['p_range'] = (100, 1050)
                    r_slider.setValue((100, 1050))
            r_slider.blockSignals(False)

    @PlotInterface.canvasDraw(tab="01 Atm.")
    def __draw_skewt(self):
        figure = self.tabAtr(f'{self.__tab_name2}Figure')
        if not METPY_AVAILABLE or self.__active_line_index < 0:
            if figure: figure.clear()
            return

        active_mode = self.__lines_data[self.__active_line_index]['mode']
        current_state = (active_mode, self.darkMode, self.__background_line_width, self.graphColor, self.__p_min_val)
        
        if not hasattr(self, '_bg_state') or self._bg_state != current_state or getattr(self, '_force_refresh', False):
            figure.clear()
            self._bg_state = current_state
            
            # Форсируем растяжение графика на всё пространство
            figure.subplots_adjust(left=0.08, right=0.98, top=0.95, bottom=0.08)
            
            self.__skew = SkewT(figure, rotation=45)
            self.__ax_skew = self.__skew.ax
            self.__ax_skew.set_aspect('auto')
            self.updateAxesStyle(self.__ax_skew)
            self.__ax_skew.set_ylim(1050, self.__p_min_val)
            self.__ax_skew.set_xlim(-40, 80)
            self.__ax_skew.tick_params(axis='both', labelsize=15)
            
            self.__draw_background(active_mode)
            self.__analytical_line_objs = []
        else:
            for obj in self.__analytical_line_objs:
                try: obj.remove()
                except: pass
            self.__analytical_line_objs = []

        self.__draw_analytical_lines()

    def __draw_background(self, active_mode):
        canvas = self.tabAtr(f'{self.__tab_name2}Canvas')
        canvas_ready = canvas and canvas.width() > 0 and canvas.height() > 0
        
        ref_p = 1000 * units.hPa
        if active_mode == 'None':
            a_iso = a_dry = a_moist = a_isobar = 0.30
            a_mix = 0.45
        else:
            a_iso, a_dry, a_mix, a_moist, a_isobar = (0.70 if active_mode == m else 0.30 for m in ['Isotherm', 'Dry adiabat', 'Saturation Mixing Ratio', 'θe', 'Isobar'])
            if active_mode == 'θe': a_moist = 0.7
            if active_mode != 'Saturation Mixing Ratio': a_mix = 0.45

        bg_color = self.graphColor
        x_min, x_max = self.__ax_skew.get_xlim()
        c_dry, c_moist, c_mix = "orange", "#009F0B", "#18CE18"

        # 1. Dry
        t0_dry = np.arange(-100, 200, 10) * units.degC
        dry_lines = self.__skew.plot_dry_adiabats(t0=t0_dry, alpha=a_dry, linestyle='-', linewidth=self.__background_line_width*2.0)
        dry_lines.set_color(c_dry)
        
        for t0 in t0_dry:
            t = np.atleast_1d(mpcalc.dry_lapse(200 * units.hPa, t0, reference_pressure=ref_p).to('degC').m)[0]
            if x_min + 2 <= t <= x_max - 2:
                t_near = np.atleast_1d(mpcalc.dry_lapse(199 * units.hPa, t0, reference_pressure=ref_p).to('degC').m)[0]
                if canvas_ready:
                    p1 = self.__ax_skew.transData.transform((t, 200))
                    p2 = self.__ax_skew.transData.transform((t_near, 199))
                    angle = np.degrees(np.arctan2(p2[1]-p1[1], p2[0]-p1[0]))
                else:
                    angle = 30
                
                if angle > 90: angle -= 180
                elif angle < -90: angle += 180
                self.__ax_skew.text(t, 200, f'{t0.m:.0f}', color=c_dry, fontsize=14, fontweight='bold', ha='center', va='center', rotation=angle, clip_on=True, bbox=dict(facecolor=bg_color, edgecolor='none', pad=0.5), zorder=10, alpha=a_dry)

        # 2. Moist
        t0_moist = np.arange(-100, 100, 5) * units.degC
        moist_lines = self.__skew.plot_moist_adiabats(t0=t0_moist, alpha=a_moist, linestyle='-', linewidth=self.__background_line_width*2.0)
        moist_lines.set_color(c_moist)
        
        for t0 in t0_moist:
            t = np.atleast_1d(mpcalc.moist_lapse(300 * units.hPa, t0, reference_pressure=ref_p).to('degC').m)[0]
            if x_min + 2 <= t <= x_max - 2:
                t_near = np.atleast_1d(mpcalc.moist_lapse(299 * units.hPa, t0, reference_pressure=ref_p).to('degC').m)[0]
                if canvas_ready:
                    p1 = self.__ax_skew.transData.transform((t, 300))
                    p2 = self.__ax_skew.transData.transform((t_near, 299))
                    angle = np.degrees(np.arctan2(p2[1]-p1[1], p2[0]-p1[0]))
                else:
                    angle = 60
                    
                if angle > 90: angle -= 180
                elif angle < -90: angle += 180
                self.__ax_skew.text(t, 300, f'{t0.m:.0f}', color=c_moist, fontsize=14, fontweight='bold', ha='center', va='center', rotation=angle, clip_on=True, bbox=dict(facecolor=bg_color, edgecolor='none', pad=0.5), zorder=10, alpha=a_moist + 0.2)

        # 3. Mix
        w_mixing = np.array([0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 2, 5, 10, 20, 30, 50]) * units('g/kg')
        mix_lines = self.__skew.plot_mixing_lines(pressure=np.linspace(1050, 100, 65) * units.hPa, mixing_ratio=w_mixing, alpha=a_mix, linestyle='--', linewidth=self.__background_line_width*2.0)
        if mix_lines: mix_lines.set_color(c_mix)
        
        for w in w_mixing:
            t = np.atleast_1d(mpcalc.dewpoint(mpcalc.vapor_pressure(500 * units.hPa, w)).to('degC').m)[0]
            if x_min + 2 <= t <= x_max - 2:
                t_near = np.atleast_1d(mpcalc.dewpoint(mpcalc.vapor_pressure(499 * units.hPa, w)).to('degC').m)[0]
                if canvas_ready:
                    p1 = self.__ax_skew.transData.transform((t, 500))
                    p2 = self.__ax_skew.transData.transform((t_near, 499))
                    angle = np.degrees(np.arctan2(p2[1]-p1[1], p2[0]-p1[0]))
                else:
                    angle = -60
                    
                if angle > 90: angle -= 180
                elif angle < -90: angle += 180
                txt = f'{w.m:.0g}' if w.m >= 0.01 else f'{w.m:.4f}'
                self.__ax_skew.text(t, 500, txt, color=c_mix, fontsize=14, fontweight='bold', ha='center', va='center', rotation=angle, clip_on=True, bbox=dict(facecolor=bg_color, edgecolor='none', pad=0.5), zorder=10, alpha=a_mix)
        
        self.__ax_skew.grid(True, axis='x', color='#AD1C1C', linewidth=self.__background_line_width*1.5, alpha=a_iso)
        self.__ax_skew.grid(True, axis='y', color="#202020", linewidth=self.__background_line_width*1.5, alpha=a_isobar if active_mode == 'Isobar' else 0.3)
        self.__ax_skew.set_xlabel('Temperature (°C)', fontsize=20); self.__ax_skew.set_ylabel('Pressure (hPa)', fontsize=20)

    def __draw_analytical_lines(self):
        ref_p = 1000 * units.hPa
        for i, data in enumerate(self.__lines_data):
            mode = data['mode']
            if mode == 'None': continue 
            
            p_min, p_max = data['p_range']
            p_line = np.linspace(p_max, p_min, 100) * units.hPa
            val = data['val']
            
            try:
                if mode == 'Isotherm': t_line = np.full_like(p_line.m, val) * units.degC; color = "#F33232"
                elif mode == 'Dry adiabat': t_line = mpcalc.dry_lapse(p_line, (val + 273.15) * units.kelvin, reference_pressure=ref_p); color = "orange"
                elif mode == 'Saturation Mixing Ratio': t_line = mpcalc.dewpoint(mpcalc.vapor_pressure(p_line, val * units('g/kg'))); color = "#0B950B"
                elif mode == 'θe': t_line = mpcalc.moist_lapse(p_line, (val + 273.15) * units.kelvin, reference_pressure=ref_p); color = "#008109"
                elif mode == 'Isobar': 
                    t_line = np.linspace(p_min, p_max, 100) * units.degC
                    p_line = np.full_like(t_line.m, val) * units.hPa
                    color = "#404040"
                else: continue
                
                lines = self.__skew.plot(p_line, t_line, color, linewidth=4.0)
                self.__analytical_line_objs.append(lines[0])
                
                if mode in ['Dry adiabat', 'Saturation Mixing Ratio', 'θe']:
                    p_top = max(data['p_range'][0], self.__p_min_val)
                    p_bottom = min(data['p_range'][1], 1050)
                    
                    for p_val in [p_top, p_bottom]:
                        p_unit = p_val * units.hPa
                        if mode == 'Dry adiabat':
                            t_point = mpcalc.dry_lapse(p_unit, (val + 273.15) * units.kelvin, reference_pressure=ref_p).to('degC').m
                        elif mode == 'Saturation Mixing Ratio':
                            t_point = mpcalc.dewpoint(mpcalc.vapor_pressure(p_unit, val * units('g/kg'))).to('degC').m
                        elif mode == 'θe':
                            t_point = mpcalc.moist_lapse(p_unit, (val + 273.15) * units.kelvin, reference_pressure=ref_p).to('degC').m
                        
                        sc = self.__ax_skew.scatter(t_point, p_val, facecolor='white', edgecolor='#333333', linewidth=2.2, s=85, zorder=35)
                        self.__analytical_line_objs.append(sc)
            except: continue
