from classes.interface import PlotInterface
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from PyQt5.QtWidgets import QPushButton, QProgressBar, QLabel, QHBoxLayout, QWidget
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import os

class MeltingWorker(QObject):
    """
    Векторизованный воркер для расчета 2D теплопроводности с плавлением.
    """
    progress = pyqtSignal(int)
    finished = pyqtSignal(dict)

    def __init__(self, params):
        super().__init__()
        self.p = params
        self.nx = params['nx_02']
        self.ny = params['ny_02']
        self.m_visual = params['m_02'] 
        self.m_total = 20000           
        self.ram = params['ram_02']

    def run(self):
        p = self.p
        nx, ny = self.nx, self.ny
        m_visual = self.m_visual
        m_total = self.m_total

        t_res = np.zeros((m_visual, nx, ny), dtype=np.float64)
        c_res = np.zeros((m_visual, nx, ny), dtype=np.float64)
        ro_res = np.zeros((m_visual, nx, ny), dtype=np.float64)
        lmbd_res = np.zeros((m_visual, nx, ny), dtype=np.float64)

        inner_mask = np.zeros((nx, ny), dtype=bool)
        inner_mask[self.ram:nx-self.ram, self.ram:ny-self.ram] = True

        a_field = np.where(inner_mask, p['a1'], p['a2'])
        b_field = np.where(inner_mask, p['b1'], p['b2'])
        d_field = np.where(inner_mask, p['d1'], p['d2'])
        e_field = np.where(inner_mask, p['e1'], p['e2'])
        f_field = np.where(inner_mask, p['f1'], p['f2'])
        g_field = np.where(inner_mask, p['g1'], p['g2'])
        h_field = np.where(inner_mask, p['h1'], p['h2'])
        lcr_field = np.where(inner_mask, p['lcr1'], p['lcr2'])
        tsol_field = np.where(inner_mask, p['tsol1'], p['tsol2'])
        tliq_field = np.where(inner_mask, p['tliq1'], p['tliq2'])

        def get_props(temp, temp_prev, rok_prev):
            ro_new = rok_prev * (1 - p['alpha_02'] * (temp - temp_prev))
            lmbd_new = a_field + b_field / (temp + 77)
            t_safe = np.where(temp_prev <= 0, 1e-10, temp_prev)
            c_new = d_field + e_field / t_safe**2 + f_field / t_safe**3 + g_field / t_safe**0.5 + h_field / t_safe
            melt_deg = np.zeros_like(temp, dtype=np.float64)
            mask_melt = (temp >= tsol_field) & (temp <= tliq_field)
            diff = tliq_field - tsol_field
            melt_deg[mask_melt] = 1.0 / np.where(diff == 0, 1e-10, diff)[mask_melt]
            c_new += lcr_field * melt_deg
            return ro_new, lmbd_new, c_new

        t_curr = np.where(inner_mask, p['t1'], p['t2']).astype(np.float64)
        ro_curr = np.where(inner_mask, p['ro1'], p['ro2']).astype(np.float64)
        _, lmbd_curr, c_curr = get_props(t_curr, t_curr, ro_curr)

        t_res[0], c_res[0], ro_res[0], lmbd_res[0] = t_curr, c_curr, ro_curr, lmbd_curr

        dx2, dy2 = p['dx_02']**2, p['dy_02']**2
        dt_small = p['dt_small_02']
        dt_large = 10 * dt_small

        for k in range(1, m_total):
            dt = dt_small if k < 2000 else dt_large
            t_next = t_curr.copy()
            term_x = (lmbd_curr[2:, 1:-1] * (t_curr[2:, 1:-1] - t_curr[1:-1, 1:-1]) - 
                      lmbd_curr[1:-1, 1:-1] * (t_curr[1:-1, 1:-1] - t_curr[:-2, 1:-1])) / dx2
            term_y = (lmbd_curr[1:-1, 2:] * (t_curr[1:-1, 2:] - t_curr[1:-1, 1:-1]) - 
                      lmbd_curr[1:-1, 1:-1] * (t_curr[1:-1, 1:-1] - t_curr[1:-1, :-2])) / dy2
            t_next[1:-1, 1:-1] += (dt / (ro_curr[1:-1, 1:-1] * c_curr[1:-1, 1:-1])) * (term_x + term_y)
            ro_next, lmbd_next, c_next = get_props(t_next, t_curr, ro_curr)
            t_curr, ro_curr, lmbd_curr, c_curr = t_next, ro_next, lmbd_next, c_next

            if k % 10 == 0:
                idx = k // 10
                if idx < m_visual:
                    t_res[idx] = t_curr
                    c_res[idx] = c_curr
                    ro_res[idx] = ro_curr
                    lmbd_res[idx] = lmbd_curr

            if k % 500 == 0:
                self.progress.emit(int(100 * (k / (m_total - 1))))
        
        self.finished.emit({'t': t_res, 'c': c_res, 'ro': ro_res, 'lmbd': lmbd_res})

class ThermoExample02:
    def _init_params_02(self):
        """Инициализация физических параметров и данных."""
        self.nx_02, self.ny_02 = 100, 100
        self.ram_02 = self.nx_02 // 4
        self.m_02 = 2000 
        self.L_02 = 1000
        self.sim_age_years_02 = 800
        self.tm_02 = self.sim_age_years_02 * (60 * 60 * 24 * 30 * 12)
        self.dx_02, self.dy_02 = self.L_02 / self.nx_02, self.L_02 / self.ny_02
        self.dt_small_02 = self.tm_02 / 182000

        self.alpha_02 = 3 * 10 ** -5
        self.ro1, self.ro2 = 3000.0, 2700.0
        self.t1, self.t2 = 1300 + 273, 0 + 273
        self.tsol1, self.tliq1, self.lcr1 = 1050 + 273, 1150 + 273, 380000
        self.tsol2, self.tliq2, self.lcr2 = 950 + 273, 1050 + 273, 300000

        self.a1, self.b1 = 1.18, 474
        self.d1, self.e1, self.f1, self.g1, self.h1 = 4896.7, -1.21e9, 1.23e11, -290790, 6447400
        self.a2, self.b2 = 0.64, 807
        self.d2, self.e2, self.f2, self.g2, self.h2 = -228.24, 3.38e8, -3.47e10, 110880, -2378100

        self.init_data_02()
        self.thermo_02_axes = {}
        self.im_objects_02 = {}
        self.slice_lines_02 = {}

    def init_data_02(self):
        self.t_02 = np.zeros((self.m_02, self.nx_02, self.ny_02), dtype=np.float64)
        self.c_02 = np.zeros((self.m_02, self.nx_02, self.ny_02), dtype=np.float64)
        self.ro_02 = np.zeros((self.m_02, self.nx_02, self.ny_02), dtype=np.float64)
        self.lmbd_02 = np.zeros((self.m_02, self.nx_02, self.ny_02), dtype=np.float64)

    def init_thermo_02(self):
        """Создание интерфейса 2D Melting."""
        # Вызываем инициализацию параметров перед созданием UI
        self._init_params_02()

        tab_layout = self.createTab('2D Melting')
        slider_box = self.tabAtr('2D MeltingSliderBox')
        ctrl_group = self.createBox(tab_layout, 'Calculation Controls')
        tab_layout.removeWidget(ctrl_group)
        self.addToBox(slider_box, ctrl_group)

        self.calc_btn_02 = QPushButton("Calculate Data")
        self.calc_btn_02.clicked.connect(self.run_melting_calc)
        self.addToBox(ctrl_group, self.calc_btn_02)
        self.read_btn_02 = QPushButton("Read Data")
        self.read_btn_02.clicked.connect(self.read_thermo_data)
        self.addToBox(ctrl_group, self.read_btn_02)
        self.write_btn_02 = QPushButton("Write Data")
        self.write_btn_02.clicked.connect(self.write_thermo_data)
        self.addToBox(ctrl_group, self.write_btn_02)

        self.prog_widget_02 = QWidget()
        p_lay = QHBoxLayout(self.prog_widget_02)
        p_lay.setContentsMargins(0, 5, 0, 5)
        self.p_bar_02 = QProgressBar()
        self.p_bar_02.setTextVisible(False)
        self.p_lbl_02 = QLabel("0%")
        p_lay.addWidget(self.p_bar_02)
        p_lay.addWidget(self.p_lbl_02)
        self.prog_widget_02.setVisible(False)
        self.addToBox(ctrl_group, self.prog_widget_02)
        self.style_progress_bar_02()

        # Step QDial
        self.createQDial(0, self.m_02 - 1, 0, tab=tab_layout, 
                         func=self.update_thermo_02_plots, name='Step_02', label=True)

        # Grid Size QSlider
        self.createSlider(20, 250, tab=tab_layout, init=100,
                          func=self.update_grid_size_label_02, name='Grid Size (NX/NY)_02', label=True)
        getattr(self, 'Grid Size (NX/NY)_02 slider').sliderReleased.connect(self.change_grid_size_02)

        # Simulation Age QSlider
        self.createSlider(100, 10000, tab=tab_layout, init=800,
                          func=self.change_sim_age_02, name='Simulation Age_02', label=True)

        self.draw_thermo_02_axes()

    def draw_thermo_02_axes(self):
        fig = self.tabAtr('2D MeltingFigure')
        fig.clear()
        gs = GridSpec(3, 3, figure=fig, wspace=0.3, hspace=0.3)
        
        self.ax_t_02 = fig.add_subplot(gs[0:2, 0:2])
        self.ax_slices_02 = fig.add_subplot(gs[2, 0:2])
        self.ax_c_02 = fig.add_subplot(gs[0, 2])
        self.ax_ro_02 = fig.add_subplot(gs[1, 2])
        self.ax_lmbd_02 = fig.add_subplot(gs[2, 2])
        
        self.thermo_02_axes = {
            'T': self.ax_t_02, 'C': self.ax_c_02, 
            'Ro': self.ax_ro_02, 'Lmbd': self.ax_lmbd_02, 
            'Slices': self.ax_slices_02
        }
        
        for ax in self.thermo_02_axes.values():
            self.updateAxesStyle(ax)

        self.plot_config = {
            'T': {'cmap': 'coolwarm', 'vmin': 273, 'vmax': 1600, 'color': 'red'},
            'C': {'cmap': 'viridis', 'vmin': 2000, 'vmax': 5000, 'color': 'green'},
            'Ro': {'cmap': 'plasma', 'vmin': 2500, 'vmax': 3100, 'color': 'purple'},
            'Lmbd': {'cmap': 'inferno', 'vmin': 0.5, 'vmax': 4.0, 'color': 'orange'}
        }

        self.im_objects_02 = {}
        for key in ['T', 'C', 'Ro', 'Lmbd']:
            ax = self.thermo_02_axes[key]
            data = getattr(self, f"{key.lower()}_02")[0]
            im = ax.imshow(data, cmap=self.plot_config[key]['cmap'], origin='lower', 
                           vmin=self.plot_config[key]['vmin'], vmax=self.plot_config[key]['vmax'], 
                           aspect='equal')
            self.im_objects_02[key] = im
            self.createColorbar(fig, im, name=key, cmap=self.plot_config[key]['cmap'])

        self.slice_lines_02 = {}
        for key in ['T', 'C', 'Ro', 'Lmbd']:
            line, = self.ax_slices_02.plot([], [], color=self.plot_config[key]['color'], 
                                            label=key, linewidth=2)
            self.slice_lines_02[key] = line
            
        self.ax_slices_02.set_ylim(-0.05, 1.05)
        self.ax_slices_02.legend(loc='upper right', fontsize=10)
        fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05, wspace=0.3, hspace=0.3)

    def update_grid_size_label_02(self, value):
        label = getattr(self, "Grid Size (NX/NY)_02 Slider Label", None)
        if label: label.setText(str(value))

    def change_grid_size_02(self):
        slider = getattr(self, 'Grid Size (NX/NY)_02 slider', None)
        if not slider: return
        value = slider.value()
        self.nx_02, self.ny_02 = value, value
        self.ram_02 = self.nx_02 // 4
        self.dx_02, self.dy_02 = self.L_02 / self.nx_02, self.L_02 / self.ny_02
        self.init_data_02()
        self.draw_thermo_02_axes()
        self.tabAtr('2D MeltingCanvas').draw_idle()

    def change_sim_age_02(self, value):
        self.sim_age_years_02 = value
        self.tm_02 = value * (60 * 60 * 24 * 30 * 12)
        self.dt_small_02 = self.tm_02 / 182000
        label = getattr(self, "Simulation Age_02 Slider Label", None)
        if label: label.setText(f"{value} years")

    def style_progress_bar_02(self):
        bg_color = self.graphColor if self.darkMode else "#f0f0f0"
        border_color = self.widgetColor if self.darkMode else "#d0d0d0"
        self.p_bar_02.setStyleSheet(f"""
            QProgressBar {{ border: 1px solid {border_color}; border-radius: 3px; background-color: {bg_color}; height: 15px; }}
            QProgressBar::chunk {{ background-color: {self.ticksColor}; }}
        """)
        self.p_lbl_02.setStyleSheet(f"color: {self.ticksColor}; font-weight: bold;")

    def run_melting_calc(self):
        self.calc_btn_02.setEnabled(False)
        self.prog_widget_02.setVisible(True)
        params = {k: v for k, v in self.__dict__.items() if isinstance(v, (int, float, bool))}
        self.tm_thread = QThread()
        self.tm_worker = MeltingWorker(params)
        self.tm_worker.moveToThread(self.tm_thread)
        self.tm_thread.started.connect(self.tm_worker.run)
        self.tm_worker.progress.connect(self.update_tm_progress)
        self.tm_worker.finished.connect(self.on_tm_finished)
        self.tm_worker.finished.connect(self.tm_thread.quit)
        self.tm_thread.start()

    def update_tm_progress(self, v):
        self.p_bar_02.setValue(v)
        self.p_lbl_02.setText(f"{v}%")

    def on_tm_finished(self, res):
        self.t_02, self.c_02, self.ro_02, self.lmbd_02 = res['t'], res['c'], res['ro'], res['lmbd']
        self.calc_btn_02.setEnabled(True)
        self.prog_widget_02.setVisible(False)
        self.update_thermo_02_plots(0)

    @PlotInterface.canvasDraw(tab='2D Melting')
    def update_thermo_02_plots(self, val):
        if not hasattr(self, 't_02') or self.t_02.ndim < 3 or self.t_02.shape[0] <= val:
            return
        label = getattr(self, "Step_02 QDial Label", None)
        if label: label.setText(str(val))
        data_dict = {'T': self.t_02[val], 'C': self.c_02[val], 'Ro': self.ro_02[val], 'Lmbd': self.lmbd_02[val]}
        for key in ['T', 'C', 'Ro', 'Lmbd']:
            self.im_objects_02[key].set_data(data_dict[key])
        curr_nx = data_dict['T'].shape[0]
        x_vals = np.arange(curr_nx)
        for key in ['T', 'C', 'Ro', 'Lmbd']:
            slice_raw = data_dict[key][curr_nx // 2, :]
            d_min, d_max = slice_raw.min(), slice_raw.max()
            slice_norm = (slice_raw - d_min) / (d_max - d_min) if d_max > d_min else np.zeros_like(slice_raw)
            self.slice_lines_02[key].set_data(x_vals, slice_norm)
        self.ax_slices_02.set_xlim(0, curr_nx - 1)

    def write_thermo_data(self):
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        if not os.path.exists(data_dir): os.makedirs(data_dir)
        for name, arr in [('t', self.t_02), ('c', self.c_02), ('ro', self.ro_02), ('lmbd', self.lmbd_02)]:
            np.save(os.path.join(data_dir, f'{name}_2d_melting.npy'), arr)

    def read_thermo_data(self):
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        try:
            for name in ['t', 'c', 'ro', 'lmbd']:
                setattr(self, f'{name}_02', np.load(os.path.join(data_dir, f'{name}_2d_melting.npy')))
            self.update_thermo_02_plots(0)
        except: pass
