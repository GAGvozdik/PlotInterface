from .interface import PlotInterface
import numpy as np
import geone as gn
import matplotlib.pyplot as plt
from pathlib import Path

# INTERFACE 12
class Example12(PlotInterface):
    def __init__(self):
        super().__init__()

        self.tab12 = self.createTab('Ex12')

        self.drawAxes12()

        current_dir = Path(__file__).parent.resolve()
        data_dir = current_dir.parent.parent / "PlotInterface" / "data"
        self.drawVariogram12(data_dir / 'data1.txt', self.ax12_1)
        self.drawVariogram12(data_dir / 'data2.txt', self.ax12_2)
        self.drawVariogram12(data_dir / 'data3.txt', self.ax12_3)
        self.drawVariogram12(data_dir / 'data4.txt', self.ax12_4)

    def drawVariogram12(self, way, ax):
        plt.sca(ax)
        file = open(way, 'r')
        x, y, v = np.loadtxt(file, unpack=True)
        xy_data = np.array((x, y)).T
        hexp_raw, gexp_raw, cexp_raw = gn.covModel.variogramExp1D(xy_data, v, ncla=30, make_plot=False, hmax=70)
        ax.plot(hexp_raw, gexp_raw)

    def drawAxes12(self):

        axArgs = {
            'grid': True
        }

        axArgs['pos'], axArgs['name'] = 221, 'data 1'
        self.ax12_1 = self.createAxes(self.tabAtr('Ex12Figure'), args=axArgs)
        self.ax12_1.set_ylim((0.0, 1.3))

        axArgs['pos'], axArgs['name'] = 222, 'data 2'
        self.ax12_2 = self.createAxes(self.tabAtr('Ex12Figure'), args=axArgs)
        self.ax12_2.set_ylim((0.0, 1.3))

        axArgs['pos'], axArgs['name'] = 223, 'data 3'
        self.ax12_3 = self.createAxes(self.tabAtr('Ex12Figure'), args=axArgs)
        self.ax12_3.set_ylim((0.0, 1.3))

        axArgs['pos'], axArgs['name'] = 224, 'data 4'
        self.ax12_4 = self.createAxes(self.tabAtr('Ex12Figure'), args=axArgs)
        self.ax12_4.set_ylim((0.0, 1.3))
