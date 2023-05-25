import numpy as np
import mne
from mne.channels import make_standard_montage
from mne.viz import plot_topomap
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys
import matplotlib

matplotlib.use("Qt5Agg")  # 声明使用QT5

class Ui_figureHeadPlotWidget(object):
    def setupUi(self, FigureHeadPlotWidget):
        print('Ui_figureHeadPlotWidget')
    
class FigureHeadPlotWidget(QWidget, Ui_figureHeadPlotWidget):
    def __init__(self):
        super(FigureHeadPlotWidget, self).__init__()
        self.fig = None
        self.channels = []
        self.ch_types = []
        self.sfreq = 1000
        self.info = None
        self.setupUi(self)
        self.set_matplotlib()
        self.setWindowTitle("head plot")
        self.resize(1200, 800)
        self.move(200, 100)
    def setChannel(self, channels):
        montage = make_standard_montage('standard_1020')
        channels_names = montage.ch_names
        channels_name_up = [item.upper() for item in channels_names]
        for index in range(len(channels)):
            if channels[index] == "US":
                del channels[index]
            id = channels_name_up.index(channels[index])
            channels[index] = channels_names[id]
        self.channels = channels
        self.ch_types = ['eeg'] * len(channels)
        self.info = mne.create_info(channels, self.sfreq, self.ch_types)
        # Load a standard electrode montage
        self.info.set_montage(montage)

    def set_matplotlib(self):
        self.fig = plt.figure()
        # plt.tight_layout(w_pad=-3, h_pad=-2)
        plt.margins(0, 0)
        plt.margins(0, tight=True)
        # self.fig.tight_layout(w_pad=-3, h_pad=0)
        self.canvas = FigureCanvas(self.fig)
        self.vlayout = QVBoxLayout()
        self.vlayout.addWidget(self.canvas)
        self.setLayout(self.vlayout)
        self.ax = self.fig.gca()
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        self.ax.spines['top'].set_visible(False)
        plt.subplots_adjust(left=0.05, right=1)
        
    def update(self, boardData):
        if len(boardData) != 0:
            self.ax.clear()
            data = np.mean(boardData, axis=1)
            plot_topomap(data, self.info, axes=self.ax, show=False,  extrapolate='head')
            self.canvas.draw()
