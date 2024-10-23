from .interface import PlotInterface
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# INTERFACE 5
class Example5(PlotInterface):
    def __init__(self):
        super().__init__()

        self.tab5 = self.createTab('Ex5')

        self.ax51 = self.createAxes(self.tabAtr('Ex5Figure'),
            args={
                'pos': 121, 
                'name': 'V [ppm]',
                'xAxName': '$x$ [m]', 
                'yAxName': '$y$ [m]',
                'grid': True
            }
        )
        self.ax51.set_aspect(1)

        self.ax52 = self.createAxes(self.tabAtr('Ex5Figure'),
            args={
                'pos': 122, 
                'name': 'V [ppm]',
                'xAxName': '$x$ [m]', 
                'yAxName': '$y$ [m]',
                'grid': False
            }
        )
        

        file = open('data/data.csv', 'r')

        x, y, V, U = np.loadtxt(file, unpack=True)
        cmap = LinearSegmentedColormap.from_list("white_to_Crimson", ["white", "Crimson"])

        self.scatterArgs5 = {
            'x': x,
            'y': y,
            'c': V,
            's': 150,
            'cmap': cmap,
            'zorder': 2
        }

        self.scatterPoints5 = self.plotScatter(self.ax51, self.scatterArgs5)

        self.createColorbar(
            self.tabAtr('Ex5Figure'), 
            self.scatterPoints5, 
            name='V', 
            cmap=self.scatterArgs5['cmap']
        )

        self.pict = self.ax52.imshow(V.reshape(10, 10), cmap=cmap)

        self.createColorbar(
            self.tabAtr('Ex5Figure'), 
            self.pict, 
            name='V', 
            cmap=self.scatterArgs5['cmap']
        )

