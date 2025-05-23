from .interface import PlotInterface
import pandas as pd
from pathlib import Path

class Example6(PlotInterface):
    def __init__(self):
        super().__init__()

        self.tab06 = self.createTab('Ex06')

        ax6 = self.createAxes(self.tabAtr('Ex06Figure'),
            args={
                'pos': 111, 
                'name': 'EC [mS/m] 475 Hz, line 10',
                'xAxName': '$x$ [m]', 
                'yAxName': '',
                'grid': False
            }
        )
        
        current_dir = Path(__file__).parent.resolve()
        data_dir = current_dir.parent.parent / "PlotInterface" / "data" / "line10.csv"
        
        data = pd.read_csv(data_dir)
        EC = data["EC475Hz[mS/m]"]
        EC_smooth = EC.rolling(15, min_periods=1).mean()

        y =  data["Y"]

        ax6.plot(y, EC, marker="x", color='Crimson', label="raw data", linewidth=2, zorder=4)    
        ax6.plot(y, EC_smooth, color='orange', label="rolling mean", zorder=5)    

        ax6.legend(fontsize=20, markerscale=2)
