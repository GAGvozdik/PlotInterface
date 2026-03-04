import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import *
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


class SinusGraphWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.mass = []

        self.setWindowTitle(
            'Решение 1D ур-я теплопроводности с заданными начальными и граничными условиями неявным методом')

        self.changingT = 0

        self.figure, self.ax1 = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        self.panel = QGroupBox("Параметры")
        vbox = QHBoxLayout()
        self.panel.setLayout(vbox)

        self.t1 = QLineEdit()
        self.t1Label = QLabel('T1')
        self.t2 = QLineEdit()
        self.t2Label = QLabel('T2')
        self.g1 = QLineEdit()
        self.g1Label = QLabel('G1')
        self.g2 = QLineEdit()
        self.g2Label = QLabel('G2')

        vbox.addWidget(self.t1Label)
        vbox.addWidget(self.t1)
        vbox.addWidget(self.t2Label)
        vbox.addWidget(self.t2)
        vbox.addWidget(self.g1Label)
        vbox.addWidget(self.g1)
        vbox.addWidget(self.g2Label)
        vbox.addWidget(self.g2)

        self.update_button = QPushButton('Plot graph')
        self.update_button.clicked.connect(self.update_graph)

        self.error_label = QLabel('')

        self.scroll_bar = QScrollBar(Qt.Horizontal)
        self.scroll_bar.setMinimum(0)
        self.scroll_bar.setMaximum(999)
        self.scroll_bar.setValue(0)  # Устанавливаем начальное значение
        self.scroll_bar.valueChanged.connect(self.update_tm)




        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        layout.addWidget(self.canvas)
        layout.addWidget(self.panel)
        layout.addWidget(self.scroll_bar)
        layout.addWidget(self.update_button)
        layout.addWidget(self.error_label)

        self.plot_triggered = False  # Переменная для отслеживания нажатия кнопки


    def update_tm(self, t):

        l = 10
        N = 100

        L = np.arange(0, l, l / (N - 1))
        L = np.append(L, l)


        if self.plot_triggered == True:
            self.update_graph()

            self.ax1.scatter(L[:-1], self.mass[t][:-1], c="red", s=1.9, zorder=3)
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

            self.ax1.scatter(L[:-1], self.mass[-1][:-1], c="orange", s=0.6, zorder=2)

        # self.ax1.scatter(L[:-1], self.mass[self.changingT][:-1], c="red", s=0.9)

        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SinusGraphWindow()
    window.show()
    sys.exit(app.exec_())