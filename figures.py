import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtCore import QDir, QTimer, Qt
import matplotlib
from PyQt5 import QtCore, QtWidgets
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, WindowOperations, DetrendOperations
from signals import Signal
from datetime import datetime
from matplotlib.widgets import Slider
from PyQt5.QtCore import Qt, QEvent
class Ui_figureWidget(object):
    def setupUi(self, figureWidge):
        print('ui_figure widget')
class FigureWindow(QWidget, Ui_figureWidget):
    def __init__(self):
        super(FigureWindow, self).__init__()
        self.setupUi(self)
        self.set_matplotlib()
        self.setWindowTitle("timeserise")
        self.resize(1200, 800)
        self.move(200, 100)
        self.signal = Signal()
        self.scale = []
        self.nowTime = []
        self.showChannels = []
        self.seletChannelIndex = []
        self.channels = []
        self.numbers = []
        plt.ioff()
        self.slider = None
        self.upScrollData = 0
        self.slider = QSlider(Qt.Vertical, self)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setGeometry(10, 350, 15, 200)
        self.slider.setTickInterval(0)
        self.slider.valueChanged.connect(self.scrollBar)
        self.splitMargin = 30
        # self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        # self.upScrollHeight = 0.3
    def setChannels(self, channels):
        labels = []
        self.labels = labels
        self.channels = channels
        for i in range(len(channels)):
            self.numbers.append(len(channels) * self.splitMargin - ((i + 0.5)  * self.splitMargin) + self.upScrollData)
        self.slider.setRange(1, len(channels))
        self.slider.setValue(len(channels))
        selectChannelsIndex = []
        for channel in channels:
            selectChannelsIndex.append(self.channels.index(channel))
        self.seletChannelIndex = selectChannelsIndex
        self.showChannels = channels
    
    def getShowChannels(self):
        return self.showChannels
    
    def chooseShowChannel(self, channels):
        return
        # selectChannelsIndex = []
        # index = 0
        # for channel in channels:
        #     selectChannelsIndex.append(self.channels.index(channel))
        #     index +=1
        # self.seletChannelIndex = selectChannelsIndex
        # self.showChannels = channels
       
    def set_matplotlib(self):
        self.fig = plt.figure()
        plt.margins(0, 0)
        plt.margins(0, tight=True)
        self.canvas = FigureCanvas(self.fig)
        self.vlayout = QVBoxLayout()
        self.vlayout.addWidget(self.canvas)
        self.setLayout(self.vlayout)
        self.ax = self.fig.gca()
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        self.ax.spines['top'].set_visible(False)
        plt.subplots_adjust(left=0.05, right=1)

    def closeEvent(self, a0: QtGui.QCloseEvent):
        if self.signal and self.signal != None:
            self.signal._mainClose.emit('timeserise')
        return super().closeEvent(a0)
    
    def scrollBar(self, data):
        self.upScrollData = self.splitMargin *  (len(self.channels) - data )
        self.numbers = []
        for i in range(len(self.channels)):
            self.numbers.append(len(self.channels) * self.splitMargin - ((i + 0.5) * self.splitMargin) + self.upScrollData)

    def update(self, data):
        self.ax.clear()
        self.ax.set_yticks(self.numbers, self.showChannels, fontsize=9)
        self.ax.set_ylim((len(self.channels) - 8) * self.splitMargin ,  len(self.channels) * self.splitMargin )
        if len(data) != 0:
            plt.xlim(500, len(data[0]))
        for i in range(len(data)):
            item = data[i]
            item -= np.mean(item) 
            item = len(data) * self.splitMargin - self.splitMargin * (i + 0.5)  + self.upScrollData + item 
            item[item == 0] = len(data) * self.splitMargin - self.splitMargin * (i + 0.5)  + self.upScrollData
            self.ax.plot(np.arange(500, len(item)), item[500: 5000], color='lightgrey')
        self.fig.canvas.draw()  # 画布重绘，self.figs.canvas
        self.fig.canvas.flush_events()
