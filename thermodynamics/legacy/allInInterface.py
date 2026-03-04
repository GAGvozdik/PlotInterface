import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from furierFunc import Furier
from splain import mySpline
from PyQt5.QtCore import Qt

def meth_progonki(lower_diagonal, main_diagonal, upper_diagonal, right_part, n):
    alpha = [-upper_diagonal[0] / main_diagonal[0]]
    beta = [right_part[0] / main_diagonal[0]]

    for i in range(1, n):
        alpha.append(-upper_diagonal[i] / (lower_diagonal[i] * alpha[i - 1] + main_diagonal[i]))
        beta.append(
            (right_part[i] - lower_diagonal[i] * beta[i - 1]) / (lower_diagonal[i] * alpha[i - 1] + main_diagonal[i]))
    x = [0] * n
    x[n - 1] = beta[n - 1]

    for i in range(n - 1, 0, -1):
        x[i - 1] = alpha[i - 1] * x[i] + beta[i - 1]

    return x



class GraphWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.blue = '#1A5F7A'

        self.text_color = '#f5f5dc'
        self.line = 'green'
        self.window_color = '#159895'
        self.graph_color = '#57C5B6'

        self.result_color = 'green'
        self.func_color = 'orange'
        self.tm_color = 'red'

        self.button_color = self.graph_color

        self.figure = plt.figure()
        self.ax1 = self.figure.add_subplot(111)
        self.ax1.grid(True, color=self.text_color)

        self.canvas = FigureCanvas(self.figure)
        self.ax1.set_facecolor(self.graph_color)
        self.figure.patch.set_facecolor(self.window_color)
        self.ax1.spines['left'].set_color(self.text_color)  # Цвет левой оси
        self.ax1.spines["right"].set_color(self.text_color)  # Цвет левой оси
        self.ax1.spines['bottom'].set_color(self.text_color)  # Цвет левой оси
        self.ax1.spines['top'].set_color(self.text_color)  # Цвет левой оси

        self.ax1.set_xlabel('X Label', color=self.text_color)  # Цвет подписи x-оси
        self.ax1.set_ylabel('Y Label', color=self.text_color)  # Цвет подписи y-оси
        self.ax1.tick_params(axis='x', colors=self.text_color)  # Устанавливаем цвет подписей значений по оси x
        self.ax1.tick_params(axis='y', colors=self.text_color)  #
        self.setStyleSheet(
            "QWidget {"
            "background-color: " + self.blue + ";"  # Серый фон для всего приложения
            "color: " + self.text_color + ";"  # Белый цвет текста для всего приложения
            "}"

            "QGroupBox {"
            "background-color: " + self.blue + ";"  # Серый фон для QGroupBox
            "border: 0px solid " + self.line + ";"  # Серая граница
            "border-radius: 12px;"  # Закругление углов
            "margin-top: 1ex;"  # Верхний отступ
            "}"

            "QGroupBox::title {"
            "subcontrol-origin: margin;"
            "subcontrol-position: top center;"
            "padding: 0 3px;"  # Отступ для заголовка
            "}"

            "QLabel {"
            "color: " + self.text_color + ";"  # Белый цвет текста для QLabel
            "}"

            "QCheckBox, QRadioButton {"
            "color: " + self.text_color + ";"  # Белый цвет текста для QCheckBox и QRadioButton
            "}"

            "QPushButton {"
            "color: " + self.button_color + ";"  # Белый цвет текста для кнопок
            "}"

        )

        self.setWindowTitle('Численные методы')
        self.setGeometry(200, 200, 1500, 1000)

        layout = QVBoxLayout()

        self.n = 21
        self.my_m = 4

        self.ynoize = np.array([])
        self.y = np.zeros(5)


        self.sin_button = QRadioButton('Синус')
        self.cos_button = QRadioButton('Хэвисайд')
        self.pol_button = QRadioButton('Полином 3 степени')
        self.func_button = QRadioButton('sin(0.2 * x) + 2 * cos(x) - 1.5 * sin(3 * x)')
        self.ode_func_button = QRadioButton('2 * x ** (3/2) / 3 + 2')



        self.ode_button = QRadioButton("Рунге Кутт")
        self.ode_button.clicked.connect(self.on_radio_toggled)
        self.ode_button.clicked.connect(self.on_furier_untoggled)


        self.splain_button = QRadioButton("Splain")
        self.lstq_button = QRadioButton("Метод наименьших квадратов")
        self.splain_button.clicked.connect(self.on_radio_untoggled)
        self.lstq_button.clicked.connect(self.on_radio_untoggled)
        self.splain_button.clicked.connect(self.on_heat_untoggled)
        self.lstq_button.clicked.connect(self.on_heat_untoggled)
        self.splain_button.clicked.connect(self.on_furier_untoggled)
        self.lstq_button.clicked.connect(self.on_furier_untoggled)

        self.heat_button = QRadioButton("Тепловой балланс")
        self.heat_button.clicked.connect(self.on_radio_untoggled)
        self.heat_button.clicked.connect(self.on_heat_toggled)
        self.heat_button.clicked.connect(self.on_furier_untoggled)

        # Добавляю полосы прокрутки
        self.scroll_bar = QScrollBar(Qt.Horizontal)
        self.scroll_bar.setMinimum(50)
        self.scroll_bar.setMaximum(120)
        self.scroll_bar.setValue(51)  # Устанавливаем начальное значение
        self.scroll_bar.valueChanged.connect(self.update_n_points)
        # self.scroll_bar.valueChanged.connect(self.addNoize)
        # setting style sheet


        self.noizeCheckBox = QCheckBox("Шумм", self)
        self.noizeCheckBox.clicked.connect(self.addNoize)

        self.plot_button = QPushButton('Построить график')
        self.plot_button.clicked.connect(self.updateGraph)


        self.furier_button = QRadioButton("Фурье")
        self.furier_button.clicked.connect(self.on_radio_untoggled)
        self.furier_button.clicked.connect(self.on_heat_untoggled)
        self.furier_button.clicked.connect(self.on_furier_toggled)

        self.scroll_bar1 = QScrollBar(Qt.Horizontal)
        self.scroll_bar1.setVisible(False)
        self.scroll_bar1.setMinimum(0)
        self.scroll_bar1.setMaximum(24)
        self.scroll_bar1.setValue(8)  # Устанавливаем начальное значение
        self.scroll_bar1.valueChanged.connect(self.update_m)


        methodBox = QGroupBox()
        vbox1 = QVBoxLayout()
        methodBox.setLayout(vbox1)

        vbox1.addWidget(self.ode_button)
        vbox1.addWidget(self.lstq_button)

        vbox1.addWidget(self.heat_button)
        vbox1.addWidget(self.splain_button)

        vbox1.addWidget(self.furier_button)


        self.commonBox = QGroupBox("Настройки ввода")
        vbox2 = QVBoxLayout()
        self.commonBox.setLayout(vbox2)

        # добавляю кпопки функций
        vbox2.addWidget(self.sin_button)
        vbox2.addWidget(self.cos_button)
        vbox2.addWidget(self.pol_button)
        vbox2.addWidget(self.func_button)
        vbox2.addWidget(self.noizeCheckBox)
        vbox2.addWidget(self.scroll_bar1)
        vbox2.addWidget(self.scroll_bar)
        vbox2.addWidget(self.plot_button)

        # ode
        # Добавляю полосы прокрутки
        self.ode_scroll_bar = QScrollBar(Qt.Horizontal)
        self.ode_scroll_bar.setMinimum(50)
        self.ode_scroll_bar.setMaximum(100)
        self.ode_scroll_bar.setValue(50)  # Устанавливаем начальное значение
        self.ode_scroll_bar.valueChanged.connect(self.update_n_points)

        self.ode_plot_button = QPushButton('Построить график')
        self.ode_plot_button.clicked.connect(self.updateGraph)

        self.odeBox = QGroupBox("")
        self.odeBox.setVisible(False)
        vbox2 = QVBoxLayout()
        self.odeBox.setLayout(vbox2)

        # добавляю кпопки функций
        vbox2.addWidget(self.ode_func_button)
        vbox2.addWidget(self.ode_scroll_bar)
        vbox2.addWidget(self.ode_plot_button)

        ## heat
        self.changingT = 0

        self.t1 = QLineEdit()
        self.t1Label = QLabel('T1')
        self.t2 = QLineEdit()
        self.t2Label = QLabel('T2')
        self.g1 = QLineEdit()
        self.g1Label = QLabel('G1')
        self.g2 = QLineEdit()
        self.g2Label = QLabel('G2')


        self.update_button = QPushButton('Построить график')
        self.update_button.clicked.connect(self.update_graph)

        self.error_label = QLabel('')

        self.scroll_bar3 = QScrollBar(Qt.Horizontal)
        self.scroll_bar3.setMinimum(0)
        self.scroll_bar3.setMaximum(999)
        self.scroll_bar3.setValue(0)  # Устанавливаем начальное значение
        self.scroll_bar3.valueChanged.connect(self.update_tm)

        self.heatBox = QGroupBox("Тепловой балланс")
        self.heatBox.setVisible(False)
        vbox4 = QVBoxLayout()
        self.heatBox.setLayout(vbox4)

        # добавляю кпопки функций
        vbox4.addWidget(self.t1Label)
        vbox4.addWidget(self.t1)
        vbox4.addWidget(self.t2Label)
        vbox4.addWidget(self.t2)
        vbox4.addWidget(self.g1Label)
        vbox4.addWidget(self.g1)
        vbox4.addWidget(self.g2Label)
        vbox4.addWidget(self.g2)
        vbox4.addWidget(self.scroll_bar3)
        vbox4.addWidget(self.update_button)
        vbox4.addWidget(self.error_label)

        panelBox1 = QGroupBox("График")
        vbox3 = QVBoxLayout()
        panelBox1.setLayout(vbox3)
        vbox3.addWidget(self.canvas)

        self.darkteam = QRadioButton('dark')
        self.normalteam = QRadioButton('light')
        self.darkteam.clicked.connect(self.darkTeam)
        self.normalteam.clicked.connect(self.darkTeam)

        self.darkBox = QGroupBox("")
        self.darkBox.setVisible(False)
        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.darkteam)
        vbox2.addWidget(self.normalteam)
        self.darkBox.setLayout(vbox2)

        panelBox2 = QGroupBox("Параметры")
        vbox4 = QVBoxLayout()
        panelBox2.setLayout(vbox4)

        vbox4.addWidget(methodBox)
        vbox4.addWidget(self.commonBox)
        vbox4.addWidget(self.odeBox)
        vbox4.addWidget(self.heatBox)


        # добавляю кпопки функций

        #
        vbox2.addWidget(self.ode_func_button)


        vbox4.addWidget(self.darkteam)
        vbox4.addWidget(self.normalteam)


        vbox4.addWidget(self.darkBox)

        panelBox = QGroupBox("Методы")
        layout.addWidget(panelBox)
        vbox5 = QHBoxLayout()
        panelBox.setLayout(vbox5)

        vbox5.addWidget(panelBox1, 3)
        vbox5.addWidget(panelBox2, 1)

        layout.addLayout(layout)

        self.setLayout(layout)
        self.count = 0

        self.plot_triggered = False  # Переменная для отслеживания нажатия кнопки

    def on_radio_toggled(self):
        if self.ode_button.isChecked():
            self.commonBox.setVisible(False)
            self.odeBox.setVisible(True)

    def darkTeam(self):
        if self.darkteam.isChecked():
            self.ax1.set_facecolor(self.graph_color)
            self.figure.patch.set_facecolor(self.window_color)
            self.ax1.spines['left'].set_color(self.text_color)  # Цвет левой оси
            self.ax1.spines["right"].set_color(self.text_color)  # Цвет левой оси
            self.ax1.spines['bottom'].set_color(self.text_color)  # Цвет левой оси
            self.ax1.spines['top'].set_color(self.text_color)  # Цвет левой оси

            self.ax1.set_xlabel('X Label', color=self.text_color)  # Цвет подписи x-оси
            self.ax1.set_ylabel('Y Label', color=self.text_color)  # Цвет подписи y-оси
            self.ax1.tick_params(axis='x', colors=self.text_color)  # Устанавливаем цвет подписей значений по оси x
            self.ax1.tick_params(axis='y', colors=self.text_color)  #
            self.ax1.grid(True, color=self.text_color)
            self.setStyleSheet(
                "QWidget {"
                "background-color: " + self.blue + ";"  # Серый фон для всего приложения
                "color: " + self.text_color + ";"  # Белый цвет текста для всего приложения
                "}"

                "QGroupBox {"
                "background-color: " + self.blue + ";"  # Серый фон для QGroupBox
                "border: 0px solid " + self.line + ";"  # Серая граница
                "border-radius: 12px;"  # Закругление углов
                "margin-top: 1ex;"  # Верхний отступ
                "}"

                "QGroupBox::title {"
                "subcontrol-origin: margin;"
                "subcontrol-position: top center;"
                "padding: 0 3px;"  # Отступ для заголовка
                "}"

                "QLabel {"
                "color: " + self.text_color + ";"  # Белый цвет текста для QLabel
                "}"

                "QCheckBox, QRadioButton {"
                "color: " + self.text_color + ";"  # Белый цвет текста для QCheckBox и QRadioButton
                "}"

                "QPushButton {"
                "color: " + self.button_color + ";"  # Белый цвет текста для кнопок
                "}"

                "QPushButton#plot_button {"
                "background-color: " + self.button_color + ";"  # Серый цвет для кнопки построения графика
                "color: " + self.button_color + ";"
                "}"
            )
        if self.normalteam.isChecked():
            self.setStyleSheet('')
            self.ax1.set_facecolor('white')
            self.figure.patch.set_facecolor('white')
            self.ax1.spines['left'].set_color('black')  # Цвет левой оси
            self.ax1.spines["right"].set_color('black')  # Цвет левой оси
            self.ax1.spines['bottom'].set_color('black')  # Цвет левой оси
            self.ax1.spines['top'].set_color('black')  # Цвет левой оси

            self.ax1.set_xlabel('X Label', color='black')  # Цвет подписи x-оси
            self.ax1.set_ylabel('Y Label', color='black')  # Цвет подписи y-оси
            self.ax1.tick_params(axis='x', colors='black')  # Устанавливаем цвет подписей значений по оси x
            self.ax1.tick_params(axis='y', colors='black')  #
            self.ax1.grid(True, color='grey')

    def on_radio_untoggled(self):
        if self.splain_button.isChecked() or self.furier_button.isChecked() or self.lstq_button.isChecked():
            self.commonBox.setVisible(True)
            self.odeBox.setVisible(False)



    def on_heat_toggled(self):
        if self.heat_button.isChecked():
            self.heatBox.setVisible(True)
            self.commonBox.setVisible(False)
            self.odeBox.setVisible(False)

    def on_heat_untoggled(self):
        if self.splain_button.isChecked() or self.furier_button.isChecked() or self.lstq_button.isChecked():
            self.heatBox.setVisible(False)
            self.commonBox.setVisible(True)
            self.odeBox.setVisible(False)

    def on_furier_toggled(self):
        # return 0
        if self.furier_button.isChecked():
            self.scroll_bar1.setVisible(True)
            self.odeBox.setVisible(False)

    def on_furier_untoggled(self):
        self.scroll_bar1.setVisible(False)




    def addNoize(self):
        if (self.noizeCheckBox.isChecked()):
            if np.max(self.y) - np.min(self.y) == 0:
                self.ynoize = np.random.normal(0, 0.01, self.n + 1)
            else:
                self.ynoize = np.random.normal(0, (np.max(self.y) - np.min(self.y)) / 20, self.n + 1)

            # self.ynoize = np.zeros(len(self.y))
        pass

    def update_n_points(self, n):
        if self.count > 0:
            self.n = n
            self.addNoize()

        self.plot_graph(n)

    def updateGraph(self):
        if self.noizeCheckBox.isChecked():
            self.addNoize()
        self.count += 1
        self.plot_graph(self.n)

    def update_m(self, m):

        if self.count > 0:
            self.my_m = m
            self.plot_graph(self.n)


    def setAxesLimit(self):
        if self.sin_button.isChecked():
            a, b, c, d = -0.1, 4.1, -0.85, 1.2
        elif self.cos_button.isChecked():
            a, b, c, d = -0.1, 4.1, -0.3, 1.3
        elif self.pol_button.isChecked():
            a, b, c, d = -0.1, 4.1, -30, 350
        elif self.func_button.isChecked():
            a, b, c, d = -0.1, 4.1, -4, 4
        # elif self.ode_func_button.isChecked():
        #     a, b, c, d = -0.1, 4.1, 0, 10
        else:
            return 0
        self.ax1.set_xlim(a, b)
        self.ax1.set_ylim(c, d)

    def plot_graph(self, n):

        self.ax1.clear()

        self.darkTeam()

        # self.plt.set_xlim(np.min(self.x), np.min(self.y))

        t = 4
        x = np.linspace(0, t, n + 1)

        if self.sin_button.isChecked():
            y = np.sin(x)
        elif self.cos_button.isChecked():
            y = np.heaviside(x - 2, 1)
        elif self.pol_button.isChecked():
            y = 1 + 2 * x + 3 * x ** 2 + 4 * x ** 3
        elif self.func_button.isChecked():
            y = np.sin(0.2 * x) + 2 * np.cos(x) - 1.5 * np.sin(3 * x)
        elif self.ode_func_button.isChecked():
            y = 2 * x ** (3/2) / 3 + 2
        elif self.ode_button.isChecked():
            y = 2 * x ** (3/2) / 3 + 2
        else:
            fig = self.figure
            self.canvas.figure = fig
            self.canvas.draw()
            return 0

        self.y = y

        if self.noizeCheckBox.isChecked():
            y += self.ynoize
        if self.furier_button.isChecked():
            self.plot_furier(self.n, x, y, t, self.my_m)
        elif self.splain_button.isChecked():
            self.plot_splain(self.n, x, y)
        elif self.ode_button.isChecked():
            self.plot_ode(self.n, x, y)
        elif self.lstq_button.isChecked():
            self.plot_lstq(self.n, x, y)

    # ax1.set_xlim(0, 10)

    def plot_ode(self, n=100, x=np.array([]), y=np.array([])):

        fig = self.figure

        self.ax1.plot(x, y, c=self.func_color)
        self.ax1.scatter(x, y, c=self.func_color)

        a = 0
        b = 2

        x = np.linspace(a, b, n)

        yn = 2 * x ** (3/2) / 3 + 2
        # yn = 1 / 4 * (x + 2) ** 2
        # yn = 2 * np.e ** x

        y = np.zeros(n)
        y[0] = 2

        def func(x, y):
            return x ** 0.5



        self.ax1.plot(x, yn, c=self.func_color)
        self.ax1.scatter(x, yn, c=self.func_color, s=9)

        h = x[1] - x[0]

        for i in range(n - 1):
            k1 = h * func(x[i], y[i])
            k2 = h * func(x[i] + h / 2, y[i] + k1 / 2)
            k3 = h * func(x[i] + h / 2, y[i] + k2 / 2)
            k4 = h * func(x[i] + h, y[i] + k3)

            y[i + 1] = y[i] + (k1 + 2 * k2 + 2 * k3 + k4) / 6
            # if x[i] > 20:
            #     y[i] = 0

        self.ax1.scatter(x, y, c=self.func_color, s=7)
        self.ax1.plot(x, y, c=self.func_color)

        self.canvas.figure = fig
        self.setAxesLimit()
        self.canvas.draw()


    def plot_furier(self, n=4, x=np.array([]), y=np.array([]), t=4, m = 4):

        fig = self.figure

        self.ax1.plot(x, y, c=self.func_color)
        self.ax1.scatter(x, y, c=self.func_color)

        resPoints = Furier(x, y, t, n, m)
        # resPoints = Furier(x, y, t, n, int(n / 2))
        #
        # print('resPoints.ti()')
        # print(resPoints.ti())
        # print('resPoints.yrmass()')
        # print(resPoints.yrmass())
        #
        # print('n')
        # print(n)
        # print('self.my_m')
        # print(self.my_m)
        #
        #
        try:
            print(len(resPoints.yrmass()))

            self.ax1.plot(resPoints.ti(), resPoints.yrmass(), c=self.result_color)
            self.ax1.scatter(resPoints.ti(), resPoints.yrmass(), c=self.result_color)
            # #
            # #
            self.canvas.figure = fig
            self.setAxesLimit()
            self.canvas.draw()
        except:
            self.canvas.figure = fig
            self.setAxesLimit()
            self.canvas.draw()

        # self.ax1.plot(resPoints.ti(), resPoints.yrmass(), c='green')
        # self.ax1.scatter(resPoints.ti(), resPoints.yrmass(), c='green')
        # self.canvas.figure = fig
        # self.setAxesLimit()
        # self.canvas.draw()




    def plot_lstq(self, n=100, x=np.array([]), y=np.array([])):

        self.ax1.plot(x, y, c=self.func_color)
        self.ax1.scatter(x, y, c=self.func_color)


        # common parameters
        N = len(x)
        lineWidth = 2.5
        dWidth = 0.25
        pointSize = 1

        ############################################################################
        # calculate parameters
        ############################################################################

        A = (N * np.sum(x * y) - np.sum(x) * np.sum(y)) / (N * np.sum(x ** 2) - np.sum(x) ** 2)
        B = np.sum(y) / N - A * np.sum(x) / N

        C = (N * np.sum(x * y) - np.sum(x) * np.sum(y)) / (N * np.sum(y ** 2) - np.sum(y) ** 2)
        D = np.sum(x) / N - C * np.sum(y) / N

        Sa = ((np.sum(y ** 2) - A * np.sum(x * y)) / ((N - 2) * (np.sum(x ** 2) - (np.sum(x / N)) ** 2))) ** 0.5
        Sb = Sa * ((np.sum(x) / N) ** 2 + np.sum((x - np.sum(x) / N)) ** 2 / N) ** 0.5

        studA = np.abs(A) / Sa
        studB = np.abs(B) / Sb
        pirs = (np.abs(A * C)) ** 0.5


        ############################################################################
        # plot y = f(x)
        ############################################################################
        # dyi plot
        for i in range(N):
            dy = A * x[i] + B
            self.ax1.plot(
                [x[i], x[i]], [y[i], dy],
                color="grey",
                zorder=1,
                linewidth=dWidth
            )

        # x trend
        self.ax1.plot(
            np.linspace(min(x) - 1, max(x) + 1, 100),
            A * np.linspace(min(x) - 1, max(x) + 1, 100) + B,
            zorder=3,
            color="darkslategrey",
            linewidth=lineWidth
        )

        # points
        self.ax1.scatter(
            x,
            y,
            s=pointSize,
            zorder=2,
            color="mediumseagreen"
        )

        # show parameters labels
        label = 'A = ' + str(round(A, 2))
        label += '\nB = ' + str(round(B, 2))
        label += '\nC = ' + str(round(C, 2))
        label += '\nD = ' + str(round(D, 2))

        label += '\nSa = ' + str(round(Sa, 5))
        label += '\nSb = ' + str(round(Sb, 2))
        label += '\nstudA = ' + str(round(studA, 2))
        label += '\nstudB = ' + str(round(studB, 2))
        label += '\npirs = ' + str(round(pirs, 2))
        label += '\nN = ' + str(N)

        # plt.legend()

        self.canvas.figure = self.figure
        self.setAxesLimit()
        self.canvas.draw()


    def plot_splain(self, n=100, x=np.array([]), y=np.array([])):

        splainK = mySpline(x, y, n)
        polA = splainK[0]
        polB = splainK[1]
        polC = splainK[2]
        polD = splainK[3]

        fig = self.figure

        # function
        self.ax1.plot(
            x,
            y,
            zorder=1,
            color="lightgrey",
            linewidth=4
        )

        # functioon points
        self.ax1.scatter(
            x,
            y,
            s=13,
            zorder=2,
            color="grey"
        )

        # splain line
        for i in range(1, n):

            xx = np.linspace(x[i - 1], x[i], n)
            yy = polA[i] + (xx - x[i]) * (polB[i] + (xx - x[i]) * (polC[i] / 2.0 + (xx - x[i]) * polD[i] / 6.0))

            # splain
            self.ax1.plot(
                xx,
                yy,
                zorder=3,
                linewidth=2
            )

        plt.legend()
        self.canvas.figure = fig
        self.setAxesLimit()
        self.canvas.draw()

    def update_tm(self, t):

        l = 10
        N = 100

        L = np.arange(0, l, l / (N - 1))
        L = np.append(L, l)


        if self.plot_triggered == True:
            self.update_graph()

            self.ax1.scatter(L[:-1], self.mass[t][:-1], c=self.tm_color, s=15, zorder=3)
            self.canvas.draw()

    def update_graph(self):


        t1_text = self.t1.text()
        t2_text = self.t2.text()
        g1_text = self.g1.text()
        g2_text = self.g2.text()

        if not (g1_text.replace('.', '', 1).replace('-', '', 1).isdigit()
                and g2_text.replace('.', '', 1).replace('-', '', 1).isdigit()
                and t1_text.replace('.', '', 1).replace('-', '', 1).isdigit()
                and t2_text.replace('.', '', 1).replace('-', '', 1).isdigit()):
            self.error_label.setText('Ошибка: Введите число')
            return 0

        t1 = float(t1_text)
        t2 = float(t2_text)
        G1 = float(g1_text)
        G2 = float(g2_text)

        self.plot_triggered = True  # Устанавливаем флаг нажатия кнопки

        # if x_min >= x_max or y_min >= y_max:
        #     self.error_label.setText('Ошибка: Минимальное значение должно быть меньше максимального')
        #     return

        self.error_label.setText('')
        self.ax1.clear()

        # известные параметры
        l = 10
        tm = 10000
        xi = 10 ** (-6)

        N = 100
        M = 10

        # рисуем исходный график
        L = np.arange(0, l, l / (N - 1))
        L = np.append(L, l)

        t = np.arange(0, tm, tm / (M - 1))
        t = np.append(t, tm)

        T = []
        for ln in L:
            if ln <= l / 2:
                T.append(t1)
            else:
                T.append(t2)



        self.ax1.plot(L[:-1], T[:-1], zorder=1)

        # считаем коэфиициент P
        dt = tm / M
        dx = l / N
        P = xi * dt / (dx ** 2)

        self.mass = []
        D = T

        for tm in t:
            for l in L:
                A = [0.0]
                B = [1.0]
                C = [0.0]
                D[0] = t1

                # G1
                D[0] = G1 * dx

                for i in range(N - 1):
                    A.append(-P)
                    B.append(1 + 2 * P)
                    C.append(-P)

                A.append(-1)
                B.append(1)
                C.append(0)

                D[N - 1] = G2 * dx
                self.mass.append(meth_progonki(A, B, C, D, N))
                D = self.mass[-1]

            self.ax1.scatter(L[:-1], self.mass[-1][:-1], c=self.func_color, s=12, zorder=2)

        # self.ax1.scatter(L[:-1], self.mass[self.changingT][:-1], c="#4e7d8e", s=0.9)

        self.canvas.draw()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GraphWindow()
    window.show()
    sys.exit(app.exec_())

