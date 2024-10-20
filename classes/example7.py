from .interface import PlotInterface
from PyQt5.QtWidgets import QApplication
import numpy as np
import sys
import pandas as pd

class Example7(PlotInterface):
    def __init__(self):
        super().__init__()

        self.tab7 = self.createTab('Ex7')

        self.slider7 = self.createSlider(1, 100, 1, func=self.updateWindowSize, name='Window size', tab=self.tab7)
        self.addToBox(self.tabAtr('Ex7SliderBox'), self.slider7)

        self.ax71 = self.createAxes(self.tabAtr('Ex7Figure'),
            args={
                'pos': 121, 
                'name': "Moving average",
                'xAxName': '$x$ [m]', 
                'yAxName': '',
                'grid': False
            }
        )

        self.ax72 = self.createAxes(self.tabAtr('Ex7Figure'),
            args={
                'pos': 122, 
                'name': "Standard deviation",
                'xAxName': '$x$ [m]', 
                'yAxName': '',
                'grid': False
            }
        )

        data_file = "data/walker_exhaustive.dat"
        data = pd.read_csv(data_file)

        self.V = data["V"].values.reshape((300, 260))

        self.winsize = 10
        Vma, Vms = self.moving(self.V, self.winsize)

        self.im_ma = self.ax71.imshow(Vma, origin="lower", cmap="terrain")
        self.im_ms = self.ax72.imshow(Vms, origin="lower", cmap="magma")

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

    def moving(self, data, size):

        Ni, Nj = data.shape

        Nii = int(Ni/size)
        Njj = int(Nj/size)

        mea = np.zeros((Nii, Njj))
        std = np.zeros((Nii, Njj))

        for i in range(Nii):
            for j in range(Njj):
                win = data[i*size:(i+1)*size,j*size:(j+1)*size]
                mea[i,j] = np.mean(win)
                std[i,j] = np.std(win)
        return mea, std    

    @PlotInterface.canvasDraw(tab='Ex7')
    def updateWindowSize(self, index):
        
        self.tabAtr('Ex7Figure').clf()

        self.ax71 = self.createAxes(self.tabAtr('Ex7Figure'),
            args={
                'pos': 121, 
                'name': "Moving average",
                'xAxName': '$x$ [m]', 
                'yAxName': '',
                'grid': False
            }
        )

        self.ax72 = self.createAxes(self.tabAtr('Ex7Figure'),
            args={
                'pos': 122, 
                'name': "Standard deviation",
                'xAxName': '$x$ [m]', 
                'yAxName': '',
                'grid': False
            }
        )

        self.winsize = index
        Vma, Vms = self.moving(self.V, self.winsize)

        self.im_ma = self.ax71.imshow(Vma, origin="lower", cmap="terrain")
        self.im_ms = self.ax72.imshow(Vms, origin="lower", cmap="magma")

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

if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("styles/darkTheme.qss", "r") as f:
        style = f.read()
        app.setStyleSheet(style)

    window = Example7()
    window.show()
    sys.exit(app.exec_())
