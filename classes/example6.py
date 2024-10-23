from .interface import PlotInterface
from PyQt5.QtWidgets import QApplication
import pandas as pd

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

        self.ax6.plot(y, EC, marker="x", color='Crimson', label="raw data", linewidth=2, zorder=4)    
        self.ax6.plot(y, EC_smooth, color='orange', label="rolling mean", zorder=5)    

        self.ax6.legend()
