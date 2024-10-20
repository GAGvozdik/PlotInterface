from .interface import PlotInterface
from PyQt5.QtWidgets import QApplication
import numpy as np
import sys
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

        self.ax6.plot(y, EC, marker="x", label="raw data", )    
        self.ax6.plot(y, EC_smooth, label="rolling mean")    

        self.ax6.legend()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("styles/darkTheme.qss", "r") as f:
        style = f.read()
        app.setStyleSheet(style)

    window = Example6()
    window.show()
    sys.exit(app.exec_())
