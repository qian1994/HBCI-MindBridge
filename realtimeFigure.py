from PyQt5.QtWidgets import *
import sys
from PyQt5.QtCore import QDir, QTimer, Qt, QObject
import numpy as np
from PyQt5 import QtGui
import time
from figureHeadPlot import FigureHeadPlotWidget
from figuresFFT import FiguresFFTWindow
from figures import FigureWindow
from dataPorcessing import DataProcessing
from threading import Thread, current_thread
from brainFigure import BrainWindow as BrainObject
import multiprocessing.connection as mp_conn
import os

class RealTimeFigure(QMainWindow):
    def __init__(self):
        super(RealTimeFigure, self).__init__()
        self.conn1 = None
        self.channel = []
        MainWidget = QWidget()
        self.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.setWindowTitle('brain wave')
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

        self.widget = QWidget()
        self.widget.setContentsMargins(0, 0, 0, 0)
        self.widget.setLayout(self.content)

        self.figures = FigureWindow()
        self.figureFft = FiguresFFTWindow()
        self.figureHeadPlot = FigureHeadPlotWidget()
        self.figures.hide()
        self.figureHeadPlot.hide()
        self.figureFft.hide()
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
        MainWidget.setLayout(layout)
        self.setCentralWidget(MainWidget)
        self.filterParams = dict({
            'high': 45,
            "low": 5,
            "order": 2,
            "filterType": 0,
        })

        self.brainBoject = BrainObject()
        self.recive_data = Thread(target=self.recv_signal)
        self.recive_data.setDaemon(True)
        self.recive_data.start()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)

    def filterBoardData(self, message):
        data = message['data']
        self.filterParams['low'] = data['low']
        self.filterParams['high'] = data['high']
        self.filterParams['filterType'] = data['filter']
        self.filterParams['order'] = data['order']

    def setChannel(self, channels):
        self.channel = channels
        self.figures.setChannels(self.channel)
        self.figureFft.setChannels(self.channel)
        self.figureHeadPlot.setChannel(self.channel)
        self.figures.show()
        self.figureHeadPlot.show()
        self.figureFft.show()

    def chooseShowChannel(self, channels):
        print('channels')

    def openWindow(self):
        print('open window')
        self.show()

    def closeWindow(self):
        print('close window')
        self.hide()

    def showEvent(self, a0: QtGui.QShowEvent):
        return super().showEvent(a0)
    
    def filterData(self, data):
        dataprocessing = DataProcessing()
        boardData = data.copy()
        boardData = dataprocessing.handleFilter(boardData, 1000, self.filterParams['low'],
                                                self.filterParams['high'], self.filterParams['order'], self.filterParams['filterType'])
        return boardData

    def update(self, data):
        data = np.array(data)
        if len(data) == 0 or len(data[0]) == 0 or len(self.channel) == 0:
            return
        try:
            data = self.filterData(data)
            self.figures.update(data)
            self.figureHeadPlot.update(data)
            fftArray = self.dataprocessing.handleFFt(data, 1000)
            self.figureFft.update(fftArray)
            
        except Exception as e:
            print('this is update', e)

    def toggleWave(self, flag):
        if flag:
            self.figures.show()
        else:
            self.figures.hide()

    def toggleFft(self, flag):
        if flag:
            self.figureFft.show()
            self.leftWidget.show()
        else:
            self.figureFft.hide()
            if self.figureHeadPlot.isVisible() == False:
                self.leftWidget.hide()

    def toggleHeadPlot(self, flag):
        if flag:
            self.figureHeadPlot.show()
            self.leftWidget.show()
        else:
            self.figureHeadPlot.hide()
            if self.figureFft.isVisible() == False:
                self.leftWidget.hide()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        os._exit(0)

    def get_Signal(self, conn1):
        self.conn1 = conn1

    def recv_signal(self):
        startTime = time.time()
        while True:
            currentTime = time.time()
            if currentTime - startTime > 0.04:
                data = self.brainBoject.getCurrentData()
                self.update(data)
                startTime = currentTime
            if self.conn1 == None:
                continue
            res = ""
            if mp_conn.wait([self.conn1], timeout=0):
                res = self.conn1.recv()
            if res == '':
                continue
            if res['action'] == 'open-window':
                if len(self.channel) != 0:
                    continue
                self.openWindow()
                self.brainBoject.createFigures(res['data'])
                self.setChannel(res['data']['data']['channels'])
                continue

            if res['action'] == 'trigger':
                print('action', res['data'])
                self.brainBoject.trigger(res['data'])
                continue

            if res['action'] == 'start-session':
                self.brainBoject.startSession(res['data'])
                continue

            if res['action'] == 'stop-session':
                self.brainBoject.stopSession(res['data'])
                continue

            if res['action'] == 'start-stream':
                self.brainBoject.startStream(res['data'])

            if res['action'] == 'stop-stream':
                self.brainBoject.stopStream(res['data'])

            if res['action'] == 'close-window':
                self.showMaximized()
                continue

            if res['action'] == 'close-app':
                self.close()

            if res['action'] == 'filter':
                self.filterBoardData(res['data'])
                continue

            if res['action'] == 'toggle-wave':
                self.toggleWave(res['data'])
                continue

            if res['action'] == 'toggle-fft':
                self.toggleFft(res['data'])
                continue

            if res['action'] == 'toggle-headplot':
                self.toggleHeadPlot(res['data'])
                continue

            if res['action'] == 'get-current-data':
                self.conn1.send({'action': 'current-data',
                                "data": self.brainBoject.getCurrentData()})

            if res['action'] == 'end-task-file':
                csvFile= self.brainBoject.endTaskSaveData(res['data'])
                self.conn1.send({'action': 'task-end-file',
                                "data": {"csv": csvFile}})

def brainWindowFunc():
    app = QApplication(sys.argv)
    m = RealTimeFigure()
    m.show()
    # m.setChannel(['1', '2', '3'])
    message =  {"data":{'productId': '532', 'ip': '127.0.0.1', 'model': '0', 'low': 5, 'high': 45, 'filter': 0, 'order': 2,
                         'channels': ['O1','C3', 'CP3', 'P3', 'P7', 'TP7', 'T7', 'A1', 'FT7', 'F7', 'FC3', 'F3', 'CZ', 'FCZ', 'FZ', 'FP1',
                                      'FP2', 'F4', 'C4', 'FC4', 'F8', 'FT8', 'P8', 'A2', 'TP8', 'T8', 'CP4', 'P4', 'O2', 'CPZ', 'PZ', 'OZ']}}
    
    m.brainBoject.createFigures(message)
    m.setChannel(message['data']['channels'])
    # data =  np.random.rand(1000, 32) * 200
    # print(data.shape)
    # m.update(data)
    sys.exit(app.exec_())


def main():
    brainWindowFunc()


if __name__ == '__main__':
    main()
