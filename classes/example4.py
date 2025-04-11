from .interface import PlotInterface
import numpy as np
from matplotlib.colors import ListedColormap
from pathlib import Path

class Example4(PlotInterface):
    def __init__(self):
        super().__init__()

        self.tab04 = self.createTab('Ex04')

        self.slider41 = self.createSlider(
            0, 
            100, 
            init=0, 
            func=self.updateQTop04, 
            name='Quantile top', 
            tab=self.tab04, 
            label=True
        )

        self.ax04 = self.createAxes(
            self.tabAtr('Ex04Figure'),
            args={
                'pos': 111, 
                'name': 'V [ppm]',
                'xAxName': '$x$ [m]', 
                'yAxName': '$y$ [m]',
                'grid': True
            }
        )

        current_dir = Path(__file__).parent.resolve()
        data_dir = current_dir.parent.parent / "PlotInterface" / "data" / "data.csv"

        x, y, self.V04, U = np.loadtxt(data_dir, unpack=True)
        self.q04 = np.quantile(self.V04, 1)

        self.scatterArgsEx04 = {
            'x': x,
            'y': y,
            'c': np.where(self.V04 > self.q04, 1, 0),
            's': 140,
            'cmap': ListedColormap(["Crimson", "orange"]),
            'zorder': 2
        }
        self.scatterPointsEx04 = self.ax04.scatter(**self.scatterArgsEx04)

        self.createColorbar(
            self.tabAtr('Ex04Figure'), 
            self.scatterPointsEx04, 
            name='Quantiles', 
            cmap=self.scatterArgsEx04['cmap']
        )

    @PlotInterface.canvasDraw(tab='Ex04')
    def updateQTop04(self, index):

        self.scatterPointsEx04.remove()

        self.q04 = np.quantile(self.V04, index / 100)
        
        self.scatterArgsEx04['c'] = np.where(self.V04 > self.q04, 1, 0)
        self.scatterPointsEx04 = self.ax04.scatter(**self.scatterArgsEx04)

        q = str(round((index / 100), 2))
        if len(q) == 3:
            q += '0'
        self.tabAtr('Quantile top Slider Label').setText(q)