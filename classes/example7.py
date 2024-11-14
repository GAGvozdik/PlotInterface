from .interface import PlotInterface
import numpy as np
import pandas as pd

class Example7(PlotInterface):
    def __init__(self):
        super().__init__()

        self.tab07 = self.createTab('Ex07')

        self.qdial07 = self.createQDial(
            1, 
            50, 
            init=1, 
            func=self.updateWindowSize07, 
            name='Window size', 
            tab=self.tab07, 
            label=True
        )

        data = pd.read_csv("data/walker_exhaustive.dat")

        self.V = data["V"].values.reshape((300, 260))
        self.winsize = 1

        self.last_method_time = 0

        self.Vma = []
        self.Vms = []

        for i in range(51):
            Vma, Vms = self.moving(self.V, i + 1)
            self.Vma.append(Vma)
            self.Vms.append(Vms)

        self.redrawEx07()

    def update_histogram(self, data):

        if hasattr(self, 'hist07'):
            for patch in self.hist07[2]:
                patch.remove()

        binsWidth = 1
        if self.winsize < 7:
            binsWidth = 80 / int(data.size / 25)

        self.hist07 = self.ax07_3.hist(
            data, 
            bins=int(data.size / 25), 
            color='Crimson', 
            zorder=2, 
            edgecolor="black", 
            linewidth=binsWidth
        )

    def redrawEx07(self):
        self.tabAtr('Ex07Figure').clf()

        self.drawAxes07()

        self.im_ma = self.ax07_1.imshow(self.Vma[self.winsize], origin="lower", cmap="terrain")
        self.im_ms = self.ax07_2.imshow(self.Vms[self.winsize], origin="lower", cmap="magma")

        self.update_histogram(np.ravel(self.Vma[self.winsize]))

        self.createColorbar(
            self.tabAtr('Ex07Figure'), 
            self.im_ma, 
            name='V', 
            cmap='terrain'
        )

        self.createColorbar(
            self.tabAtr('Ex07Figure'), 
            self.im_ms, 
            name='V', 
            cmap='magma'
        )

    @PlotInterface.canvasDraw(tab='Ex07')
    def updateWindowSize07(self, index):
        self.winsize = index
        self.tabAtr('Window size QDial Label').setText(str(index))
        self.redrawEx07()


    @PlotInterface.getWorkTime('moving')
    def moving(self, data, size):

        Ni, Nj = data.shape
        Nii = int(Ni / size)
        Njj = int(Nj / size)

        Ni_new = Nii * size
        Nj_new = Njj * size
        data_trimmed = data[:Ni_new, :Nj_new] 

        data_reshaped = data_trimmed.reshape(Nii, size, Njj, size)
        mea = np.mean(data_reshaped, axis=(1, 3)) 
        std = np.std(data_reshaped, axis=(1, 3)) 

        return mea, std
    
    def drawAxes07(self):

        axArgs = {
            'xAxName': '$x$ [m]', 
            'yAxName': '',
        }

        axArgs['pos'], axArgs['name'] = 221, "Moving average"
        self.ax07_1 = self.createAxes(self.tabAtr('Ex07Figure'), args=axArgs)
        self.ax07_1.set_position([0.05, 0.55, 0.4, 0.4])

        axArgs['pos'], axArgs['name'] = 222, "Standard deviation"
        self.ax07_2 = self.createAxes(self.tabAtr('Ex07Figure'), args=axArgs)
        self.ax07_2.set_position([0.55, 0.55, 0.4, 0.4]) 

        axArgs['pos'], axArgs['name'], axArgs['grid'] = 223, "Hist", True
        self.ax07_3 = self.createAxes(self.tabAtr('Ex07Figure'), args=axArgs)
        self.ax07_3.set_ylim(0, 150)
        self.ax07_3.set_xlim(-50, 1300)
        self.ax07_3.set_position([0.36, 0.06, 0.35, 0.4]) 




