import time
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
import math
import numpy as np
from plot import Plot
import logging
logging.basicConfig(level=logging.INFO)

class LiveGraph():
    
    
    def __init__(self,plotdata,inteactiveMode = True) -> None:
        
        
        # plotData = [grain,dataNames,overAllName,colors]
        
        self.fig = plt.figure(figsize=(10,10))
        
        self.plots = []
        for i,data in enumerate(plotdata):
            self.plots.append(Plot(
                                   self.fig,
                                   self.fig.add_subplot(len(plotdata),1,i+1),
                                   data[0],
                                   data[1],
                                   data[2],
                                   data[3] if len(data) > 3 else None
                                   ))
        

        
        self.tick = 0
        plt.show(block = False)
        plt.pause(0.1)  
        if inteactiveMode: 
            plt.ion() 
        else:
            pass
            # self.fig.canvas.mpl_connect('draw_event', self.updateOnWindowChange)
            # TODO: Allow for non interactive mode with window change detection and then updating after change 
        
        
    def update(self,y: list[list[int,]] = None ,drawInSequence: bool = True) -> None :
        
        
        
        
        self.tick += 1
        if drawInSequence:
            [plot.restore() for plot in self.plots]
            [plot.setYData(y[i]) for i, plot in enumerate(self.plots)] if y is not None else None
            [plot.draw_artist() for plot in self.plots]
            [plot.blit() for plot in self.plots]
        else:
            for i,plot in enumerate(self.plots):
                plot.restore()
                plot.setYData(y[i]) if y is not None else None
                plot.draw_artist()
                plot.blit()
        self.fig.canvas.flush_events()
        
    def updateOnWindowChange(self,event):
        
        for plot in self.plots:
            if event is not None:
                if event.canvas != self.fig.canvas:
                    raise RuntimeError
            plot.updateBg()
        self.update()
    
            
        
            

        

            
        
    
    