from .interface import PlotInterface
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from pathlib import Path

# INTERFACE 5
class Example5(PlotInterface):
    def __init__(self):
        super().__init__()

        self.tab05 = self.createTab('Ex05')

        axArgs = { 
            'name': 'V [ppm]',
            'xAxName': '$x$ [m]', 
            'yAxName': '$y$ [m]',
            'grid': True
        }

        axArgs['pos'] = 121
        ax05_1 = self.createAxes(self.tabAtr('Ex05Figure'), args=axArgs)
        ax05_1.set_aspect(1)

        axArgs['pos'] = 122
        ax05_2 = self.createAxes(self.tabAtr('Ex05Figure'), args=axArgs)

        current_dir = Path(__file__).parent.resolve()
        data_dir = current_dir.parent.parent / "PlotInterface" / "data" / "data.csv"
        file = open(data_dir, 'r')

        x, y, V, U = np.loadtxt(file, unpack=True)
        cmap = LinearSegmentedColormap.from_list("white_to_Crimson", ["white", "Crimson"])

        scatterArgs05 = {
            'x': x,
            'y': y,
            'c': V,
            's': 150,
            'cmap': cmap,
            'zorder': 2
        }

        scatterPoints05 = ax05_1.scatter(**scatterArgs05)

        self.createColorbar(
            self.tabAtr('Ex05Figure'), 
            scatterPoints05, 
            name='V', 
            cmap=scatterArgs05['cmap']
        )

        pict = ax05_2.imshow(V.reshape(10, 10), cmap=cmap, zorder=3)

        self.createColorbar(
            self.tabAtr('Ex05Figure'), 
            pict, 
            name='V', 
            cmap=scatterArgs05['cmap']
        )
