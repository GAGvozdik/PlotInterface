from .interface import PlotInterface
import numpy as np
from matplotlib.colors import ListedColormap

class Example4(PlotInterface):
    def __init__(self):
        super().__init__()

        self.tab4 = self.createTab('Ex4')
        self.slider41 = self.createSlider(0, 100, init=0, func=self.updateQTop, name='quantile top', tab=self.tab4, label=True)
        self.addToBox(self.tabAtr('Ex4SliderBox'), self.slider41)

        self.ax41 = self.createAxes(self.tabAtr('Ex4Figure'),
            args={
                'pos': 111, 
                'name': 'V [ppm]',
                'xAxName': '$x$ [m]', 
                'yAxName': '$y$ [m]',
                'grid': True
            }
        )

        data_file = "data/data.csv"
        self.xEx4, self.yEx4, self.VEx4,self.UEx4 = np.loadtxt(data_file, unpack=True)
        self.qEx4 = np.quantile(self.VEx4, 1)

        self.scatterArgsEx4 = {
            'x': self.xEx4,
            'y': self.yEx4,
            'c': np.where(self.VEx4>self.qEx4, 1, 0),
            's': 140,
            'cmap': ListedColormap(["Crimson", "orange"]),
            'zorder': 2
        }
        self.scatterPointsEx4 = self.plotScatter(self.ax41, self.scatterArgsEx4)

        self.createColorbar(
            self.tabAtr('Ex4Figure'), 
            self.scatterPointsEx4, 
            name='Quantiles', 
            cmap=self.scatterArgsEx4['cmap']
        )

    @PlotInterface.canvasDraw(tab='Ex4')
    def updateQTop(self, index):

        self.scatterPointsEx4.remove()

        self.qEx4 = np.quantile(self.VEx4, index / 100)
        
        self.scatterArgsEx4['c'] = np.where(self.VEx4>self.qEx4, 1, 0)
        self.scatterPointsEx4 = self.plotScatter(self.ax41, self.scatterArgsEx4)

        q = str(round((index / 100), 2))
        if len(q) == 3:
            q += '0'
        self.tabAtr('quantile top Slider Label').setText(q)