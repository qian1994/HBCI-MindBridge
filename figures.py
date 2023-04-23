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

import random
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
        
    def setChannels(self, channels):
        labels = []
        numbers = []
        for index in range(len(channels)):
            labels.append(channels[len(channels)-1 - index])
            numbers.append(index* 120 +240)
            self.scale.append(0)
            self.nowTime.append(0)
        self.numbers = numbers
        self.labels = labels
        self.channels = channels
    def getShowChannels(self):
        return self.showChannels
    def chooseShowChannel(self, channels):
        selectChannelsIndex = []
        numbers = []
        index = 0
        for channel in channels:
            numbers.append(index* 120 +240)
            selectChannelsIndex.append(self.channels.index(channel))
            index +=1
        self.seletChannelIndex = selectChannelsIndex
        self.showChannels = channels
        self.numbers = numbers
    def set_matplotlib(self):
        self.fig = plt.figure()
        plt.tight_layout(w_pad=0, h_pad=-2)
        plt.margins(0, 0)
        plt.margins(0, tight=True)
        plt.xlim(0, 5000)
        plt.ylim(0, 120)
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
    
    def update(self, data):
        self.ax.clear()
        plt.yticks(self.numbers, self.showChannels, fontsize=9)
        plt.ylim(120, len(self.seletChannelIndex)* 120+ 240)
        current_count = 0
        for i in range(len(data)):
            if i not in self.seletChannelIndex:
                continue
            item = data[i] 
            if (datetime.now().timestamp() - self.nowTime[i]) > 0.05:
                maxD = np.max(item)
                min = np.min(item) 
                self.scale[i] = maxD - min
                if self.scale[i] < 3:
                    self.scale[i] = 3
                self.nowTime[i] = datetime.now().timestamp()
            if abs(self.scale[i] ) != 0:
                item /= self.scale[i]
            item *= 50
            item = item + (len(self.seletChannelIndex)-current_count)*120 + 120
            self.ax.plot(item)
            current_count += 1
        self.fig.canvas.draw()  # 画布重绘，self.figs.canvas
        self.fig.canvas.flush_events()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = FigureWindow()
    m.show()
    sys.exit(app.exec_())
