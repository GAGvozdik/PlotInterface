from .interface import PlotInterface

# INTERFACE 3
class Example3(PlotInterface):
    def __init__(self):
        super().__init__()

        self.tab3 = self.createTab('Ex3')
        
        self.ax31 = self.createAxes(self.tabAtr('Ex3Figure'),
            args={
                'pos': 231, 
                'name': 'plot 1',
                'xAxName': 'x', 
                'yAxName': 'y',
                'grid': True
            }
        )
        self.ax31.set_aspect(1)
        
        self.ax32 = self.createAxes(self.tabAtr('Ex3Figure'),
            args={
                'pos': 232, 
                'name': 'plot 2',
                'xAxName': 'x', 
                'yAxName': 'y',
                'grid': True
            }
        )
        self.ax32.set_aspect(5)

        self.ax33 = self.createAxes(self.tabAtr('Ex3Figure'),
            args={
                'pos': 233, 
                'name': 'plot 3',
                'xAxName': 'x', 
                'yAxName': 'y',
                'grid': True
            }
        )
        self.ax33.set_aspect(5)

        self.ax34 = self.createAxes(self.tabAtr('Ex3Figure'),
            args={
                'pos': 234, 
                'name': 'plot 4',
                'xAxName': 'x', 
                'yAxName': 'y',
                'grid': True
            }
        )
        self.ax34.set_aspect(0.5)

        self.ax35 = self.createAxes(self.tabAtr('Ex3Figure'),
            args={
                'pos': 235, 
                'name': 'plot 5',
                'xAxName': 'x', 
                'yAxName': 'y',
                'grid': True
            }
        )
        self.ax35.set_aspect(0.25)

        self.ax36 = self.createAxes(self.tabAtr('Ex3Figure'),
            args={
                'pos': 236, 
                'name': 'plot 6',
                'xAxName': 'x', 
                'yAxName': 'y',
                'grid': True
            }
        )
        self.ax36.set_aspect(1)


