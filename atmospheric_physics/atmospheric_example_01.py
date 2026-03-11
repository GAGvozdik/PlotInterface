import numpy as np
from classes.interface import PlotInterface
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QListWidget, QPushButton, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt

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
        
        # 1. Группа радиокнопок (ВЕРХ)
        self.createRadioGroup(
            ['Isotherm', 'Dry adiabat', 'Saturation Mixing Ratio', 'θe'],
            tab=self.__tab2,
            func=self.__on_mode_changed,
            name='Isolines'
        )
        
        # 2. Одиночный слайдер
        self.__param_slider_box2 = self.createSlider(
            -40, 100, init=20,
            func=self.__on_param_changed,
            name='Surface Temp', 
            tab=self.__tab2,
            label=True
        )
        
        # 3. Range Slider
        self.createRangeSlider(
            100, 1050, init=(200, 800),
            func=self.__on_pressure_changed,
            name='Pressure Range',
            tab=self.__tab2,
            label=True
        )

        # 4. Блок МЕНЕДЖЕРА ЛИНИЙ (Теперь ОТОБРАЖАЕТСЯ)
        self.__manager_box = self.createBox(self.__tab2, "LINES MANAGER", size=['auto', 300])
        self.__manager_box.layout().setContentsMargins(10, 10, 10, 10)
        
        self.__list_widget = QListWidget()
        self.__list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__list_widget.setWordWrap(True)
        
        # Добавляем список внутрь менеджера
        self.addToBox(self.__manager_box, self.__list_widget)
        
        # ГЕОМЕТРИЯ: Жесткий фикс
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
        
        # ВАЖНО: Добавляем сам бокс менеджера в боковую панель!
        self.addToBox(s_box, self.__manager_box)
        
        # 5. Кнопки Save/Load (Перемещаем вниз)
        # Находим кнопки по тексту и перемещаем их в конец лейаута
        for i in range(s_box.layout().count()):
            item = s_box.layout().itemAt(i)
            if item and item.widget():
                w = item.widget()
                if isinstance(w, QPushButton) and w.text() in ["Save picture", "Load file"]:
                    s_box.layout().removeWidget(w)
                    s_box.layout().addWidget(w)

        # Прижимаем всё меню к верху
        s_box.layout().insertStretch(s_box.layout().count() - 2, 1)
        
        # Инициализируем первую линию
        self.__add_line()
        self.__draw_skewt()

    def __add_line(self):
        """Добавление новой линии с автоинкрементом."""
        self.__line_counter += 1
        mode = 'Isotherm'
        new_line = {
            'mode': mode,
            'val': 20.0,
            'p_range': (200, 800),
            'name': f"[{self.__line_counter:02d}] {mode}"
        }
        self.__lines_data.append(new_line)
        self.__list_widget.addItem(new_line['name'])
        self.__list_widget.setCurrentRow(len(self.__lines_data) - 1)

    def __delete_line(self):
        """Удаление выбранной линии."""
        row = self.__list_widget.currentRow()
        if row >= 0 and len(self.__lines_data) > 1:
            self.__lines_data.pop(row)
            self.__list_widget.takeItem(row)
            self.__list_widget.setCurrentRow(max(0, row - 1))
            self.__draw_skewt()

    def __on_line_selected(self, index):
        """Синхронизация интерфейса."""
        if index < 0 or index >= len(self.__lines_data): return
        self.__active_line_index = index
        data = self.__lines_data[index]
        
        if hasattr(self, 'modeGroupIsolines'):
            self.modeGroupIsolines.blockSignals(True)
            for btn in self.modeGroupIsolines.buttons():
                if btn.text() == data['mode']:
                    btn.setChecked(True)
                    break
            self.modeGroupIsolines.blockSignals(False)
        
        slider = getattr(self, "Surface Temp slider", None)
        if slider:
            slider.blockSignals(True)
            self.__update_slider_limits()
            slider.setValue(int(data['val']))
            slider.blockSignals(False)
            
        r_slider = getattr(self, "Pressure Range slider", None)
        if r_slider:
            r_slider.blockSignals(True)
            r_slider.setValue(data['p_range'])
            r_slider.blockSignals(False)
            
        self.__draw_skewt()

    def __on_mode_changed(self, button):
        if self.__active_line_index < 0: return
        mode = button.text()
        self.__lines_data[self.__active_line_index]['mode'] = mode
        
        old_name = self.__list_widget.item(self.__active_line_index).text()
        prefix = old_name.split(']')[0] + ']'
        new_name = f"{prefix} {mode}"
        self.__lines_data[self.__active_line_index]['name'] = new_name
        self.__list_widget.item(self.__active_line_index).setText(new_name)
        
        self.__update_slider_limits()
        self.__draw_skewt()

    def __on_param_changed(self, val):
        if self.__active_line_index < 0: return
        self.__lines_data[self.__active_line_index]['val'] = float(val)
        
        label = getattr(self, "Surface Temp Slider Label", None)
        mode = self.__lines_data[self.__active_line_index]['mode']
        if label:
            if mode == 'Saturation Mixing Ratio':
                label.setText(f"{val/10000.0:.4f} g/kg")
            elif mode == 'θe':
                label.setText(f"{val/10.0:.1f} °C")
            else:
                label.setText(str(val))
        self.__draw_skewt()

    def __on_pressure_changed(self, val):
        if self.__active_line_index < 0: return
        self.__lines_data[self.__active_line_index]['p_range'] = val
        label = getattr(self, "Pressure Range Slider Label", None)
        if label:
            label.setText(f"{val[0]} - {val[1]}")
        self.__draw_skewt()

    def __update_slider_limits(self):
        if self.__active_line_index < 0: return
        slider = getattr(self, "Surface Temp slider", None)
        box = getattr(self, "Surface Temp Slider Box", None)
        mode = self.__lines_data[self.__active_line_index]['mode']
        if not slider: return
        
        if box: box.setTitle(mode)
        
        limits = {
            'Isotherm': (-80, 50),
            'Dry adiabat': (-20, 150),
            'Saturation Mixing Ratio': (1, 500000),
            'θe': (-200, 1500)
        }
        min_val, max_val = limits.get(mode, (-40, 100))
        slider.setRange(min_val, max_val)

    @PlotInterface.canvasDraw(tab="01 Atm.")
    def __draw_skewt(self):
        figure = self.tabAtr(f'{self.__tab_name2}Figure')
        if not METPY_AVAILABLE:
            figure.clear()
            return

        active_mode = self.__lines_data[self.__active_line_index]['mode'] if self.__active_line_index >= 0 else 'None'
        current_state = (active_mode, self.darkMode)
        
        if not hasattr(self, '_bg_state') or self._bg_state != current_state:
            figure.clear()
            self._bg_state = current_state
            self.__analytical_line_objs = [] 
            
            self.__skew = SkewT(figure, rotation=45)
            self.__ax_skew = self.__skew.ax
            self.updateAxesStyle(self.__ax_skew)
            self.__ax_skew.set_ylim(1050, 100)
            self.__ax_skew.set_xlim(-40, 50)
            self.__ax_skew.tick_params(axis='both', labelsize=15)
            
            ref_p = 1000 * units.hPa
            a_iso = 0.70 if active_mode == 'Isotherm' else 0.30
            a_dry = 0.70 if active_mode == 'Dry adiabat' else 0.30
            a_mix = 0.70 if active_mode == 'Saturation Mixing Ratio' else 0.30
            a_moist = 0.70 if active_mode == 'θe' else 0.30

            t0_dry = np.arange(-100, 200, 10) * units.degC
            dry = self.__skew.plot_dry_adiabats(t0=t0_dry, alpha=a_dry, linestyle='-')
            dry.set_color('orange')
            dry.set_linewidth(2.0)
            
            p_dry_label = 250 * units.hPa
            for t0 in t0_dry[::2]:
                try:
                    t = mpcalc.dry_lapse(p_dry_label, t0, reference_pressure=ref_p).to('degC').m
                    if -44 <= t <= 46:
                        self.__ax_skew.text(t, p_dry_label.m, f'{t0.m:.0f}', color='orange', fontsize=14,
                                            ha='center', va='center', rotation=45, clip_on=True,
                                            bbox=dict(facecolor=self.graphColor, edgecolor='none', alpha=1.0, pad=0.2))
                except: continue

            t0_moist = np.arange(-100, 100, 5) * units.degC
            moist = self.__skew.plot_moist_adiabats(t0=t0_moist, alpha=a_moist, linestyle='-')
            moist.set_color('green')
            moist.set_linewidth(2.0)
            
            p_moist_label = 400 * units.hPa
            for t0 in t0_moist[::4]:
                try:
                    t = mpcalc.moist_lapse(p_moist_label, t0, reference_pressure=ref_p).to('degC').m
                    if -44 <= t <= 46:
                        self.__ax_skew.text(t, p_moist_label.m, f'{t0.m:.0f}', color='green', fontsize=14,
                                            ha='center', va='center', rotation=45, clip_on=True,
                                            bbox=dict(facecolor=self.graphColor, edgecolor='none', alpha=1.0, pad=0.2))
                except: continue

            w_mixing = np.array([0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 2, 5, 10, 20, 30, 50]) * units('g/kg')
            p_all = np.linspace(1050, 100, 65) * units.hPa
            mixing = self.__skew.plot_mixing_lines(pressure=p_all, mixing_ratio=w_mixing, alpha=a_mix, linestyle='--')
            if mixing:
                mixing.set_color('#90EE90')
                mixing.set_linewidth(2.0)
            
            p_mix_label = 600 * units.hPa
            for w in w_mixing:
                try:
                    t = mpcalc.dewpoint(mpcalc.vapor_pressure(p_mix_label, w)).to('degC').m
                    if -44 <= t <= 46:
                        self.__ax_skew.text(t, p_mix_label.m, f'{w.m:.0g}', color='#90EE90', fontsize=14,
                                            ha='center', va='center', rotation=60, clip_on=True,
                                            bbox=dict(facecolor=self.graphColor, edgecolor='none', alpha=1.0, pad=0.2))
                except: continue
            
            self.__ax_skew.grid(True, axis='x', color='red', linewidth=1.5, alpha=a_iso)
            self.__ax_skew.grid(True, axis='y', color='black', linewidth=1.5, alpha=0.3)
            self.__ax_skew.set_xlabel('Temperature (°C)', fontsize=20)
            self.__ax_skew.set_ylabel('Pressure (hPa)', fontsize=20)
        else:
            for obj in self.__analytical_line_objs:
                try: obj.remove()
                except: pass
            self.__analytical_line_objs = []

        # Отрисовка всех линий
        for i, data in enumerate(self.__lines_data):
            p_min, p_max = data['p_range']
            p_line = np.linspace(p_max, p_min, 100) * units.hPa
            mode = data['mode']
            val = data['val']
            
            try:
                if mode == 'Isotherm':
                    t_line = np.full_like(p_line.m, val) * units.degC
                    color = 'red'
                elif mode == 'Dry adiabat':
                    t_line = mpcalc.dry_lapse(p_line, (val + 273.15) * units.kelvin)
                    color = 'orange'
                elif mode == 'Saturation Mixing Ratio':
                    w = (val / 10000.0) * units('g/kg')
                    t_line = mpcalc.dewpoint(mpcalc.vapor_pressure(p_line, w))
                    color = '#90EE90'
                elif mode == 'θe':
                    t_line = mpcalc.moist_lapse(p_line, (val / 10.0 + 273.15) * units.kelvin)
                    color = 'green'
                
                lw = 5.0 if i == self.__active_line_index else 3.0
                lines = self.__skew.plot(p_line, t_line, color, linewidth=lw)
                self.__analytical_line_objs.append(lines[0])
            except: continue
