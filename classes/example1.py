from .interface import PlotInterface
import numpy as np
from pathlib import Path

# INTERFACE 1
class Example1(PlotInterface):
    def __init__(self):
        super().__init__()

        self.tab01 = self.createTab('Ex01')

        self.slider01 = self.createSlider(0, 500, 
            func=self.updatePoint01, 
            name='Parameter 1', 
            tab=self.tab01
        )

        self.qdial01 = self.createQDial(1, 99, 1, 
            func=self.updateScatter01, 
            name='Parameter 2', 
            tab=self.tab01
        )

        ax01_1 = self.createAxes(
            self.tabAtr('Ex01Figure'),
            args={
                'pos': 111, 
                'name': 'plot 1',
                'xAxName': 'x', 
                'yAxName': 'y',
                'grid': True
            }
        )

        x = np.linspace(-np.pi, np.pi, 100)
        y = np.sin(x)
        
        ax01_1.plot(x, y, color='grey', linewidth=4, zorder=3)

        self.pointRam01 = ax01_1.scatter(0, 0, color='#bfbfbf', s=260, zorder=6)
        self.point01 = ax01_1.scatter(0, 0, color='Crimson', s=160, zorder=7)

        x = np.linspace(-np.pi, np.pi, 10)
        y = np.sin(x)

        self.linePointsRam01 = ax01_1.scatter(x, y, color='#bfbfbf', s=80, zorder=4)
        self.linePoints01 = ax01_1.scatter(x, y, color='ForestGreen', s=40, zorder=5)

    @PlotInterface.canvasDraw(tab='Ex01')
    def updatePoint01(self, index):
        x = index * 2 * np.pi / 499 - np.pi
        self.pointRam01.set_offsets([x, np.sin(x)])
        self.point01.set_offsets([x, np.sin(x)])

    @PlotInterface.canvasDraw(tab='Ex01')
    def updateScatter01(self, index):
        x = np.linspace(-np.pi, np.pi, index)
        y = np.sin(x)
        self.linePoints01.set_offsets(np.c_[x, y])
        self.linePointsRam01.set_offsets(np.c_[x, y])

