import numpy as np
from .interface import PlotInterface
from pathlib import Path

class Example8(PlotInterface):
    def __init__(self):
        super().__init__()

        self.tab8 = self.createTab('Ex08')

        self.inc = 0
        self.dcl = 0
    
        self.slider081 = self.createSlider(0, 6, 
            init=self.inc, 
            func=self.moveRectUp, 
            name='Rect up', 
            tab=self.tab8
        )

        self.slider082 = self.createSlider(0, 6,
            init=self.dcl,
            func=self.moveRectDown,
            name='Rect down',
            tab=self.tab8
        )

        self.ax8 = self.createAxes(
            self.tabAtr('Ex08Figure'),
            args={
                'pos': 111, 
                'name': 'V [ppm]',
                'xAxName': '$x$', 
                'yAxName': '$y$',
                'grid': True,
            }
        )

        current_dir = Path(__file__).parent.resolve()
        data_dir = current_dir.parent.parent / "PlotInterface" / "data" / "data.csv"
        x, y, V, U = np.loadtxt(data_dir, unpack=True)
        border = 1

        self.ax8.set_xlim((x[0] - border, x[-1] + border))
        self.ax8.set_ylim((y[0] - border, y[-1] + border))

        self.ax8.scatter(x, y, s=200, marker='+', color='crimson', linewidth=2, zorder=12)

        for i in range(np.size(V)):
            self.ax8.text(
                x[i] + 0.1, 
                y[i] + 0.1, 
                "{0:.0f}".format(V[i]), 
                color=self.ticksColor, 
                zorder=3,
                fontsize=12
            )

        self.plot081, = self.ax8.plot([], [], "--", color="orange")
        self.plot082, = self.ax8.plot([], [], "--", color="orange")
        self.plot083, = self.ax8.plot([], [], "--", color="orange")
        self.plot084, = self.ax8.plot([], [], "--", color="orange")

        self.redrawRect(self.inc, self.dcl)

    @PlotInterface.canvasDraw(tab='Ex08')
    def moveRectUp(self, inc):
       self.inc = inc
       self.redrawRect(self.inc, self.dcl)

    @PlotInterface.canvasDraw(tab='Ex08')
    def moveRectDown(self, dcl):
        self.dcl=  -dcl
        self.redrawRect(self.inc, self.dcl)

    def redrawRect(self, inc, dcl):
        x = [10.5 + inc, 14.5 + inc]
        y = [250.5 + dcl, 250.5 + dcl]
        self.plot081.set_data([x], [y])
        
        x = [10.5 + inc, 14.5 + inc]
        y = [246.5 + dcl, 246.5 + dcl]
        self.plot082.set_data([x], [y])
        
        x = [10.5 + inc, 10.5 + inc]
        y = [246.5 + dcl, 250.5 + dcl]
        self.plot083.set_data([x], [y])
        
        x = [14.5 + inc, 14.5 + inc]
        y = [246.5 + dcl, 250.5 + dcl]
        self.plot084.set_data([x], [y])


