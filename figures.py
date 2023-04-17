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
            # labels.append("200")
            labels.append(channels[len(channels)-1 - index])
            # labels.append("200")
            # numbers.append(index* 120 +240 - 40)
            numbers.append(index* 120 +240)
            # numbers.append(index* 120 +240 + 40)
            self.scale.append(0)
            self.nowTime.append(0)
        self.numbers = numbers
        self.labels = labels
        self.channels = channels
    def chooseShowChannel(self, channels):
        selectChannelsIndex = []
        for channel in channels:
            selectChannelsIndex.append(self.channels.index(channel))
        
        self.seletChannelIndex = selectChannelsIndex
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
        plt.yticks(self.numbers, self.labels, fontsize=9)
        plt.ylim(120, len(self.scale)* 120+ 240)
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
                # self.labels[i * 3 ] = str(int(min)) 
                # self.labels[i*3 +2] = str(int(maxD))
            if abs(self.scale[i] ) != 0:
                item /= self.scale[i]
            item *= 50
            item = item + (len(data)-i)*120 + 120
            self.ax.plot(item)
        self.fig.canvas.draw()  # 画布重绘，self.figs.canvas
        self.fig.canvas.flush_events()
    # def start(self):
    #     channels = [str(i+1) for i in range(32)]
    #     self.setChannels(channels)
    #     self.timer = QTimer()
    #     self.timer.timeout.connect(self.timeDownCount)
    #     self.timer.start(100)
    # def timeDownCount(self):
    #     data = self.createData()
    #     self.update(data)
    # def createData(self):
    #     data = []
    #     for i in range(32):
    #         sub = []
    #         for j in range(3000):
    #             sub.append(1850000 * random.randint(-1, 1))
    #         data.append(sub)
    #     return np.array(data, dtype=np.float64)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = FigureWindow()
    m.show()
    sys.exit(app.exec_())
