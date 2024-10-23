import numpy as np
from .interface import PlotInterface

class Example8(PlotInterface):
    def __init__(self):
        super().__init__()

        self.tab8 = self.createTab('Ex8')

        self.inc = 0
        self.dcl = 0
    
        self.slider81 = self.createSlider(0, 6, 
            init=self.inc, 
            func=self.moveRectUp, 
            name='Rect up', 
            tab=self.tab8
        )
        self.addToBox(self.tabAtr('Ex8SliderBox'), self.slider81)

        self.slider82 = self.createSlider(0, 6,
            init=self.dcl,
            func=self.moveRectDown,
            name='Rect down',
            tab=self.tab8
        )
        self.addToBox(self.tabAtr('Ex8SliderBox'), self.slider82)

        self.ax8 = self.createAxes(self.tabAtr('Ex8Figure'),
            args={
                'pos': 111, 
                'name': 'V [ppm]',
                'xAxName': '$x$', 
                'yAxName': '$y$',
                'grid': True,
            }
        )

        xx, yy, V, U = np.loadtxt("data/data.csv", unpack=True)
        border = 1

        self.ax8.set_xlim((xx[0] - border, xx[-1] + border))
        self.ax8.set_ylim((yy[0] - border, yy[-1] + border))

        self.ax8.scatter(xx, yy, s=200, marker='+', color='crimson', linewidth=2, zorder=12)

        for i in range(np.size(V)):
            self.ax8.text(
                xx[i] + 0.1, 
                yy[i] + 0.1, 
                "{0:.0f}".format(V[i]), 
                color=self.ticksColor, 
                zorder=3,
                fontsize=12
            )

        self.plot81, = self.ax8.plot([], [], "--", color="orange")
        self.plot82, = self.ax8.plot([], [], "--", color="orange")
        self.plot83, = self.ax8.plot([], [], "--", color="orange")
        self.plot84, = self.ax8.plot([], [], "--", color="orange")

        self.redrawRect(self.inc, self.dcl)

    @PlotInterface.canvasDraw(tab='Ex8')
    def moveRectUp(self, inc):
       self.inc = inc
       self.redrawRect(self.inc, self.dcl)

    @PlotInterface.canvasDraw(tab='Ex8')
    def moveRectDown(self, dcl):
        self.dcl=  -dcl
        self.redrawRect(self.inc, self.dcl)

    def redrawRect(self, inc, dcl):
        x = [10.5 + inc, 14.5 + inc]
        y = [250.5 + dcl, 250.5 + dcl]
        self.plot81.set_data([x], [y])
        
        x = [10.5 + inc, 14.5 + inc]
        y = [246.5 + dcl, 246.5 + dcl]
        self.plot82.set_data([x], [y])
        
        x = [10.5 + inc, 10.5 + inc]
        y = [246.5 + dcl, 250.5 + dcl]
        self.plot83.set_data([x], [y])
        
        x = [14.5 + inc, 14.5 + inc]
        y = [246.5 + dcl, 250.5 + dcl]
        self.plot84.set_data([x], [y])


