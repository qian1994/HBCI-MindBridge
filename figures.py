from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from signals import Signal
from PyQt5.QtWidgets import  QVBoxLayout, QWidget, QLabel, QScrollArea
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
import numpy as np
from config import impedence32
class RealTimePlotWidget(QWidget):
    def __init__(self, num_plots=32, parent=None):
        super().__init__(parent)
        
        self.num_plots = num_plots
        self.curves = []
        self.plots = []
        self.channels = impedence32
        self.lables = []
        self.plot_widget = None
        self.layout = QVBoxLayout(self)
        self.initUI()

    def set_range(self, number):
        if number <= 0:
            self.plot_widget.enableAutoRange()
        elif number == 50:
            self.plot_widget.setRange(yRange=[-50, 50])
        elif number == 100:
            self.plot_widget.setRange(yRange=[-100, 100])
        elif number == 200:
            self.plot_widget.setRange(yRange=[-200, 200])    
        elif number == 1000:
            self.plot_widget.setRange(yRange=[-1000, 1000])   
        elif number == 10000:
            self.plot_widget.setRange(yRange=[-10000, 10000]) 
    def initUI(self):
        hbox = QVBoxLayout()

        for i in range(self.num_plots):
            label = QLabel(self.channels[i], self)
            self.lables.append(label)
            hbox.addWidget(label)
            self.plot_widget = pg.PlotWidget()
            self.plot_widget.setBackground(None)
            self.plot_widget.getPlotItem().getViewBox().setMouseEnabled(x=False, y=False)
            self.plot_widget.enableAutoRange()
            color = QtGui.QColor(128,128,128)
            curve = self.plot_widget.plot(pen=pg.mkPen(color=color, width=2))
            self.curves.append(curve)
            self.plots.append(self.plot_widget)
            self.set_range(0)
            hbox.addWidget(self.plot_widget)
        self.layout.addLayout(hbox)
    def setChannels(self, channels):
        self.channels = channels
        for i in range(len(channels)):
            self.lables[i].setText(channels[i])
    def update_data(self, data):
        # Update the data for each plot
        for i, curve in enumerate(self.curves):
            curve.setData(data[i][200:])

class Ui_figureWidget(object):
    def setupUi(self, figureWidge):
        print('ui_figure widget')
class FigureWindow(QWidget, Ui_figureWidget):
    def __init__(self):
        super(FigureWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("timeserise")
        self.signal = Signal()
        self.channels = []
        self.mainLayout = QHBoxLayout()
        self.setLayout(self.mainLayout)
        self.scroll_area = QScrollArea()
        self.mainLayout.addWidget(self.scroll_area)
        self.scroll_widget = None
        self.scroll_widget = RealTimePlotWidget()
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)

    def setChannels(self, channels):
        self.showChannels = channels
        self.scroll_widget.setChannels(channels)

    def closeEvent(self, a0: QtGui.QCloseEvent):
        if self.signal and self.signal != None:
            self.signal._mainClose.emit('timeserise')
        return super().closeEvent(a0)
    

    def update(self, data):
        if self.scroll_widget != None:
            self.scroll_widget.update_data(data)
