import time
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import figure, axes
matplotlib.use('TkAgg')
import numpy as np
import math
import logging

logging.basicConfig(level=logging.INFO)



class Plot():
    
    def __init__(self,fig: figure , ax: axes ,grain: int,dataNames: list[int,] , names = list[str],colors = None ) -> None:
        
        

        self.fig = fig
        self.ax = ax
        self.grain = grain
        
        
        self.names = names
        self.color = "r" * len(dataNames) if colors is None else colors
        
        
        self.xData = range(grain)
        
        self.yData = []
        self.Lines = []
        
        
        for i in range(len(dataNames)):
            self.yData.append([0] * grain ) 
            ln, = self.ax.plot(self.xData,self.yData[i] , animated=False,label=dataNames[i], color=colors[i])
            
            self.Lines.append(ln)            
        
    
        self.minVal = 0
        self.maxVal = 0 
        
        
        
        self.fig.canvas.draw()
        self.fig.show()
        
        self.bg = fig.canvas.copy_from_bbox(self.ax.bbox)
        self.fig.canvas.blit(self.ax.bbox)
        self.ax.legend()
        
            
    def restore(self):
        self.fig.canvas.restore_region(self.bg)
    
    def setYData(self,y:list[int,]): # for loop could be made more readable 
        for i,yVal in enumerate(y):
            self.yData[i].append(yVal) 
            self.yData[i].pop(0) 
            
            self.Lines[i].set_ydata(self.yData[i]) # every line has its own yData
        
        
    def draw_artist(self,minVal:int  = None, maxVal: int = None):
        
        currMax = max([max(y) for y in self.yData ])
        currMin = min([min(y) for y in self.yData ])
        
        # TODO: when the graph is more that 10% away from the edges start shrinking it for a cirtain % every call
        # need to do this to be able to see spikes but also shrink back when they occoer.
        
        if maxVal is None:
            if self.maxVal <= currMax:
                self.maxVal = currMax    # sets the maxVal to the highest value ever recorded in the timeline if the data 
            else:
                self.maxVal *= .95
                        
        if minVal is None:
            if self.minVal >= currMin:
                self.minVal = currMin  
            else:
                self.minVal *= .95
            
        for line in self.Lines:
            self.ax.draw_artist(line)
            
        self.ax.axis([0,self.grain,self.minVal,self.maxVal])
            
        self.ax.set_title(self.names)
        self.ax.legend()
        
        
    def blit(self):
        self.fig.canvas.blit(self.fig.bbox)
        
    def updateBg(self):
        self.bg = self.fig.canvas.copy_from_bbox(self.ax.bbox)