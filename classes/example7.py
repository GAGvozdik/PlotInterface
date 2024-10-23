from .interface import PlotInterface
import numpy as np
import pandas as pd
import time

class Example7(PlotInterface):
    def __init__(self):
        super().__init__()

        self.tab7 = self.createTab('Ex7')

        self.slider7 = self.createSlider(1, 50, init=1, 
            func=self.updateWindowSize, 
            name='Window size', 
            tab=self.tab7, 
            label=True
        )
        self.addToBox(self.tabAtr('Ex7SliderBox'), self.slider7)

        self.qdial7 = self.createQDial(1, 50, init=1, 
            func=self.updateWindowSize, 
            name='Window size', 
            tab=self.tab7, 
            label=True
        )
        self.addToBox(self.tabAtr('Ex7SliderBox'), self.qdial7)

        data = pd.read_csv("data/walker_exhaustive.dat")

        self.V = data["V"].values.reshape((300, 260))
        self.winsize = 10

        self.last_method_time = 0

        self.Vma = []
        self.Vms = []

        for i in range(51):
            Vma, Vms = self.moving(self.V, i + 1)
            self.Vma.append(Vma)
            self.Vms.append(Vms)

        self.redrawEx7()

    def update_histogram(self, data):

        if hasattr(self, 'hist7'):
            for patch in self.hist7[2]:
                patch.remove()

        binsWidth = 1
        if self.winsize < 7:
            binsWidth = 80 / int(data.size / 25)

        self.hist7 = self.ax73.hist(
            data, 
            bins=int(data.size / 25), 
            color='Crimson', 
            zorder=2, 
            edgecolor="black", 
            linewidth=binsWidth
        )
        


    def redrawEx7(self):
        self.tabAtr('Ex7Figure').clf()

        self.ax71 = self.createAxes(self.tabAtr('Ex7Figure'),
            args={
                'pos': 221, 
                'name': "Moving average",
                'xAxName': '$x$ [m]', 
                'yAxName': '',
                'grid': False
            }
        )

        self.ax72 = self.createAxes(self.tabAtr('Ex7Figure'),
            args={
                'pos': 222, 
                'name': "Standard deviation",
                'xAxName': '$x$ [m]', 
                'yAxName': '',
                'grid': False
            }
        )

        self.ax73 = self.createAxes(self.tabAtr('Ex7Figure'),
            args={
                'pos': 224, 
                'name': "",
                'xAxName': '', 
                'yAxName': '',
                'grid': False
            }
        )
        self.ax73.set_ylim(0, 150)

        self.ax73.set_position([0.22, 0.1, 0.2, 0.35]) 

        self.im_ma = self.ax71.imshow(self.Vma[self.winsize], origin="lower", cmap="terrain")
        self.im_ms = self.ax72.imshow(self.Vms[self.winsize], origin="lower", cmap="magma")

        self.update_histogram(np.ravel(self.Vma[self.winsize]))

        self.createColorbar(
            self.tabAtr('Ex7Figure'), 
            self.im_ma, 
            name='V', 
            cmap='terrain'
        )

        self.createColorbar(
            self.tabAtr('Ex7Figure'), 
            self.im_ms, 
            name='V', 
            cmap='magma'
        )

    @PlotInterface.canvasDraw(tab='Ex7')
    def updateWindowSize(self, index):
        self.winsize = index

        self.tabAtr('Window size Slider Label').setText(str(index))
        self.tabAtr('Window size QDial Label').setText(str(index))

        self.redrawEx7()



    def moving(self, data, size):

        start_time = time.time() 

        Ni, Nj = data.shape
        Nii = int(Ni / size)
        Njj = int(Nj / size)

        # Обрезка массива
        Ni_new = Nii * size
        Nj_new = Njj * size
        data_trimmed = data[:Ni_new, :Nj_new] 

        # Переформатирование и вычисление среднего и стандартного отклонения
        data_reshaped = data_trimmed.reshape(Nii, size, Njj, size)
        mea = np.mean(data_reshaped, axis=(1, 3)) 
        std = np.std(data_reshaped, axis=(1, 3)) 

        end_time = time.time()
        method_time = end_time - start_time

        if method_time > self.last_method_time:
            print(f"Время работы метода moving: {method_time:.4f} секунд")
            self.last_method_time = method_time

        return mea, std