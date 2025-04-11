from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog
import numpy as np
import geone as gn
from matplotlib.colors import LinearSegmentedColormap
from .interface import PlotInterface
import matplotlib.pyplot as plt
from pathlib import Path

class Example17(PlotInterface):
    def __init__(self):
        super().__init__()
        
        self.tab17 = self.createTab('Ex17')
        
        self.loadButton = QPushButton("Load file")
        self.loadButton.clicked.connect(self.loadFile17)
        self.addToBox(self.tabAtr('Ex17SliderBox'), self.loadButton)

        self.qdial17_1 = self.createQDial(1, 200, 80, func=self.updateParameter17_1, name='parameter', tab=self.tab17, label=True)

        self.drawAxes17()
        



    def loadFile17(self):
        # self.x, self.y, self.v = self.load_file()
        # self.xy_data = np.array((self.x, self.y)).T
        print(self.load_file())

        # self.ti = gn.img.readImageTxt("self.ti.txt")
        # self.plotScatter17()
        # self.plotVariogram17()
        # self.plotHist()
        # self.plotVariogramRose17()
        
        self.tabAtr('Ex17Canvas').draw()

    @PlotInterface.getWorkTime('updateParameter17_1')
    @PlotInterface.canvasDraw(tab='Ex17')
    def updateParameter17_1(self, anis):
        self.anis = anis       
        # self.tabAtr('QDial Label').setText(str(self.anis))
        self.redraw()


    def redraw17(self):

        self.ti.get_unique()

        categ_val = [0, 1, 2]
        categ_col = ['#1b9e77', "#d95f02", '#7570b3']

        nx, ny, nz = 100, 100, 1         # number of cells
        sx, sy, sz = self.ti.sx, self.ti.sy, self.ti.sz # cell unit
        ox, oy, oz = 0.0, 0.0, 0.0       # origin (corner of the "first" grid cell)

        # current_dir = Path(__file__).parent.resolve()
        # data_dir = current_dir.parent.parent / "PlotInterface" / "data" / "artic135_subsample.txt"
        
        hd = gn.img.readPointSetTxt('hd.txt')

        hd_col = gn.imgplot.get_colors_from_values(hd.val[3], categ=True, categVal=categ_val, categCol=categ_col)

    
        im_empty = gn.img.Img(nx, ny, nz, sx, sy, sz, ox, oy, oz, nv=0)


        nreal = 20
        deesse_input = gn.deesseinterface.DeesseInput(
            nx=nx, ny=ny, nz=nz,        # dimension of the simulation grid (number of cells)
            sx=sx, sy=sy, sz=sz,        # cells units in the simulation grid
            ox=ox, oy=oy, oz=oz,        # origin of the simulation grid
            nv=1, varname='code',       # number of variable(s), name of the variable(s)
            TI=self.ti,                      # TI (class gn.deesseinterface.Img)
            dataPointSet=hd,            # hard data (optional)
            distanceType='categorical', # distance type: proportion of mismatching nodes (categorical var., default)
            #conditioningWeightFactor=10.,  # put more weight to conditioning data (if needed)
            nneighboringNode=24,        # max. number of neighbors (for the patterns)
            distanceThreshold=0.05,     # acceptation threshold (for distance between patterns)
            maxScanFraction=0.25,       # max. scanned fraction of the TI (for simulation of each cell)
            npostProcessingPathMax=1,   # number of post-processing path(s)
            seed=444,                   # seed (initialization of the random number generator)
            nrealization=nreal)         # number of realization(s)


        deesse_output = gn.deesseinterface.deesseRun(deesse_input, nthreads=8)

        sim = deesse_output['sim']

        hd_col = gn.imgplot.get_colors_from_values(hd.val[3], categ=True, categVal=categ_val, categCol=categ_col) 

        plt.subplots(1, 3, figsize=(17,5), sharey=True)
        for i in range(3):
            plt.subplot(1, 3, i+1)
            
        
            gn.imgplot.drawImage2D(sim[i], categ=True, categVal=categ_val, categCol=categ_col) 
            plt.scatter(hd.x(), hd.y(), marker='o', s=50, color=hd_col, edgecolors='black', linewidths=1)
            
            plt.title(f'Real. #{i}')

        # plt.show()

        

    def drawAxes17(self):
        self.ax17_1 = self.createAxes(self.tabAtr('Ex17Figure'), args={'pos': 231})
        self.ax17_2 = self.createAxes(self.tabAtr('Ex17Figure'), args={'pos': 232})
        self.ax17_3 = self.createAxes(self.tabAtr('Ex17Figure'), args={'pos': 233})
        self.ax17_4 = self.createAxes(self.tabAtr('Ex17Figure'), args={'pos': 234})
        self.ax17_5 = self.createAxes(self.tabAtr('Ex17Figure'), args={'pos': 235})
        self.ax17_6 = self.createAxes(self.tabAtr('Ex17Figure'), args={'pos': 236})


    


# a 3
# b 1
# c 2
# d 4

# range of data2 > rage data 1