import numpy as np
from classes.interface import PlotInterface
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QListWidget, QPushButton, QHBoxLayout, QSizePolicy
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
        self.__tab2 = self.createTab(self.__tab_name2)
        s_box = self.tabAtr(f"{self.__tab_name2}SliderBox")
        
        # Данные менеджера линий
        self.__lines_data = [] 
        self.__active_line_index = -1
        self.__line_counter = 0
        self.__analytical_line_objs = [] 
        self.__background_line_width = 0.7
        
        # 1. Группа радиокнопок
        self.createRadioGroup(
            ['None', 'Dry adiabat', 'Saturation Mixing Ratio', 'θe', 'Isotherm'],
            tab=self.__tab2,
            func=self.__on_mode_changed,
            name='Isolines'
        )
        
        # 2. Одиночный слайдер
        self.createSlider(
            -200, 1500, init=200, 
            func=self.__on_param_changed,
            name='Surface Temp', 
            tab=self.__tab2,
            label=True
        )

        # 2. Толщина линий
        lw_slider_box = self.createSlider(
            1, 15, init=int(self.__background_line_width * 10), 
            func=self.__on_background_line_width_changed,
            name='Background LineWidth', 
            tab=self.__tab2,
            label=True
        )
        self.addToBox(s_box, lw_slider_box)
        label = getattr(self, "Background LineWidth Slider Label", None)
        if label: label.setText(f"{self.__background_line_width}")
        # -----------------------
        
        # 3. Range Slider
        self.createRangeSlider(
            100, 1050, init=(200, 800),
            func=self.__on_pressure_changed,
            name='Pressure Range',
            tab=self.__tab2,
            label=True
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
            s_box.layout().removeWidget(save_btn); s_box.layout().removeWidget(load_btn)
            s_box.layout().addStretch(1); s_box.layout().addWidget(save_btn); s_box.layout().addWidget(load_btn)
        
        self.__add_line()
        self.__draw_skewt()

    def __add_line(self):
        self.__line_counter += 1
        new_line = {'mode': 'None', 'val': 20.0, 'p_range': (200, 800), 'name': f"[{self.__line_counter:02d}] None"}
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
        
        group = getattr(self, "Isolines Group", None)
        if group:
            group.blockSignals(True)
            for btn in group.buttons():
                if btn.text() == data['mode']: btn.setChecked(True); break
            group.blockSignals(False)
        
        slider = getattr(self, "Surface Temp slider", None)
        if slider:
            slider.blockSignals(True); self.__update_slider_limits()
            if data['mode'] == 'Saturation Mixing Ratio':
                log_val = (np.log10(max(1e-6, data['val'])) - (-4)) / (np.log10(50) - (-4)) * 10000.0
                slider.setValue(int(log_val))
            elif data['mode'] in ['Dry adiabat', 'θe']: slider.setValue(int(data['val'] * 10))
            else: slider.setValue(int(data['val']))
            slider.blockSignals(False)
            
        r_slider = getattr(self, "Pressure Range slider", None)
        if r_slider:
            r_slider.blockSignals(True); r_slider.setValue(data['p_range']); r_slider.blockSignals(False)
        self.__draw_skewt()

    def __on_mode_changed(self, button):
        if self.__active_line_index < 0: return
        mode = button.text(); self.__lines_data[self.__active_line_index]['mode'] = mode
        old_name = self.__list_widget.item(self.__active_line_index).text()
        prefix = old_name.split(']')[0] + ']'; new_name = f"{prefix} {mode}"
        self.__list_widget.item(self.__active_line_index).setText(new_name)
        self.__update_slider_limits()
        slider = getattr(self, "Surface Temp slider", None)
        if slider: self.__on_param_changed(slider.value())
        self.__draw_skewt()

    def __on_param_changed(self, val):
        if self.__active_line_index < 0: return
        mode = self.__lines_data[self.__active_line_index]['mode']
        if mode == 'Saturation Mixing Ratio': actual_val = 10**(-4 + (val/10000.0) * (np.log10(50) - (-4)))
        elif mode in ['Dry adiabat', 'θe']: actual_val = val / 10.0
        else: actual_val = float(val)
        self.__lines_data[self.__active_line_index]['val'] = actual_val
        label = getattr(self, "Surface Temp Slider Label", None)
        if label:
            if mode == 'Saturation Mixing Ratio': label.setText(f"{actual_val:.4f} g/kg")
            elif mode in ['Dry adiabat', 'θe']: label.setText(f"{actual_val:.1f} °C")
            else: label.setText(str(actual_val))
        self.__draw_skewt()

    def __on_pressure_changed(self, val):
        if self.__active_line_index < 0: return
        self.__lines_data[self.__active_line_index]['p_range'] = val
        label = getattr(self, "Pressure Range Slider Label", None)
        if label: label.setText(f"{val[0]} - {val[1]}")
        self.__draw_skewt()

    def __on_background_line_width_changed(self, val):
        self.__background_line_width = val / 10
        label = getattr(self, "Background LineWidth Slider Label", None)
        if label: label.setText(f"{self.__background_line_width}")
        self.__draw_skewt()

    def __update_slider_limits(self):
        if self.__active_line_index < 0: return
        slider = getattr(self, "Surface Temp slider", None)
        r_slider = getattr(self, "Pressure Range slider", None)
        box = getattr(self, "Surface Temp Slider Box", None)
        mode = self.__lines_data[self.__active_line_index]['mode']
        
        if slider:
            if box: box.setTitle(mode)
            is_none = (mode == 'None')
            slider.setEnabled(not is_none)
            if r_slider: r_slider.setEnabled(not is_none)
            
            if mode == 'Saturation Mixing Ratio': slider.setRange(0, 10000)
            elif mode in ['Dry adiabat', 'θe']: slider.setRange(-200, 1500)
            else: slider.setRange(-80, 50)

    @PlotInterface.canvasDraw(tab="01 Atm.")
    def __draw_skewt(self):
        figure = self.tabAtr(f'{self.__tab_name2}Figure')
        if not METPY_AVAILABLE or self.__active_line_index < 0:
            if figure: figure.clear()
            return

        active_mode = self.__lines_data[self.__active_line_index]['mode']
        current_state = (active_mode, self.darkMode, self.__background_line_width)
        
        if not hasattr(self, '_bg_state') or self._bg_state != current_state:
            figure.clear(); self._bg_state = current_state; self.__analytical_line_objs = [] 
            self.__skew = SkewT(figure, rotation=45); self.__ax_skew = self.__skew.ax
            self.updateAxesStyle(self.__ax_skew)
            self.__ax_skew.set_ylim(1050, 100); self.__ax_skew.set_xlim(-40, 50); self.__ax_skew.tick_params(axis='both', labelsize=15)
            
            # Принудительное обновление для стабильности трансформаций
            self.__ax_skew.apply_aspect()
            canvas = self.tabAtr(f'{self.__tab_name2}Canvas')
            canvas_ready = canvas and canvas.width() > 0 and canvas.height() > 0
            
            ref_p = 1000 * units.hPa
            if active_mode == 'None':
                a_iso = a_dry = a_mix = a_moist = 0.30
            else:
                a_iso, a_dry, a_mix, a_moist = (0.70 if active_mode == m else 0.30 for m in ['Isotherm', 'Dry adiabat', 'Saturation Mixing Ratio', 'θe'])
                if active_mode == 'θe': a_moist = 0.7
                
            pe = [path_effects.withStroke(linewidth=self.__background_line_width*4, foreground=self.graphColor)]
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
                    self.__ax_skew.text(t, 200, f'{t0.m:.0f}', color=c_dry, fontsize=14, fontweight='bold', ha='center', va='center', rotation=angle, clip_on=True, path_effects=pe, alpha=a_dry)

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
                    self.__ax_skew.text(t, 300, f'{t0.m:.0f}', color=c_moist, fontsize=14, fontweight='bold', ha='center', va='center', rotation=angle, clip_on=True, path_effects=pe, alpha=a_moist + 0.2)

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
                    self.__ax_skew.text(t, 500, txt, color=c_mix, fontsize=14, fontweight='bold', ha='center', va='center', rotation=angle, clip_on=True, path_effects=pe, alpha=a_mix)
            
            self.__ax_skew.grid(True, axis='x', color='#AD1C1C', linewidth=self.__background_line_width*1.5, alpha=a_iso)
            self.__ax_skew.grid(True, axis='y', color="#202020", linewidth=self.__background_line_width*1.5, alpha=0.3)
            self.__ax_skew.set_xlabel('Temperature (°C)', fontsize=20); self.__ax_skew.set_ylabel('Pressure (hPa)', fontsize=20)
        else:
            for obj in self.__analytical_line_objs:
                try: obj.remove()
                except: pass
            self.__analytical_line_objs = []

        # Отрисовка ВСЕХ сохраненных линий из менеджера
        ref_p = 1000 * units.hPa
        for i, data in enumerate(self.__lines_data):
            mode = data['mode']
            if mode == 'None': continue # Пропускаем, если текущая линия в режиме None
            
            p_min, p_max = data['p_range']
            p_line = np.linspace(p_max, p_min, 100) * units.hPa
            val = data['val']
            
            try:
                if mode == 'Isotherm': t_line = np.full_like(p_line.m, val) * units.degC; color = "#AD1C1C"
                elif mode == 'Dry adiabat': t_line = mpcalc.dry_lapse(p_line, (val + 273.15) * units.kelvin, reference_pressure=ref_p); color = "orange"
                elif mode == 'Saturation Mixing Ratio': t_line = mpcalc.dewpoint(mpcalc.vapor_pressure(p_line, val * units('g/kg'))); color = "#18CE18"
                elif mode == 'θe': t_line = mpcalc.moist_lapse(p_line, (val + 273.15) * units.kelvin, reference_pressure=ref_p); color = "#009F0B"
                else: continue
                lines = self.__skew.plot(p_line, t_line, color, linewidth=4.0); self.__analytical_line_objs.append(lines[0])
            except: continue
