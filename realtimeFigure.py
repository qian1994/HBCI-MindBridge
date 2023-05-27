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

class RealTimeFigure(QMainWindow):
    def __init__(self):
        super(RealTimeFigure, self).__init__()
        self.conn1 = None
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
        message = {'data': {'productId': '532', 'ip': '127.0.0.1', 'model': '0', 'low': 5, 'high': 45, 'filter': 0, 'order': 2,
                            'channels': ['O1', 'C3', 'CP3', 'P3', 'P7', 'TP7', 'T7', 'A1', 'FT7', 'F7', 'FC3', 'F3', 'CZ', 'FCZ', 'FZ', 'FP1', 'FP2', 'F4', 'C4', 'FC4',
                                         'F8', 'FT8', 'P8', 'A2', 'TP8', 'T8', 'CP4', 'P4', 'O2', 'CPZ', 'PZ', 'OZ']}}
        self.brainBoject.createFigures(message)
        self.setChannel(message['data']['channels'])
        # self.recv_signal()
        recive_data = Thread(target=self.recv_signal)
        recive_data.setDaemon(True)
        recive_data.start()
        # self.recv_signal()
       
    
    def filterBoardData(self, message):
        data = message['data']
        self.filterParams['low'] = data['low']
        self.filterParams['high'] = data['high']
        self.filterParams['filterType'] = data['filter']
        self.filterParams['order'] = data['order']

    def setChannel(self, channels):
        print('asdfasdf')
        
        self.channel = channels
        self.show()
        self.figures.setChannels( self.channel)
        self.figureFft.setChannels( self.channel)
        self.figureHeadPlot.setChannel( self.channel)

    def chooseShowChannel(self, channels):
        print('channels')

    def openWindow(self):
        self.show()

    def closeWindow(self):
        print('close window')
        self.hide()
    
    def filterData(self, data):
        dataprocessing = DataProcessing()

        boardData = data.copy()
        boardData = dataprocessing.handleFilter(data, 1000, self.filterParams['low'],
                                                     self.filterParams['high'], self.filterParams['order'], self.filterParams['filterType'])
        return boardData
    def update(self, data):
        data = np.array(data)
        # data = self.filterData(data)
        try:
            self.figures.update(data)
            self.figureHeadPlot.update(data)
            fftArray = self.dataprocessing.handleFFt(data, 1000)
            self.figureFft.update(fftArray)
        except Exception as e:
            print('this is update', e)
    def get_Signal(self, conn1):
        self.conn1 = conn1

    def recv_signal(self):
        while True:
            time.sleep(0.04)
            data = self.brainBoject.getCurrentData()
            self.update(data)
            # print(data.shape)
        # try:
        #     while True:
        #         if self.conn1 == None:
        #             continue
        #         res = self.conn1.recv()
        #         if res['action'] == 'update':
        #             self.update(res['data'])
                
        #         if res['action'] == 'channels':
        #             self.setChannel(res['data'])

        #         if res['action'] == 'show':
        #             self.openWindow()

        #         if res['action'] == 'close-window':
        #             self.closeWindow()
                
        #         if res['action'] == 'filter':
        #             self.filterData(res['data'])

        # except Exception as e:
        #     print('this is wrong', e)
def brainWindowFunc():
    app = QApplication(sys.argv)
    m = RealTimeFigure()
    m.show()
    # data =  np.random.rand(1000, 32) * 200
    # print(data.shape)
    # m.update(data)
    sys.exit(app.exec_())


def main():
    brainWindowFunc()


if __name__ == '__main__':
    main()