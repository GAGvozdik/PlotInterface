from .interface import PlotInterface
import numpy as np
from pathlib import Path

# INTERFACE 2
class Example2(PlotInterface):
    def __init__(self):
        super().__init__()
        self.tab02 = self.createTab('Ex02')

        self.qdial02 = self.createQDial(
            10, 
            250, 
            10, 
            func=self.updateBins02, 
            name='bins', 
            tab=self.tab02, 
            label=True
        )

        self.ax02_1 = self.createAxes(
            self.tabAtr('Ex02Figure'),
            args={
                'pos': 111, 
                'name': 'plot 1',
                'xAxName': '', 
                'yAxName': '',
                'grid': True
            }
        )
        self.ax02_1.set_ylim(0, 3000)

        self.histData02 = np.array(np.random.normal(0, 1, 10000))
        self.hist02 = self.ax02_1.hist(self.histData02, bins=10, color='Crimson', zorder=2, edgecolor="black")

    @PlotInterface.canvasDraw(tab='Ex02')
    def updateBins02(self, index):
        for patch in self.hist02[2]: 
            patch.remove()  
            
        self.hist02 = self.ax02_1.hist(self.histData02, bins=index, color='Crimson', zorder=2, edgecolor="black")
        
        self.tabAtr('bins QDial Label').setText(str(index))



