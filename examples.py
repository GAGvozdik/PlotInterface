from interface import PlotInterface
from PyQt5.QtWidgets import QApplication
import numpy as np
import sys
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd
# https://scikit-gstat.readthedocs.io/en/latest/install.html

# INTERFACE 1
class Example1(PlotInterface):
    def __init__(self):
        super().__init__()

        self.tab1 = self.createTab('Ex1')
        self.slider1 = self.createSlider(0, 500, 1, func=self.updatePoint, name='Parameter 1', tab=self.tab1)
        self.addToBox(self.tabAtr('Ex1SliderBox'), self.slider1)
        self.qdial1 = self.createQDial(1, 99, 1, func=self.updateScatter, name='Parameter 2', tab=self.tab1)
        self.addToBox(self.tabAtr('Ex1SliderBox'), self.qdial1)

        self.ax11 = self.createAxes(self.tabAtr('Ex1Figure'),
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
        self.line = self.ax11.plot(x, y, color='grey', linewidth=4, zorder=1)

        self.pointRam = self.ax11.scatter(0, 0, color='#bfbfbf', s=120, zorder=4)
        self.point = self.ax11.scatter(0, 0, color='Crimson', s=60, zorder=5)

        self.xS = np.linspace(-np.pi, np.pi, 10)
        self.yS = np.sin(self.xS)

        self.linePointsRam = self.ax11.scatter(self.xS, self.yS, color='#bfbfbf', s=80, zorder=2)
        self.linePoints = self.ax11.scatter(self.xS, self.yS, color='ForestGreen', s=40, zorder=3)

    @PlotInterface.canvasDraw(tab='Ex1')
    def updatePoint(self, index):
        x = index * 2 * np.pi / 499 - np.pi
        self.pointRam.set_offsets([x, np.sin(x)])
        self.point.set_offsets([x, np.sin(x)])

    @PlotInterface.canvasDraw(tab='Ex1')
    def updateScatter(self, index):
        self.xS = np.linspace(-np.pi, np.pi, index)
        self.yS = np.sin(self.xS)
        self.linePoints.set_offsets(np.c_[self.xS, self.yS])
        self.linePointsRam.set_offsets(np.c_[self.xS, self.yS])

# INTERFACE 2
class Example2(PlotInterface):
    def __init__(self):
        super().__init__()
        self.tab2 = self.createTab('Ex2')

        self.qdial2 = self.createQDial(10, 99, 40, func=self.updateBins, name='bins', tab=self.tab2)
        self.addToBox(self.tabAtr('Ex2SliderBox'), self.qdial2)

        self.ax21 = self.createAxes(self.tabAtr('Ex2Figure'),
            args={
                'pos': 111, 
                'name': 'plot 1',
                'xAxName': '', 
                'yAxName': '',
                'grid': True
            }
        )
        self.ax21.set_ylim(0, 800)

        self.histData = np.array(np.random.normal(0, 1, 10000))
        self.hist1 = self.ax21.hist(self.histData, bins=100, color='Crimson')

    @PlotInterface.canvasDraw(tab='Ex2')
    def updateBins(self, index):

        self.ax21.remove()
        self.ax21 = self.createAxes(self.tabAtr('Ex2Figure'),
            args={
                'pos': 111, 
                'name': 'plot 1',
                'xAxName': '', 
                'yAxName': '',
                'grid': True
            }
        )
        self.ax21.set_ylim(0, 800)
        self.hist1 = self.ax21.hist(self.histData, bins=index, color='Crimson')

# INTERFACE 3
class Example3(PlotInterface):
    def __init__(self):
        super().__init__()

        self.tab3 = self.createTab('Ex3')

        self.ax31 = self.createAxes(self.tabAtr('Ex3Figure'),
            args={
                'pos': 221, 
                'name': 'plot 1',
                'xAxName': 'x', 
                'yAxName': 'y',
                'grid': True
            }
        )
        
        self.ax32 = self.createAxes(self.tabAtr('Ex3Figure'),
            args={
                'pos': 222, 
                'name': 'plot 2',
                'xAxName': 'x', 
                'yAxName': 'y',
                'grid': True
            }
        )
        self.ax33 = self.createAxes(self.tabAtr('Ex3Figure'),
            args={
                'pos': 223, 
                'name': 'plot 3',
                'xAxName': 'x', 
                'yAxName': 'y',
                'grid': True
            }
        )
        self.ax34 = self.createAxes(self.tabAtr('Ex3Figure'),
            args={
                'pos': 224, 
                'name': 'plot 4',
                'xAxName': 'x', 
                'yAxName': 'y',
                'grid': True
            }
        )

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
        
        self.scatterArgsEx4['c'] = np.where(self.VEx4>self.qEx4, 1, 0),
        self.scatterPointsEx4 = self.plotScatter(self.ax41, self.scatterArgsEx4)


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


class Example6(PlotInterface):
    def __init__(self):
        super().__init__()

        self.tab6 = self.createTab('Ex6')

        self.ax6 = self.createAxes(self.tabAtr('Ex6Figure'),
            args={
                'pos': 111, 
                'name': 'EC [mS/m] 475 Hz, line 10',
                'xAxName': '$x$ [m]', 
                'yAxName': '',
                'grid': False
            }
        )

        file_in = "data/line10.csv"
        win = 15
        data = pd.read_csv(file_in)
        EC = data["EC475Hz[mS/m]"]
        EC_smooth = EC.rolling(win, min_periods=1).mean()

        y =  data["Y"]

        self.ax6.plot(y, EC, marker="x", label="raw data", )    
        self.ax6.plot(y, EC_smooth, label="rolling mean")    

        self.ax6.legend()


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

        # self.im_ma.remove()
        # self.im_ms.remove()

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

class AllExamples(Example7, Example6, Example5, Example4, Example3, Example2, Example1):
    def __init__(self):
        super().__init__()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("styles/darkTheme.qss", "r") as f:
        style = f.read()
        app.setStyleSheet(style)

    window = AllExamples()
    window.show()
    sys.exit(app.exec_())