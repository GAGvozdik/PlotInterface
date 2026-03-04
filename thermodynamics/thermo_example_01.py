from classes.interface import PlotInterface
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QPushButton, QProgressBar, QLabel, QHBoxLayout, QWidget
from PyQt5.QtCore import QObject, QThread, pyqtSignal

class CalculationWorker(QObject):
    """
    Воркер для выноса тяжелых тепловых расчетов в отдельный поток.
    """
    progress = pyqtSignal(int)
    finished = pyqtSignal(np.ndarray)

    def __init__(self, nx, ny, m, dt, dx, dy, lmbdzero, rozero, cp):
        super().__init__()
        self.nx = nx
        self.ny = ny
        self.m = m
        self.dt = dt
        self.dx = dx
        self.dy = dy
        self.lmbdzero = lmbdzero
        self.rozero = rozero
        self.cp = cp

    def run(self):
        # Инициализация локальных массивов для расчета
        t = np.zeros((self.m, self.nx, self.ny))
        
        ram = 25
        # Начальное условие: горячее пятно в центре
        r_i_min, r_i_max = max(0, ram), min(self.nx, self.nx - ram)
        r_j_min, r_j_max = max(0, ram), min(self.ny, self.ny - ram)
        
        if r_i_max > r_i_min and r_j_max > r_j_min:
            t[0, r_i_min:r_i_max, r_j_min:r_j_max] = 1200

        # Коэффициент температуропроводности
        alpha_const = self.lmbdzero / (self.rozero * self.cp)

        # Основной цикл расчета (векторизованный для производительности)
        for k in range(self.m - 1):
            t_k = t[k]
            
            # Вторые производные (центральная разность)
            d2t_dx2 = (t_k[2:, 1:-1] - 2*t_k[1:-1, 1:-1] + t_k[:-2, 1:-1]) / (self.dx**2)
            d2t_dy2 = (t_k[1:-1, 2:] - 2*t_k[1:-1, 1:-1] + t_k[1:-1, :-2]) / (self.dy**2)
            
            # Обновление внутренних узлов
            t[k+1, 1:-1, 1:-1] = t_k[1:-1, 1:-1] + alpha_const * self.dt * (d2t_dx2 + d2t_dy2)
            
            # Эмиссия прогресса
            self.progress.emit(int((k + 1) / (self.m - 1) * 100))
            
        self.finished.emit(t)

class ThermoExample01(PlotInterface):
    def __init__(self):
        super().__init__()

        # Параметры сетки (по умолчанию)
        self.nx = 70
        self.ny = 70
        self.m = 100
        self.L = 100

        # Параметры среды
        self.alpha = 3 * 10 ** -5
        self.rozero = 0.0027
        self.lmbdzero = 3
        self.cp = 800

        # Временные параметры
        self.tm = 100
        self.dt = self.tm / self.m
        
        self.__init_data()
        self.__init_thermo_ui()

    def __init_data(self):
        """Инициализация массивов данных на основе текущей сетки."""
        self.t = np.zeros((self.m, self.nx, self.ny))
        self.dx = self.L / self.nx
        self.dy = self.L / self.ny

    def __init_thermo_ui(self):
        # Создание вкладки
        thermo_layout = self.createTab('Thermo2D')
        
        # Получаем SliderBox для добавления элементов
        slider_box = self.tabAtr('Thermo2DSliderBox')
        
        # Кнопка расчета
        self.calc_button = QPushButton("Calculate Data")
        self.calc_button.clicked.connect(self.start_calculation)
        self.addToBox(slider_box, self.calc_button)
        
        # Контейнер для прогресс-бара и лейбла
        self.progress_container = QWidget()
        self.progress_layout = QHBoxLayout(self.progress_container)
        self.progress_layout.setContentsMargins(0, 5, 0, 5)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_label = QLabel("0%")
        
        self.progress_layout.addWidget(self.progress_bar)
        self.progress_layout.addWidget(self.progress_label)
        
        self.style_progress_bar()
        self.progress_container.setVisible(False)
        self.addToBox(slider_box, self.progress_container)
        
        # Слайдер для времени
        self.createSlider(0, self.m - 1, 
            tab=thermo_layout, 
            init=0, 
            func=self.update_thermo_plot, 
            name='Time Step', 
            label=True
        )

        # Слайдер для размера сетки
        self.createSlider(70, 400,
            tab=thermo_layout,
            init=70,
            func=self.change_grid_size,
            name='Grid Size (NX/NY)',
            label=True
        )

        # Подписка на событие изменения размера канваса (Задача 6)
        canvas = self.tabAtr('Thermo2DCanvas')
        canvas.mpl_connect('resize_event', self.on_canvas_resize)

        # Отрисовка осей и начального состояния
        self.draw_thermo_axes()
        self.draw_thermo_plot()

    def style_progress_bar(self):
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid {self.widgetColor};
                border-radius: 3px;
                background-color: {self.graphColor};
                height: 15px;
            }}
            QProgressBar::chunk {{
                background-color: {self.ticksColor};
            }}
        """)
        self.progress_label.setStyleSheet(f"color: {self.ticksColor}; font-weight: bold;")

    def change_grid_size(self, value):
        self.nx = value
        self.ny = value
        self.__init_data()
        
        label = getattr(self, "Grid Size (NX/NY) Slider Label", None)
        if label:
            label.setText(str(value))
            
        # Полная перерисовка
        self.draw_thermo_axes()
        self.draw_thermo_plot()

    def on_canvas_resize(self, event):
        """Обработчик изменения размера канваса для обновления размера точек (Задача 6)."""
        if hasattr(self, 'thermo_scatter'):
            new_s = self.calculate_marker_size()
            self.thermo_scatter.set_sizes([new_s])
            self.tabAtr('Thermo2DCanvas').draw_idle()

    @PlotInterface.canvasDraw(tab='Thermo2D')
    def draw_thermo_axes(self):
        fig = self.tabAtr('Thermo2DFigure')
        fig.clear()
        
        self.thermo_ax = self.createAxes(
            fig,
            args={
                'pos': 111,
                'name': '2D Heat Equation',
                'xAxName': 'X',
                'yAxName': 'Y',
                'grid': False
            }
        )
        self.thermo_ax.set_aspect(1)

    def calculate_marker_size(self):
        """Расчет размера квадратного маркера с проверкой на валидность (Задача 6)."""
        try:
            bbox = self.thermo_ax.get_window_extent()
            width = bbox.width
            # Проверка на валидность bbox (Задача 6)
            if width <= 1:
                return (72 / self.nx) ** 2
                
            dpi = self.thermo_ax.figure.dpi
            points_per_unit = (width / self.nx) * (72 / dpi)
            return points_per_unit ** 2
        except:
            return (72 / self.nx) ** 2

    @PlotInterface.canvasDraw(tab='Thermo2D')
    def draw_thermo_plot(self):
        x = np.linspace(0, 1, self.nx)
        y = np.linspace(0, 1, self.ny)
        X, Y = np.meshgrid(x, y)
        
        norm = plt.Normalize(vmin=0, vmax=1500)
        s_val = self.calculate_marker_size()
                
        self.thermo_scatter = self.thermo_ax.scatter(
            X.flatten(), 
            Y.flatten(), 
            c=self.t[0].flatten(), 
            cmap='coolwarm', 
            norm=norm, 
            edgecolors='none',
            marker='s',
            s=s_val
        )
        
        self.createColorbar(
            self.tabAtr('Thermo2DFigure'), 
            self.thermo_scatter, 
            name='T', 
            cmap='coolwarm'
        )
        
        # Убеждаемся, что размер рассчитан корректно сразу (Задача 6)
        self.on_canvas_resize(None)

    @PlotInterface.canvasDraw(tab='Thermo2D')
    def update_thermo_plot(self, value):
        if hasattr(self, 'thermo_scatter'):
            data_to_plot = self.t[value].flatten()
            if len(data_to_plot) == len(self.thermo_scatter.get_offsets()):
                self.thermo_scatter.set_array(data_to_plot)
                
            label = getattr(self, "Time Step Slider Label", None)
            if label:
                label.setText(str(value))

    def start_calculation(self):
        self.calc_button.setEnabled(False)
        self.progress_container.setVisible(True)
        self.progress_bar.setValue(0)
        self.progress_label.setText("0%")
        
        self.thread = QThread()
        self.worker = CalculationWorker(
            self.nx, self.ny, self.m, self.dt, self.dx, self.dy,
            self.lmbdzero, self.rozero, self.cp
        )
        self.worker.moveToThread(self.thread)
        
        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.update_progress_ui)
        self.worker.finished.connect(self.handle_calculation_finished)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        
        self.thread.start()

    def update_progress_ui(self, value):
        self.progress_bar.setValue(value)
        self.progress_label.setText(f"{value}%")

    def handle_calculation_finished(self, result):
        self.t = result
        self.calc_button.setEnabled(True)
        self.progress_container.setVisible(False)
        self.update_thermo_plot(0)
