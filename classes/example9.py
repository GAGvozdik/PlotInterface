import numpy as np
import pandas as pd
import geone as gn
from .interface import PlotInterface
import matplotlib.pyplot as plt
from pathlib import Path

class Example9(PlotInterface):
    def __init__(self):
        super().__init__()

        self.tab09 = self.createTab('Ex09')

        self.slider091 = self.createSlider(0, 40, 
            init=10, 
            func=self.updateRmax09, 
            name='R max', 
            tab=self.tab09, 
            label=True
        )

        self.slider092 = self.createSlider(0, 30, 
            init=10, 
            func=self.updatePhincla09, 
            name='Phi ncla', 
            tab=self.tab09, 
            label=True
        )

        self.slider093 = self.createSlider(0, 60, 
            init=10, 
            func=self.updateRncla09, 
            name='R ncla', 
            tab=self.tab09, 
            label=True
        )
        
        current_dir = Path(__file__).parent.resolve()
        data_dir = current_dir.parent.parent / "PlotInterface" / "data" / "walker_exhaustive.dat"
        data = pd.read_csv(data_dir)

        idx = np.arange(len(data))
        np.random.shuffle(idx)
        mask = idx[:2000]

        self.x09 = np.array((data["X"][mask], data["V"][mask])).T 
        self.v09 = data["V"][mask].values 

        self.ax09 = self.createPolarAxes(self.tabAtr('Ex09Figure'), 111)

        self.redrawRose()

            
    @PlotInterface.canvasDraw(tab='Ex09')
    def redrawRose(self, r_max=10, phi_ncla=10, r_ncla=10):

        self.tabAtr('Ex09Figure').clf()
        
        if r_max == 10:
            r_max = self.tabAtr('R max slider').value()
        if phi_ncla == 10:
            phi_ncla = self.tabAtr('Phi ncla slider').value()
        if r_ncla == 10:
            r_ncla = self.tabAtr('R ncla slider').value()

        self.ax09 = self.createPolarAxes(self.tabAtr('Ex09Figure'), 111)

        plt.sca(self.ax09)
        
        self.rose09 = gn.covModel.variogramExp2D_rose(
            self.x09, 
            self.v09, 
            set_polar_subplot=False, 
            r_max=r_max, 
            r_ncla=r_ncla, 
            phi_ncla=phi_ncla,
            cmap="viridis",
            
        )

    def updateRmax09(self, index):
        self.redrawRose(r_max=index)
        self.tabAtr('R max Slider Label').setText(str(index))

    def updatePhincla09(self, phi_ncla):
        self.redrawRose(phi_ncla=phi_ncla)
        self.tabAtr('Phi ncla Slider Label').setText(str(phi_ncla))

    def updateRncla09(self, r_ncla):
        self.redrawRose(r_ncla=r_ncla)
        self.tabAtr('R ncla Slider Label').setText(str(r_ncla))


