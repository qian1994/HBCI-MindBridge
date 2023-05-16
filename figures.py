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
        self.slider.setGeometry(50, 350, 30, 200)
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(self.scrollBar)
        self.resize(1200, 750)
        # self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        # self.upScrollHeight = 0.3
    def setChannels(self, channels):
        labels = []
        self.labels = labels
        self.channels = channels
        if len(channels) <= 8:
            self.upScrollData = -0.2
        for i in range(len(channels)):
            self.numbers.append(0.95 - 0.08 * i + 0.0005 + self.upScrollData)
        self.slider.setRange(1, len(channels))
        self.slider.setValue(len(channels))
        selectChannelsIndex = []
        index = 0
        for channel in channels:
            selectChannelsIndex.append(self.channels.index(channel))
            index +=1
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
        plt.tight_layout(w_pad=0, h_pad=-2)
        plt.margins(0, 0)
        plt.margins(0, tight=True)
        self.fig.tight_layout(w_pad=0, h_pad=0)
        self.canvas = FigureCanvas(self.fig)
        self.vlayout = QVBoxLayout()
        self.vlayout.addWidget(self.canvas)
        self.setLayout(self.vlayout)
        self.ax = self.fig.gca()
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        self.ax.spines['top'].set_visible(False)


    def closeEvent(self, a0: QtGui.QCloseEvent):
        if self.signal and self.signal != None:
            self.signal._mainClose.emit('timeserise')
        return super().closeEvent(a0)
    
    def scrollBar(self, data):
        if len(self.channels) <= 8:
            return
        number = 0.06
        if len(self.channels) > 32:
            number = 0.07
        self.upScrollData = number * len(self.channels) / len(self.channels) * (len(self.channels)-data)
        self.numbers = []
        for i in range(len(self.channels)):
            self.numbers.append(0.95 - 0.08 * i + 0.0005 + self.upScrollData)

    def update(self, data):
        self.ax.clear()
        plt.yticks(self.numbers, self.showChannels, fontsize=9)
        plt.ylim(0, 1)
        for i in range(len(data)):
            if i not in self.seletChannelIndex:
                continue
            item = data[i] 
            if len(item) == 0:
                continue
            self.ax.plot(item*0.0005 + ( 0.95 - 0.08 * i) + self.upScrollData, color='lightgrey')
        self.fig.canvas.draw()  # 画布重绘，self.figs.canvas
        self.fig.canvas.flush_events()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     m = FigureWindow()
#     m.show()
#     sys.exit(app.exec_())
