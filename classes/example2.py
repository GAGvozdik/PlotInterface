from .interface import PlotInterface
import numpy as np

# INTERFACE 2
class Example2(PlotInterface):
    def __init__(self):
        super().__init__()
        self.tab2 = self.createTab('Ex2')
        #TODO set ax limit
        #TODO add qdial label


        self.qdial2 = self.createQDial(10, 250, 10, func=self.updateBins, name='bins', tab=self.tab2, label=True)
        self.addToBox(self.tabAtr('Ex2SliderBox'), self.qdial2)

        self.histData = np.array(np.random.normal(0, 1, 10000))

        self.ax21 = self.createAxes(self.tabAtr('Ex2Figure'),
            args={
                'pos': 111, 
                'name': 'plot 1',
                'xAxName': '', 
                'yAxName': '',
                'grid': True
            }
        )

        self.ax21.set_ylim(0, 3000)

        self.hist1 = self.ax21.hist(self.histData, bins=10, color='Crimson', zorder=2, edgecolor="black")

    @PlotInterface.canvasDraw(tab='Ex2')
    def updateBins(self, index):
        for patch in self.hist1[2]: 
            patch.remove()  
            
        self.hist1 = self.ax21.hist(self.histData, bins=index, color='Crimson', zorder=2, edgecolor="black")
        
        self.tabAtr('bins QDial Label').setText(str(index))



