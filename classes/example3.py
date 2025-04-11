from .interface import PlotInterface
from pathlib import Path

# INTERFACE 3
class Example3(PlotInterface):
    def __init__(self):
        super().__init__()

        self.tab03 = self.createTab('Ex03')
        self.createAxes03()

    def createAxes03(self):
        axArgs = {
            'xAxName': 'x', 
            'yAxName': 'y',
        }

        axArgs['pos'], axArgs['name'] = 231, 'data1'
        self.ax03_1 = self.createAxes(self.tabAtr('Ex03Figure'), args=axArgs)
        self.ax03_1.set_aspect(1)

        axArgs['pos'], axArgs['name'] = 232, 'data2'
        self.ax03_2 = self.createAxes(self.tabAtr('Ex03Figure'), args=axArgs)
        self.ax03_2.set_aspect(5)

        axArgs['pos'], axArgs['name'] = 233, 'data3'
        self.ax03_3 = self.createAxes(self.tabAtr('Ex03Figure'), args=axArgs)
        self.ax03_3.set_aspect(5)

        axArgs['pos'], axArgs['name'], axArgs['grid'] = 234, 'data4', True
        self.ax03_4 = self.createAxes(self.tabAtr('Ex03Figure'), args=axArgs)
        self.ax03_4.set_aspect(0.5)

        axArgs['pos'], axArgs['name'], axArgs['xAxName'], axArgs['yAxName'] = 235, 'data5', 'x[m]', 'y[m]'
        self.ax03_5 = self.createAxes(self.tabAtr('Ex03Figure'), args=axArgs)
        self.ax03_5.set_aspect(0.25)

        axArgs['pos'], axArgs['name'] = 236, 'data6'
        self.ax03_6 = self.createAxes(self.tabAtr('Ex03Figure'), args=axArgs)
        self.ax03_6.set_aspect(1)


