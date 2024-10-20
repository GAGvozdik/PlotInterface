from .interface import PlotInterface
from PyQt5.QtWidgets import QApplication
import numpy as np
import sys
from matplotlib.colors import ListedColormap

class Example4(PlotInterface):
    def __init__(self):
        super().__init__()

        self.tab4 = self.createTab('Ex4')
        self.slider41 = self.createSlider(0, 100, 1, func=self.updateQTop, name='quantile top', tab=self.tab4)
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
        self.qEx4 = np.quantile(self.VEx4, 0.9)

        self.scatterArgsEx4 = {
            'x': self.xEx4,
            'y': self.yEx4,
            'c': np.where(self.VEx4>self.qEx4, 1, 0),
            's': 80,
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

if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("styles/darkTheme.qss", "r") as f:
        style = f.read()
        app.setStyleSheet(style)

    window = Example4()
    window.show()
    sys.exit(app.exec_())
