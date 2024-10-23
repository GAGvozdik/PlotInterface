import numpy as np
import pandas as pd
import geone as gn
from .interface import PlotInterface

class Example9(PlotInterface):
    def __init__(self):
        super().__init__()

        self.tab9 = self.createTab('Ex9')

        self.slider91 = self.createSlider(0, 40, init=10, func=self.updateRmax, name='R max', tab=self.tab9, label=True)
        self.addToBox(self.tabAtr('Ex9SliderBox'), self.slider91)
        self.slider92 = self.createSlider(0, 30, init=10, func=self.updatePhincla, name='Phi ncla', tab=self.tab9, label=True)
        self.addToBox(self.tabAtr('Ex9SliderBox'), self.slider92)
        self.slider93 = self.createSlider(0, 60, init=10, func=self.updateRncla, name='R ncla', tab=self.tab9, label=True)
        self.addToBox(self.tabAtr('Ex9SliderBox'), self.slider93)

        data_file = "data/walker_exhaustive.dat"
        data = pd.read_csv(data_file)

        data_size = len(data)
        idx = np.arange(data_size)
        max_size = 2000
        np.random.shuffle(idx)
        mask = idx[:max_size]

        self.x9 = np.array((data["X"][mask], data["V"][mask])).T 
        self.v9 = data["V"][mask].values 

        self.ax9 = self.createPolarAxes(self.tabAtr('Ex9Figure'), 111)

        self.rose = gn.covModel.variogramExp2D_rose(
            self.x9,
            self.v9,
            set_polar_subplot=False,
            r_max=10,
            r_ncla=10, 
            phi_ncla=10,
            cmap="viridis"
        )

        # fig = self.tabAtr('RoseFigure')
        # colorbar = plt.colorbar() 
        # tick_labels = colorbar.ax.get_yticklabels()
        # for label in tick_labels:
        #     label.set_color('white')
            
    @PlotInterface.canvasDraw(tab='Ex9')
    def redrawRose(self, r_max=10, phi_ncla=10, r_ncla=10):

        self.tabAtr('Ex9Figure').clf()

        if r_max == 10:
            r_max = self.tabAtr('R max slider').value()
        if phi_ncla == 10:
            phi_ncla = self.tabAtr('Phi ncla slider').value()
        if r_ncla == 10:
            r_ncla = self.tabAtr('R ncla slider').value()

        self.ax9 = self.createPolarAxes(self.tabAtr('Ex9Figure'), 111)

        self.rose = gn.covModel.variogramExp2D_rose(
            self.x9, 
            self.v9, 
            set_polar_subplot=False, 
            r_max=r_max, 
            r_ncla=r_ncla, 
            phi_ncla=phi_ncla,
            cmap="viridis",
        )

        #TODO rename vars v9 x9
        #TODO colorbar
        #TODO set ax limit

    def updateRmax(self, index):
        self.redrawRose(r_max=index)
        self.tabAtr('R max Slider Label').setText(str(index))

    def updatePhincla(self, phi_ncla):
        self.redrawRose(phi_ncla=phi_ncla)
        self.tabAtr('Phi ncla Slider Label').setText(str(phi_ncla))

    def updateRncla(self, r_ncla):
        self.redrawRose(r_ncla=r_ncla)
        self.tabAtr('R ncla Slider Label').setText(str(r_ncla))

