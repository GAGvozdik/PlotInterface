import sys
import time
import numpy as np
from PyQt5.QtCore import Qt, QDir
from .graphObjects import GraphObjects
from pathlib import Path
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTabWidget, QPushButton, QVBoxLayout,
    QBoxLayout, QFileDialog, QMessageBox, QHBoxLayout, QLabel, QSlider,
    QGridLayout, QGroupBox, QDial, QSizePolicy, QSpacerItem, QMenu,
    QRadioButton, QButtonGroup, QComboBox, QScrollArea, QStyleFactory,
    QStyle, QStyleOptionSlider
)

try:
    import pywinstyles
except ImportError:
    pywinstyles = None

class TickSlider(QSlider):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self._ticks_color = QColor("#AAAAAA") 

    def setTicksColor(self, color_str):
        self._ticks_color = QColor(color_str)
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.tickPosition() == QSlider.NoTicks:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(self._ticks_color, 2)
        painter.setPen(pen)

        opt = QStyleOptionSlider()
        self.initStyleOption(opt)
        gr = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderGroove, self)
        handle = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderHandle, self)

        interval = self.tickInterval()
        if interval <= 0: interval = 1
        
        min_v, max_v = self.minimum(), self.maximum()
        if max_v <= min_v: return

        # Центрирование делений относительно дорожки
        for i in range(min_v, max_v + 1, interval):
            ratio = (i - min_v) / (max_v - min_v)
            # Учитываем, что центр ручки смещается от края до края
            x = gr.left() + handle.width()//2 + ratio * (gr.width() - handle.width())
            
            # Рисуем деления сверху и снизу
            painter.drawLine(int(x), gr.top() - 5, int(x), gr.top() - 12)
            painter.drawLine(int(x), gr.bottom() + 5, int(x), gr.bottom() + 12)
        
        painter.end()

class PlotInterface(GraphObjects):
    def __init__(self):
        super().__init__()  

        # Защита от повторной инициализации при динамической смене режимов
        if hasattr(self, '_setup_done') and self._setup_done:
            return

        self._setup_done = True
        self.setWindowTitle("Module plot interface")
        self.setGeometry(250, 100, 1600, 900)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        # Внедрение центрального виджета для QMainWindow
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.layout)

        # Боковая панель
        self.sidebar_widget = QWidget(self)
        self.sidebar_widget.setObjectName("sideBarContainer")
        self.sidebar_widget.setFixedWidth(300)
        self.sidebar_widget.setVisible(True) # Включаем видимость по умолчанию
        self.sidebar_layout = QVBoxLayout()
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)
        self.sidebar_layout.setSpacing(10)
        self.sidebar_widget.setLayout(self.sidebar_layout)
        
        # Добавляем в лейаут с коэффициентом растяжения 0 (не растягивается)
        self.layout.addWidget(self.sidebar_widget, 0)

        # Наполнение боковой панели
        self.sidebar_box = self.createBox(self.sidebar_layout, "NAVIGATION")
        self.sidebar_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.sidebar_box.layout().setSpacing(10)

        # Создание радиокнопок для режимов
        self.modeGroup = QButtonGroup(self)
        
        self.radio_general = QRadioButton("Geostatistics")
        self.radio_seismic = QRadioButton("Seismic")
        self.radio_thermo = QRadioButton("Thermodynamics")
        self.radio_atmospheric = QRadioButton("Atmospheric Physics")
        
        # По умолчанию выбираем атмосферную физику
        self.radio_atmospheric.setChecked(True)
        
        self.modeGroup.addButton(self.radio_general)
        self.modeGroup.addButton(self.radio_seismic)
        self.modeGroup.addButton(self.radio_thermo)
        self.modeGroup.addButton(self.radio_atmospheric)
        
        self.addToBox(self.sidebar_box, self.radio_general)
        self.addToBox(self.sidebar_box, self.radio_seismic)
        self.addToBox(self.sidebar_box, self.radio_thermo)
        self.addToBox(self.sidebar_box, self.radio_atmospheric)
        
        # Прижимаем кнопки к верху
        self.sidebar_box.layout().addStretch(1)

        # Блок переключения темы
        self.theme_box = self.createBox(self.sidebar_layout, "THEME")
        self.theme_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.theme_box.layout().setSpacing(10)

        self.themeGroup = QButtonGroup(self)
        self.radio_dark = QRadioButton("Dark")
        self.radio_light = QRadioButton("Light")
        
        self.radio_dark.setChecked(True)
        self.themeGroup.addButton(self.radio_dark)
        self.themeGroup.addButton(self.radio_light)
        
        self.addToBox(self.theme_box, self.radio_dark)
        self.addToBox(self.theme_box, self.radio_light)
        
        self.themeGroup.buttonClicked.connect(self.switchTheme)

        # Основной контент
        self.main_content_widget = QWidget(self)
        self.main_content_layout = QVBoxLayout()
        self.main_content_layout.setContentsMargins(10, 10, 10, 10)
        self.main_content_layout.setSpacing(0)
        self.main_content_widget.setLayout(self.main_content_layout)
        
        # Добавляем в лейаут с коэффициентом растяжения 1 (растягивается)
        self.layout.addWidget(self.main_content_widget, 1)

        # Кнопка переключения сайдбара
        self.toggle_sidebar_btn = QPushButton("☰")
        self.toggle_sidebar_btn.setFixedSize(50, 50)
        self.toggle_sidebar_btn.setFlat(True)
        self.toggle_sidebar_btn.setStyleSheet('''
            QPushButton {
                font-size: 24px;
                padding: 0px;
                margin: 0px 20px 19px 0px;
                border-radius: 0px;
                border: none;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: rgba(110, 110, 110, 50);
            }
        ''')
        self.toggle_sidebar_btn.clicked.connect(self.toggle_sidebar)

        self.tabs = QTabWidget()
        self.tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # Кнопка в левом верхнем углу вкладок
        self.tabs.setCornerWidget(self.toggle_sidebar_btn, Qt.TopLeftCorner)
        self.main_content_layout.addWidget(self.tabs)

        self.windowColor = '#2E2E2E'   
        self.widgetColor = '#6e6e6e'
        self.graphColor = '#4c4c4c'
        self.ticksColor = '#b5b5b5'
        self.gridColor = '#6e6e6e'
        self.ticksWidth = 2.5

        self.darkMode = True
        self.fileName = None

    def toggle_sidebar(self):
        # """Переключение видимости бового меню."""
        self.sidebar_widget.setVisible(not self.sidebar_widget.isVisible())
        
    def refreshActiveTab(self):
        # """Переопределяется в дочерних классах для обновления контента."""
        pass
        
    def switchTheme(self):
        # """Переключение тем оформления и синхронизация цветов графиков."""
        checked_button = self.themeGroup.checkedButton()
        if not checked_button:
            return
            
        self._force_refresh = True # Установка флага для принудительной перерисовки
        theme_name = checked_button.text().lower()
        current_dir = Path(__file__).parent.parent.resolve()
        qss_path = current_dir / "styles" / f"{theme_name}Theme.qss"
        
        # Обновляем цвета для matplotlib
        if theme_name == "dark":
            self.dividerColor = '#2E2E2E'   
            self.windowColor = self.dividerColor
            self.widgetColor = '#6e6e6e'
            self.graphColor = '#4c4c4c'
            self.ticksColor = '#b5b5b5'
            self.gridColor = '#6e6e6e'
            self.ticksWidth = 2.5
            self.darkMode = True
        else:
            self.dividerColor = '#FFFFFF'   
            self.windowColor = self.dividerColor
            self.gridColor = 'grey'
            self.widgetColor = 'black'
            self.graphColor = '#FFFFFF'
            self.ticksColor = 'black'
            self.ticksWidth = 1
            self.darkMode = False

        # Применяем QSS
        if qss_path.exists():
            with open(qss_path, "r") as f:
                QApplication.instance().setStyleSheet(f.read())
        
        # Обновляем все открытые вкладки и графики
        for i in range(self.tabs.count()):
            tab_name = self.tabs.tabText(i)
            figure = getattr(self, f"{tab_name}Figure", None)
            canvas = getattr(self, f"{tab_name}Canvas", None)
            
            if figure:
                # Обновляем фон фигуры
                figure.patch.set_facecolor(self.windowColor)
                # Обновляем стили всех осей в фигуре
                for ax in figure.axes:
                    self.updateAxesStyle(ax)
                
                # Перерисовываем холст
                if canvas:
                    canvas.draw()

        # Обновляем цвет делений на всех кастомных слайдерах
        for slider in self.findChildren(TickSlider):
            slider.setTicksColor(self.ticksColor)

        # Обновляем контент графиков (если реализовано в дочерних классах)
        self.refreshActiveTab()
        self._force_refresh = False # Сброс флага

        # Обновляем заголовок окна (Windows)
        if pywinstyles:
            try:
                style = "dark" if theme_name == "dark" else "normal"
                pywinstyles.apply_style(self, style)
            except Exception as e:
                print(f"Failed to apply pywinstyles: {e}")

    def clearTabs(self):
        """Полная очистка вкладок с удалением виджетов."""
        while self.tabs.count() > 0:
            widget = self.tabs.widget(0)
            self.tabs.removeTab(0)
            if widget:
                widget.setParent(None)
                widget.deleteLater()
            
    def createTab(self, name, columns=1):
        tab = QWidget()
        layout = QGridLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        # Устанавливаем растяжение для строки с графиком
        layout.setRowStretch(0, 1)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1) # Дополнительно для колонок графика
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, name)
        layout.setObjectName(name)
        setattr(self, name, layout)

        graphBox = self.createBox(layout, "Graph box", [0, 0, 1, 2])
        graphBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        setattr(self, f"{name}GraphBox", graphBox)

        # Создаем область прокрутки для слайдеров
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setFixedWidth(300 * columns + 25) # Запас для полосы прокрутки
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        layout.addWidget(scroll, 0, 2)

        sliderBox = self.createBox(None, "Sliders box", columns=columns)
        sliderBox.layout().setAlignment(Qt.AlignTop)
        sliderBox.setFixedWidth(300 * columns)
        sliderBox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        setattr(self, f"{name}SliderBox", sliderBox)
        
        scroll.setWidget(sliderBox)

        figure, canvas = self.createFigure(name, graphBox)
        setattr(self, f"{name}Figure", figure)
        setattr(self, f"{name}Canvas", canvas)

        saveButton = QPushButton("Save picture")
        saveButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        saveButton.setFixedHeight(60)
        saveButton.clicked.connect(self.saveFile)
        self.addToBox(sliderBox, saveButton)

        loadButton = QPushButton("Load file")
        loadButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        loadButton.setFixedHeight(60)
        loadButton.clicked.connect(self.get_file_way)
        # self.addToBox(sliderBox, loadButton)

        return layout

    def tabAtr(self, name):
        return getattr(self, f"{name}", None)

    def createSlider(self, min, max, tab, init=0, func='none', name='', label=False, isTicks=False, ticksInterval=0):
        # Если есть деления, увеличиваем высоту бокса со 110 до 130
        box_height = 130 if isTicks else 110
        sliderBox = self.createBox(tab, name, size=['auto', box_height], v=True)
        sliderBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Используем TickSlider вместо QSlider
        slider = TickSlider(Qt.Horizontal)
        slider.setMinimum(min)
        slider.setMaximum(max)
        slider.setValue(init)
        
        # Если есть деления, увеличиваем высоту слайдера с 40 до 60
        slider_height = 60 if isTicks else 40
        slider.setFixedHeight(slider_height)
        
        if isTicks: 
            slider.setProperty("hasTicks", True)
            slider.setTickPosition(QSlider.TicksBothSides)
            slider.setTickInterval(ticksInterval)
            # Инициализируем цвет делений из текущих настроек интерфейса
            slider.setTicksColor(self.ticksColor)

        # Применяем изменения стиля для динамических свойств
        slider.style().unpolish(slider)
        slider.style().polish(slider)

        if func != 'none':
            slider.valueChanged.connect(func)
        self.addToBox(sliderBox, slider)

        if label:
            label_widget = QLabel(str(init))
            setattr(self, f"{name} Slider Label", label_widget)
            self.addToBox(sliderBox, label_widget)

        setattr(self, f"{name} slider", slider)
        setattr(self, f"{name} Slider Box", sliderBox)
        self.addToBox(self.tabAtr(f'{tab.objectName()}SliderBox'), sliderBox)
        return sliderBox

    def createRangeSlider(self, min, max, tab, init=(0, 110), func='none', name='', label=False):
        try:
            from superqt import QRangeSlider
        except ImportError:
            print("superqt is not installed. Falling back to regular sliders.")
            return None

        sliderBox = self.createBox(tab, name, size=['auto', 110], v=True)
        sliderBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        slider = QRangeSlider(Qt.Horizontal)
        slider.setMinimum(min)
        slider.setMaximum(max)
        
        # Гарантируем кортеж для двух ползунков
        if isinstance(init, (int, float)):
            init = (min, int(init))
        slider.setValue(init)
        
        slider.setFixedHeight(40)
        # Сброс стилей, чтобы избежать скрытия ползунков глобальными QSS
        slider.setStyleSheet("QRangeSlider { background: transparent; }")
        
        # Улучшенная визуализация для superqt
        try:
            slider.setHandleLabelVisible(True)
            slider.setEdgeLabelVisible(False)
        except AttributeError:
            pass

        if func != 'none':
            slider.valueChanged.connect(func)
        self.addToBox(sliderBox, slider)

        if label:
            label_widget = QLabel(f"{init[0]} - {init[1]}")
            setattr(self, f"{name} Slider Label", label_widget)
            self.addToBox(sliderBox, label_widget)

        setattr(self, f"{name} slider", slider)
        self.addToBox(self.tabAtr(f'{tab.objectName()}SliderBox'), sliderBox)
        return sliderBox

    def createRadioGroup(self, options, tab, func='none', name=''):
        groupBox = self.createBox(tab, name, size=['auto', 'auto'], v=True)
        groupBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        buttonGroup = QButtonGroup(self)
        for i, option in enumerate(options):
            radio = QRadioButton(option)
            if i == 0:
                radio.setChecked(True)
            buttonGroup.addButton(radio, i)
            self.addToBox(groupBox, radio)
            
        if func != 'none':
            buttonGroup.buttonClicked.connect(func)
            
        setattr(self, f"{name} Group", buttonGroup)
        self.addToBox(self.tabAtr(f'{tab.objectName()}SliderBox'), groupBox)
        return buttonGroup

    def createQDial(self, min, max, init, tab, func='none', name='', label=False):
        dialBox = self.createBox(tab, name, size=['auto', 240])
        dialBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        dial = QDial(self)
        dial.setFixedSize(225, 150)
        dial.setRange(min, max)

        if func != 'none':
            dial.valueChanged.connect(func)

        self.addToBox(dialBox, dial)
        if label:
            label_widget = QLabel(str(init))
            setattr(self, f"{name} QDial Label", label_widget)
            self.addToBox(dialBox, label_widget)

        setattr(self, f"{name} QDial", dial)
        self.addToBox(self.tabAtr(f'{tab.objectName()}SliderBox'), dialBox)
        return dialBox

    def createBox(self, tab, title='', position=[], size=['none', 'none'], v=True, columns=1):
        box = QGroupBox(title)

        if isinstance(size[0], int) and isinstance(size[1], int):
            box.setFixedSize(size[0], size[1])
        elif size[0] == 'auto' and isinstance(size[1], int):
            box.setFixedHeight(size[1])
        elif isinstance(size[0], int) and size[1] == 'auto':
            box.setFixedWidth(size[0])

        if size == ['none', 'none']:
            box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        if position:
            tab.addWidget(box, *position)
        else:
            if hasattr(tab, "addWidget"):
                tab.addWidget(box)

        # Основной лейаут бокса всегда вертикальный для поддержки spanning-виджетов
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(15)
        main_layout.setAlignment(Qt.AlignTop)
        box.setLayout(main_layout)

        if columns > 1:
            # Контейнер для колонок
            col_container = QHBoxLayout()
            col_container.setContentsMargins(0, 0, 0, 0)
            col_container.setSpacing(15)
            col_container.setAlignment(Qt.AlignTop)
            main_layout.addLayout(col_container)

            box._column_layouts = []
            box._next_column = 0
            box._columns = columns

            for _ in range(columns):
                col_layout = QVBoxLayout()
                col_layout.setContentsMargins(0, 0, 0, 0)
                col_layout.setSpacing(15)
                col_layout.setAlignment(Qt.AlignTop)

                col_container.addLayout(col_layout, 1)
                box._column_layouts.append(col_layout)

        elif not v:
            # Если колонка одна и нужен горизонтальный вид — пересоздаем лейаут
            h_layout = QHBoxLayout()
            h_layout.setContentsMargins(0, 0, 0, 0)
            h_layout.setSpacing(15)
            h_layout.setAlignment(Qt.AlignTop)
            main_layout.addLayout(h_layout)
            box._internal_h_layout = h_layout

        return box

    def addToBox(self, box, widget):
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Если box многоколоночный — добавляем в одну из вертикальных колонок
        if hasattr(box, "_column_layouts"):
            col = box._next_column
            box._column_layouts[col].addWidget(widget)

            col += 1
            if col >= box._columns:
                col = 0
            box._next_column = col
        elif hasattr(box, "_internal_h_layout"):
            box._internal_h_layout.addWidget(widget)
        else:
            box.layout().addWidget(widget)

    def updateAxesStyle(self, ax):
        ax.set_facecolor(self.graphColor)
        ax.set_frame_on(True)
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color(self.widgetColor)
            spine.set_linewidth(2.0)
        ax.tick_params(axis='both', labelcolor=self.ticksColor, color=self.widgetColor, width=self.ticksWidth)
        ax.xaxis.label.set_color(self.ticksColor)
        ax.yaxis.label.set_color(self.ticksColor)
        ax.title.set_color(self.ticksColor)

    @staticmethod
    def getWorkTime(name):
        def decorator(func):
            def wrapper(self, *args, **kwargs):
                start_time = time.time()
                result = func(self, *args, **kwargs)
                end_time = time.time()
                print(f"Max {name} method work time: {end_time - start_time:.4f} s")
                return result
            return wrapper
        return decorator

    @staticmethod
    def canvasDraw(tab):
        def decorator(func):
            def wrapper(self, *args, **kwargs):
                result = func(self, *args, **kwargs)
                canvas = getattr(self, f'{tab}Canvas', None)
                if canvas:
                    canvas.draw()
                return result
            return wrapper
        return decorator

    def saveFile(self):
        try:
            current_index = self.tabs.currentIndex()
            current_tab_name = self.tabs.tabText(current_index)
            figure = getattr(self, f"{current_tab_name}Figure", None)
            way = self.save_file()
            if way:
                figure.savefig(way, transparent=True, dpi=400)
        except: pass

    def get_file_way(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Choose the file")
        if fileName: self.fileName = fileName

    def save_file(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Save picture", "", "PNG Images (*.png)")
        return fileName if fileName else None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlotInterface()
    window.show()
    sys.exit(app.exec_())
