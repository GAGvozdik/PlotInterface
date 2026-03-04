import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import sys
from pathlib import Path
import wget
import re
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSlider
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QCheckBox
# import py2exe

from PyQt5.QtWidgets import QComboBox
import time


class ParabolaGraph(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Parabola Graph')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.nx = 100
        self.ny = 100
        self.m = 100
        self.L = 100

        self.tSlider = QSlider(Qt.Horizontal)
        self.tSlider.setMinimum(0)
        self.tSlider.setMaximum(self.m)
        self.tSlider.setValue(0)
        self.tSlider.setTickInterval(1)
        self.tSlider.setTickPosition(QSlider.TicksBelow)
        self.tSlider.valueChanged.connect(self.updateT)

        self.button = QPushButton('Load data')
        self.button.clicked.connect(self.calculateData)

        self.alpha = 3 * 10 ^ (-5)
        self.rozero = 0.0027

        self.lmbdzero = 3
        self.cp = 800

        self.ro = np.zeros([self.m, self.nx, self.ny])
        self.lmbd = np.zeros([self.m, self.nx, self.ny])
        self.c = np.zeros([self.m, self.nx, self.ny])
        self.t = np.zeros([self.m, self.nx, self.ny])

        self.tm = 100
        self.dx = self.L / self.nx
        self.dy = self.L / self.ny
        self.dt = self.tm / self.m



        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.tSlider)
        self.layout.addWidget(self.button)

        # self.update_parabola()

    # def writeFile(self, t=[[[]]]):
    #     file = open('data.txt', 'w')
    #     # file.write(str(t))
    #     file.close()
    #
    #     np.savetxt('data.txt', t.flatten())
    #

    #
    # def readFile(self):
    #     file = open('data.txt', 'r')
    #     file.close()
    #
    #     t = np.loadtxt('data.txt')
    #
    #     self.t = t.reshape([self.m, self.nx, self.ny])



    def calculateData(self):

        for i in range(len(self.lmbd)):
            for j in range(len(self.lmbd[0])):
                for k in range(len(self.lmbd[0][0])):
                    self.lmbd[i][j][k] = self.lmbdzero
                    self.ro[i][j][k] = self.rozero
                    self.c[i][j][k] = self.cp

        self.tm = 100
        self.dx = self.L / self.nx
        self.dy = self.L / self.ny
        self.dt = self.tm / self.m

        ram = 25

        for k in range(self.m - 1):
            for i in range(self.nx):
                for j in range(self.ny):
                    if ((i > ram) and (i < self.nx - ram)):
                        if ((j > ram) and (j < self.ny - ram)):

                            # lmbd
                            # ro
                            # c

                            self.t[k][i][j] = 1200
                        else:
                            self.t[k][i][j] = 0
                    else:
                        self.t[k][i][j] = 0

        if (self.dt / self.dx ** 2 + self.dt / self.dy ** 2) < 0.5:

            print('condition successfully passed')

        else:
            print(np.shape(self.t))
            for k in range(self.m - 1):
                for i in range(self.nx - 1):
                    for j in range(self.ny - 1):
                        # граничные условия

                        self.t[k + 1][i][j] = self.t[k][i][j]

                        crash1 = self.dt / (self.ro[k][i][j] * self.c[k][i][j] * self.dx ** 2)
                        crash2 = self.lmbd[k][i + 1][j] * (self.t[k][i + 1][j] - self.t[k][i][j])
                        crash3 = self.lmbd[k][i][j] * (self.t[k][i][j] - self.t[k][i - 1][j])

                        self.t[k + 1][i][j] += crash1 * (crash2 - crash3)

                        crash1 = self.dt / (self.ro[k][i][j] * self.c[k][i][j] * self.dy ** 2)
                        crash2 = self.lmbd[k][i][j + 1] * (self.t[k][i][j + 1] - self.t[k][i][j])
                        crash3 = self.lmbd[k][i][j] * (self.t[k][i][j] - self.t[k][i][j - 1])

                        self.t[k + 1][i][j] += crash1 * (crash2 - crash3)

                        # ro[k + 1][i][j] = ro[k][i][j] * (1 - alpha * (t[k + 1][i][j] - y[k][i][j]))
                        # lmbd[k][i][j] = a[k][i][j] + b[k][i][i] / (t[k][i][j] + 77)
                        # pass

        # self.writeFile(self.t)


    def updateT(self):


        x = np.linspace(0, 1, self.nx)
        y = np.linspace(0, 1, self.ny)
        X, Y = np.meshgrid(x, y)
        # t = np.ones((nx, ny))


        self.figure.clear()
        self.ax1 = self.figure.add_subplot(111)


        # Нормализуем значения температуры для цветовой шкалы
        norm = plt.Normalize(vmin=0, vmax=1500)

        # Создаем график сетки точек с цветовой шкалой от синего к красному через белый ноль

        self.ax1.scatter(X, Y, c=self.t[self.tSlider.value() - 1], cmap='bwr', norm=norm, edgecolors='none')
        # self.ax1.colorbar(label='Temperature', ax=self.ax1)
        #
        self.ax1.set_xlabel('X')
        self.ax1.set_ylabel('Y')
        self.ax1.set_title('Parabola Graph')
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ParabolaGraph()
    window.show()
    sys.exit(app.exec_())
