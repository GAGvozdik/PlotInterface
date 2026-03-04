import sys
from pathlib import Path
import wget
import re
import time
import py2exe

from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QCheckBox

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QSlider
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QObject

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import threading
import sys


# git log
# e23c2c59638bfc266e6c9f2efe17e94997649213
# git checkout -b имя-новой-ветки aaaaaa
#
# или git stash save --keep-index ???????????????

# TODO вылет после конца расчета
# TODO сделай один файл
# TODO 4 графика

class ParabolaGraph(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('2d heat flow')
        self.setGeometry(200, 200, 2000, 1100)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # parameters

        self.tliq2 = 1050 + 273
        self.tsol2 = 950 + 273
        self.lcr2 = 300000
        self.tliq1 = 1150 + 273
        self.tsol1 = 1050 + 273
        self.lcr1 = 380000





        # parameters
        self.maxT = 2000
        self.minT = -2000

        self.maxC = 3000
        self.minC = -3000

        self.maxRo = 3500
        self.minRo = 2500

        self.maxLmbd = 3
        self.minLmbd = 0

        self.nx = 100
        self.ny = 100
        self.ram = 25
        self.m = 1000
        self.L = 1000

        self.tm = 60 * 60 * 24 * 30 * 12 * 200
        self.dx = self.L / self.nx
        self.dy = self.L / self.ny
        self.dt = self.tm / self.m

        self.a = np.zeros([self.nx, self.ny])
        self.b = np.zeros([self.nx, self.ny])
        self.d = np.zeros([self.nx, self.ny])
        self.e = np.zeros([self.nx, self.ny])
        self.f = np.zeros([self.nx, self.ny])
        self.g = np.zeros([self.nx, self.ny])
        self.h = np.zeros([self.nx, self.ny])

        self.c = np.zeros([self.m, self.nx, self.ny])
        self.t = np.zeros([self.m, self.nx, self.ny])
        self.ro = np.zeros([self.m, self.nx, self.ny])
        self.lmbd = np.zeros([self.m, self.nx, self.ny])

        # делить или умножить для си?
        self.alpha = 3 * 10 ** (-5)
        self.ro1 = 3.0 * 1000
        self.ro2 = 2.7 * 1000
        self.t1 = 1300 + 273
        self.t2 = 0 + 273

        self.a1 = 1.18
        self.b1 = 474
        self.e1 = -1.21 * 10 ** 9
        self.f1 = 1.23 * 10 ** 11
        self.g1 = -290790
        self.h1 = 6447400
        self.d1 = 4896.7

        self.a2 = 0.64
        self.b2 = 807
        self.e2 = 3.38 * 10 ** 8
        self.f2 = -3.47 * 10 ** 10
        self.g2 = 110880
        self.h2 = -2378100
        self.d2 = -228.24

        self.a = self.setSquare(self.a, self.a1, self.a2)
        self.b = self.setSquare(self.b, self.b1, self.b2)
        self.e = self.setSquare(self.e, self.e1, self.e2)
        self.f = self.setSquare(self.f, self.f1, self.f2)
        self.g = self.setSquare(self.g, self.g1, self.g2)
        self.h = self.setSquare(self.h, self.h1, self.h2)
        self.d = self.setSquare(self.d, self.d1, self.d2)

        self.debug = 0

        # interface
        self.tSlider = QSlider(Qt.Horizontal)
        self.tSlider.setMinimum(1)
        self.tSlider.setMaximum(self.m - 1)
        self.tSlider.setValue(1)
        self.tSlider.setTickInterval(10)
        self.tSlider.setTickPosition(QSlider.TicksBelow)
        self.tSlider.valueChanged.connect(self.updateGraph)

        self.button = QPushButton('Calculate data')
        self.button.clicked.connect(self.calculateDataThread)
        # self.button.clicked.connect(self.calculateData)

        self.readButton = QPushButton('Read data')
        self.readButton.clicked.connect(self.readFile)

        self.writeButton = QPushButton('Write data')
        self.writeButton.clicked.connect(self.writeFile)

        self.figure = Figure()
        # self.figure, ((self.ax1, self.ax2, self.ax3, self.ax4), (self.ax5, self.ax6, self.ax7, self.ax8)) = plt.subplots(2, 4, figsize=(15, 15))
        self.canvas = FigureCanvas(self.figure)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.hide()

        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.tSlider)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.readButton)
        self.layout.addWidget(self.writeButton)

    def hideInterface(self):
        self.tSlider.hide()
        self.readButton.hide()
        self.writeButton.hide()
        self.button.hide()

    def showInterface(self):
        self.tSlider.show()
        self.readButton.show()
        self.writeButton.show()
        self.button.show()

    def calculateDataThread(self):
        calculateThread = threading.Thread(target=self.calculateData)
        calculateThread.start()


    def calculateData(self):

        try:

            start_time = time.time()

            self.hideInterface()

            self.progress_bar.show()
            self.progress_bar.setValue(0)

            self.ro = self.setMultSquare(self.ro, self.roCalc(self.ro1, self.t1, 270),
                                         self.roCalc(self.ro2, self.t2, 270))

            self.lmbd = self.setMultSquare(
                self.lmbd,
                self.lmbdCalc(self.a1, self.b1, self.t1),
                self.lmbdCalc(self.a2, self.b2, self.t2)
            )

            self.c = self.setMultSquare(
                self.c,
                self.cCalc(self.d1, self.e1, self.f1, self.g1, self.h1, self.t1),
                self.cCalc(self.d2, self.e2, self.f2, self.g2, self.h2, self.t2)
            )

            self.c[0] = self.addMelting(
                self.c[0],
                self.t1,
                self.t2,
                self.tsol1,
                self.tsol2,
                self.tliq1,
                self.tliq2,
                self.lcr1,
                self.lcr2
            )

            self.t = self.setMultSquare(
                self.t,
                self.t1,
                self.t2
            )

            if (self.dt / self.dx ** 2 + self.dt / self.dy ** 2) < 0.5:
                print('condition successfully passed')
            else:
                for k in range(self.m - 1):

                    valueInPercents = int(100 * (k / (self.m - 1)))

                    self.progress_bar.setValue(valueInPercents)

                    for i in range(self.nx - 1):
                        for j in range(self.ny - 1):
                            self.t[k + 1][i][j] = self.t[k][i][j]

                            crash1 = self.dt / (self.ro[k][i][j] * self.c[k][i][j] * self.dx ** 2)
                            crash2 = self.lmbd[k][i + 1][j] * (self.t[k][i + 1][j] - self.t[k][i][j])
                            crash3 = self.lmbd[k][i][j] * (self.t[k][i][j] - self.t[k][i - 1][j])

                            self.t[k + 1][i][j] += crash1 * (crash2 - crash3)

                            crash1 = self.dt / (self.ro[k][i][j] * self.c[k][i][j] * self.dy ** 2)
                            crash2 = self.lmbd[k][i][j + 1] * (self.t[k][i][j + 1] - self.t[k][i][j])
                            crash3 = self.lmbd[k][i][j] * (self.t[k][i][j] - self.t[k][i][j - 1])

                            self.t[k + 1][i][j] += crash1 * (crash2 - crash3)

                            self.ro[k + 1][i][j] = self.roCalc(
                                self.ro[k][i][j],
                                self.t[k + 1][i][j],
                                self.t[k][i][j]
                            )

                            self.lmbd[k + 1][i][j] = self.lmbdCalc(
                                self.a[i][j],
                                self.b[i][j],
                                self.t[k + 1][i][j]
                            )

                            self.c[k + 1][i][j] = self.cCalc(
                                self.d[i][j],
                                self.e[i][j],
                                self.f[i][j],
                                self.g[i][j],
                                self.h[i][j],
                                self.t[k][i][j]
                            )

                            if ((i > self.ram) and (i < self.nx - self.ram)):
                                if ((j > self.ram) and (j < self.ny - self.ram)):

                                    self.c[k][i][j] = self.c[k][i][j] + self.lcr2 * self.meltingDegree(self.t[k][i][j], self.tsol2, self.tliq2)
                                else:
                                    self.c[k][i][j] = self.c[k][i][j] + self.lcr1 * self.meltingDegree(self.t[k][i][j], self.tsol1, self.tliq1)
                            else:
                                self.c[k][i][j] = self.c[k][i][j] + self.lcr1 * self.meltingDegree(self.t[k][i][j], self.tsol1, self.tliq1)

                            # if ((i > self.ram) and (i < self.nx - self.ram)):
                            #     if ((j > self.ram) and (j < self.ny - self.ram)):
                            #         self.c[k][i][j] = self.c[k][i][j] + self.lcr1 * self.meltingDegree(self.t[k][i][j], self.tsol1, self.tliq1)
                            #     else:
                            #         self.c[k][i][j] = self.c[k][i][j] + self.lcr2 * self.meltingDegree(self.t[k][i][j], self.tsol2, self.tliq2)
                            # else:
                            #     self.c[k][i][j] = self.c[k][i][j] + self.lcr2 * self.meltingDegree(self.t[k][i][j], self.tsol2, self.tliq2)



                    # self.updateGraph2(k)


            self.progress_bar.setValue(100)
            self.progress_bar.hide()

            self.showInterface()
            self.tSlider.setValue(1)

            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Время выполнения расчета: {elapsed_time} секунд")

        except:
            print('oops')

    def writeFileThread(self):
        writeThread = threading.Thread(target=self.writeFile)
        writeThread.start()

    def writeFile(self):

        start_time = time.time()

        self.hideInterface()
        self.progress_bar.show()
        self.progress_bar.setValue(0)

        np.savetxt('t.txt', self.t.flatten())
        self.progress_bar.setValue(25)

        np.savetxt('c.txt', self.c.flatten())
        self.progress_bar.setValue(50)

        np.savetxt('ro.txt', self.ro.flatten())
        self.progress_bar.setValue(75)

        np.savetxt('lmbd.txt', self.lmbd.flatten())
        self.progress_bar.setValue(100)

        self.progress_bar.hide()
        self.showInterface()
        self.tSlider.setValue(1)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Время выполнения записи: {elapsed_time} секунд")

    def readFileThread(self):

        readThread = threading.Thread(target=self.readFile)
        readThread.start()

    def readFile(self):
        start_time = time.time()

        self.hideInterface()

        self.progress_bar.show()
        self.progress_bar.setValue(0)

        t = np.loadtxt('t.txt')
        self.t = t.reshape([self.m, self.nx, self.ny])

        self.progress_bar.setValue(25)
        ro = np.loadtxt('ro.txt')
        self.ro = ro.reshape([self.m, self.nx, self.ny])

        self.progress_bar.setValue(50)
        lmbd = np.loadtxt('lmbd.txt')
        self.lmbd = lmbd.reshape([self.m, self.nx, self.ny])

        self.progress_bar.setValue(75)
        c = np.loadtxt('c.txt')
        self.c = c.reshape([self.m, self.nx, self.ny])

        self.progress_bar.setValue(100)

        self.progress_bar.hide()

        self.showInterface()

        self.tSlider.setValue(1)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Время выполнения считывания: {elapsed_time} секунд")

    # Calculation functions
    def setSquare(self, p, value1, value2):
        param = p
        for i in range(self.nx):
            for j in range(self.ny):
                if ((i > self.ram) and (i < self.nx - self.ram)):
                    if ((j > self.ram) and (j < self.ny - self.ram)):
                        param[i][j] = value1
                    else:
                        param[i][j] = value2
                else:
                    param[i][j] = value2
        return param


    def meltingDegree(self, t, tsol, tliq):
        try:
            if t < tsol:
                return 0
            elif t <= tliq and t >= tsol:
                return 1 / (tliq - tsol)
            elif t > tliq:
                return 0
        except:
            print('error meltingDegree')
            return 0

    def addMelting(self, p, t1, t2, tsol1, tsol2, tliq1, tliq2, lcr1, lcr2):
        try:
            param = p
            for i in range(self.nx):
                for j in range(self.ny):
                    if ((i > self.ram) and (i < self.nx - self.ram)):
                        if ((j > self.ram) and (j < self.ny - self.ram)):
                            param[i][j] += lcr1 * self.meltingDegree(t1, tsol1, tliq1)
                        else:
                            param[i][j] += lcr2 * self.meltingDegree(t2, tsol2, tliq2)
                    else:
                        param[i][j] += lcr2 * self.meltingDegree(t2, tsol2, tliq2)
            return param
        except:

            print('error addMelting')
            return p

    def setMultMelting(self, p, t1, t2, tsol1, tsol2, tliq1, tliq2, lcr1, lcr2):
        try:
            param = p
            for k in range(self.m - 1):
                param[k] = self.addMelting(
                    param[k],
                    t1,
                    t2,
                    tsol1,
                    tsol2,
                    tliq1,
                    tliq2,
                    lcr1,
                    lcr2
                )
            return param
        except:
            print('error setMultMelting')
            return p


    def setMultSquare(self, p, value1, value2):
        param = p
        for k in range(self.m - 1):
            self.setSquare(param[k], value1, value2)
        return param

    def lmbdCalc(self, a, b, t):
        lmbd = a + b / (t + 77)
        return lmbd

    def roCalc(self, ro0, t, t0):
        ro = ro0 * (1 - self.alpha * (t - t0))
        return ro

    def cCalc(self, d, e, f, g, h, t):
        c = d + e / t ** 2
        c += f / t ** 3
        c += g / t ** 0.5
        c += h / t
        return c

    # Paint functions
    def updateGraph(self):

        # self.maxT = np.max(self.t)
        # self.minT = np.min(self.t)
        #
        # self.maxC = np.max(self.c)
        # self.minC = np.min(self.c)
        #
        # self.maxRo = np.max(self.ro)
        # self.minRo = np.min(self.ro)
        #
        # self.maxLmbd = np.max(self.lmbd)
        # self.minLmbd = np.min(self.lmbd)

        self.figure.clear()
        self.ax1 = self.figure.add_subplot(241)

        self.ax1.set_title('t')
        norm1 = plt.Normalize(vmin=self.minT, vmax=self.maxT)  # Нормализация для значений температуры

        # Создание изображения с данными температуры
        im1 = self.ax1.imshow(
            self.t[self.tSlider.value() - 1],
            cmap='bwr',
            norm=norm1,
            origin='lower',
            extent=(0, self.nx - 1, 0, self.ny - 1)
        )

        # Добавление цветовой шкалы
        # plt.colorbar(im1, ax=self.ax1)

        ################################################################

        self.ax2 = self.figure.add_subplot(242)

        self.ax2.set_title('c')
        norm2 = plt.Normalize(vmin=self.minC, vmax=self.maxC)  # Нормализация для значений температуры

        # Создание изображения с данными температуры
        im2 = self.ax2.imshow(
            self.c[self.tSlider.value() - 1],
            cmap='bwr',
            norm=norm2,
            origin='lower',
            extent=(0, self.nx - 1, 0, self.ny - 1)
        )

        # Добавление цветовой шкалы
        # plt.colorbar(im2, ax=self.ax2)

        ################################################################

        self.ax3 = self.figure.add_subplot(243)

        self.ax3.set_title('ro')
        norm3 = plt.Normalize(vmin=self.minRo, vmax=self.maxRo)  # Нормализация для значений температуры

        # Создание изображения с данными температуры
        im3 = self.ax3.imshow(
            self.ro[self.tSlider.value() - 1],
            cmap='bwr',
            norm=norm3,
            origin='lower',
            extent=(0, self.nx - 1, 0, self.ny - 1)
        )

        # Добавление цветовой шкалы
        # plt.colorbar(im3, ax=self.ax3)

        ################################################################

        self.ax4 = self.figure.add_subplot(244)

        self.ax4.set_title('lmbd')
        norm4 = plt.Normalize(vmin=self.minLmbd, vmax=self.maxLmbd)  # Нормализация для значений температуры

        # Создание изображения с данными температуры
        im4 = self.ax4.imshow(
            self.lmbd[self.tSlider.value() - 1],
            cmap='bwr',
            norm=norm4,
            origin='lower',
            extent=(0, self.nx - 1, 0, self.ny - 1)
        )

        # Добавление цветовой шкалы
        # plt.colorbar(im4, ax=self.ax4)

        ################################################################

        self.ax5 = self.figure.add_subplot(245)
        self.ax5.set_title('t')

        tSlice = self.t[self.tSlider.value() - 1]
        tSlice = tSlice[int(len(tSlice) / 2)]

        self.ax5.plot(np.linspace(0, self.nx, len(tSlice)), tSlice)



        ################################################################

        self.ax6 = self.figure.add_subplot(246)
        self.ax6.set_title('c')

        tSlice = self.c[self.tSlider.value() - 1]
        tSlice = tSlice[int(len(tSlice) / 2)]

        self.ax6.plot(np.linspace(0, self.nx, len(tSlice)), tSlice)


        ################################################################

        self.ax7 = self.figure.add_subplot(247)
        self.ax7.set_title('ro')

        tSlice = self.ro[self.tSlider.value() - 1]
        tSlice = tSlice[int(len(tSlice) / 2)]

        self.ax7.plot(np.linspace(0, self.nx, len(tSlice)), tSlice)



        ################################################################

        self.ax8 = self.figure.add_subplot(248)
        self.ax8.set_title('lmbd')

        tSlice = self.lmbd[self.tSlider.value() - 1]
        tSlice = tSlice[int(len(tSlice) / 2)]

        self.ax8.plot(np.linspace(0, self.nx, len(tSlice)), tSlice)

        self.canvas.draw()

    # Paint functions
    def updateGraph2(self, k):

        # self.maxT = np.max(self.t)
        # self.minT = np.min(self.t)
        #
        # self.maxC = np.max(self.c)
        # self.minC = np.min(self.c)
        #
        # self.maxRo = np.max(self.ro)
        # self.minRo = np.min(self.ro)
        #
        # self.maxLmbd = np.max(self.lmbd)
        # self.minLmbd = np.min(self.lmbd)

        self.figure.clear()
        self.ax1 = self.figure.add_subplot(241)

        self.ax1.set_title('t')
        norm1 = plt.Normalize(vmin=self.minT, vmax=self.maxT)  # Нормализация для значений температуры

        # Создание изображения с данными температуры
        im1 = self.ax1.imshow(
            self.t[k],
            cmap='bwr',
            norm=norm1,
            origin='lower',
            extent=(0, self.nx - 1, 0, self.ny - 1)
        )

        # Добавление цветовой шкалы
        # plt.colorbar(im1, ax=self.ax1)

        ################################################################

        self.ax2 = self.figure.add_subplot(242)

        self.ax2.set_title('c')
        norm2 = plt.Normalize(vmin=self.minC, vmax=self.maxC)  # Нормализация для значений температуры

        # Создание изображения с данными температуры
        im2 = self.ax2.imshow(
            self.c[k],
            cmap='bwr',
            norm=norm2,
            origin='lower',
            extent=(0, self.nx - 1, 0, self.ny - 1)
        )

        # Добавление цветовой шкалы
        # plt.colorbar(im2, ax=self.ax2)

        ################################################################

        self.ax3 = self.figure.add_subplot(243)

        self.ax3.set_title('ro')
        norm3 = plt.Normalize(vmin=self.minRo, vmax=self.maxRo)  # Нормализация для значений температуры

        # Создание изображения с данными температуры
        im3 = self.ax3.imshow(
            self.ro[k],
            cmap='bwr',
            norm=norm3,
            origin='lower',
            extent=(0, self.nx - 1, 0, self.ny - 1)
        )

        # Добавление цветовой шкалы
        # plt.colorbar(im3, ax=self.ax3)

        ################################################################

        self.ax4 = self.figure.add_subplot(244)

        self.ax4.set_title('lmbd')
        norm4 = plt.Normalize(vmin=self.minLmbd, vmax=self.maxLmbd)  # Нормализация для значений температуры

        # Создание изображения с данными температуры
        im4 = self.ax4.imshow(
            self.lmbd[k],
            cmap='bwr',
            norm=norm4,
            origin='lower',
            extent=(0, self.nx - 1, 0, self.ny - 1)
        )

        # Добавление цветовой шкалы
        # plt.colorbar(im4, ax=self.ax4)

        ################################################################

        self.ax5 = self.figure.add_subplot(245)
        self.ax5.set_title('t')

        tSlice = self.t[k]
        tSlice = tSlice[int(len(tSlice) / 2)]

        self.ax5.plot(np.linspace(0, self.nx, len(tSlice)), tSlice)


        ################################################################

        self.ax6 = self.figure.add_subplot(246)
        self.ax6.set_title('c')

        tSlice = self.c[k]
        tSlice = tSlice[int(len(tSlice) / 2)]

        self.ax6.plot(np.linspace(0, self.nx, len(tSlice)), tSlice)



        ################################################################

        self.ax7 = self.figure.add_subplot(247)
        self.ax7.set_title('ro')

        tSlice = self.ro[k]
        tSlice = tSlice[int(len(tSlice) / 2)]

        self.ax7.plot(np.linspace(0, self.nx, len(tSlice)), tSlice)



        ################################################################

        self.ax8 = self.figure.add_subplot(248)
        self.ax8.set_title('lmbd')

        tSlice = self.lmbd[k]
        tSlice = tSlice[int(len(tSlice) / 2)]

        self.ax8.plot(np.linspace(0, self.nx, len(tSlice)), tSlice)

        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ParabolaGraph()
    window.show()
    sys.exit(app.exec_())
