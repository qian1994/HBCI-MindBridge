from PyQt5.QtWidgets import *
import sys
from PyQt5.QtCore import QDir, QTimer, Qt, QObject
import numpy as np
from figureHeadPlot import FigureHeadPlotWidget
from figuresFFT import FiguresFFTWindow
from figures import FigureWindow 
from dataPorcessing import DataProcessing
class Ui_RealTimeFigure(object):
    def setupUi(self, figureWidge):
        print('ui_figure widget')
class RealTimeFigure(QWidget, Ui_RealTimeFigure):
    def __init__(self):
        super(RealTimeFigure, self).__init__()

        self.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.resize(1200, 600)
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.content = QHBoxLayout()
        self.content.setSpacing(0)

        self.content.setContentsMargins(0, 0, 0, 0)

        self.content.setSpacing(0)
        self.content.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)

        # central_widget = QWidget()
        # central_widget.setLayout(layout)
        # central_widget.setContentsMargins(0, 0, 0, 0)
        # self.setCentralWidget(central_widget)

        self.widget = QWidget()
        self.widget.setContentsMargins(0, 0, 0, 0)
        self.widget.setLayout(self.content)
        
        self.figures = FigureWindow()
        self.figureFft = FiguresFFTWindow()
        self.figureHeadPlot = FigureHeadPlotWidget()

        self.content.addWidget(self.figures)
        self.leftLayout = QVBoxLayout()
        self.leftLayout.setSpacing(0)
        self.leftWidget = QWidget()
        self.leftWidget.setContentsMargins(0, 0, 0, 0)
        self.leftLayout.setContentsMargins(0, 0, 0, 0)
        self.leftLayout.addWidget(self.figureFft)
        self.leftLayout.addWidget(self.figureHeadPlot)
        self.leftWidget.setLayout(self.leftLayout)
        self.content.addWidget(self.leftWidget)
        layout.addWidget(self.widget)

        self.dataprocessing = DataProcessing()
        self.setLayout(layout)
    def setChannel(self, channels):
        self.channel = channels
        self.figures.setChannels( self.channel)
        self.figureFft.setChannels( self.channel)
        self.figureHeadPlot.setChannel( self.channel)
    def chooseShowChannel(self, channels):
        print('channels')
        
    def update(self, data):
        self.figures.update(data)
        self.figureHeadPlot.update(data)
        fftArray = self.dataprocessing.handleFFt(data, 1000)
        self.figureFft.update(fftArray)
    
        
