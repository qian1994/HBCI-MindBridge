import os
import sys
import json
import time
import numpy as np
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtCore import QDir, QTimer, Qt, QObject
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *
from jsBridge import JsBridge
from signals import Signal
from brainflow.data_filter import DataFilter, FilterTypes, DetrendOperations
from startSocketClient import SocketCustomClient
from threading import Thread, current_thread
from multiprocessing import Process, Pipe, Queue, Manager
from brainFigure import BrainWindow
conn1, conn2 = Pipe()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stackData = []
        self.dir_path = '.'
        self.dir_path = self.dir_path.replace("\\", "/", 5)
        self.time = time.time()
        self.boartStatus = None
        self.setStyleSheet("background-color:rgb(128, 128, 128)")
        self.fileName = None
        self.brainflow_file_name = None
        self.webView = None
        self.webViewWidget = None
        self.webViewlayout = None
        self.widget = QWidget()
        self.content = QHBoxLayout()
        self.content.setSpacing(0)
        self.widget.setLayout(self.content)
        self.setWindowTitle('MindBridge')
        self.resize(1200, 600)
        self.content.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.widget.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.widget)
        self.createWebEng()
        self._signal = Signal()
        self._signal._mainClose[str].connect(self._sub_close)
        self.devToolsStatus = None
        self.filterParams = dict({
            'high': 45,
            "low": 5,
            "order": 2,
            "filterType": 0,
        })
        self.badChannel = None
        self.SocketCustomClient = None
        self.MindBridgefileName = ''
        self.processing = None
        self.message = None
        self.currentData = []
        self.conn2 = None
        self.recvSignalData()

    def recvSignalData(self):
        threadSaveData = Thread(target=self.recvSignalDataThread)
        threadSaveData.setDaemon(True)
        threadSaveData.start()
    
    def recvSignalDataThread(self):
        self.timmerSession = QTimer()  # 创建定时器
        self.timmerSession.timeout.connect(self.recv_signal)
        self.timmerSession.start(10)

    def createWebEng(self):
        self.webView = QWebEngineView()
        self.webView.settings().setAttribute(
            QtWebEngineWidgets.QWebEngineSettings.JavascriptEnabled, True)
        self.webViewWidget = QWidget()
        channel = QWebChannel(self.webView.page())
        self.webView.page().setWebChannel(channel)
        self.python_bridge = JsBridge(self)
        channel.registerObject("context", self.python_bridge)
        # self.webViewlayout = QHBoxLayout()
        self.webViewlayout = QVBoxLayout()
        self.webViewlayout.setSpacing(0)
        self.webViewlayout.addWidget(self.webView)
        # # 调试工具
        html_path = QtCore.QUrl.fromLocalFile(
            QDir.currentPath() + "/mainPage/index.html")
        # html_path = QtCore.QUrl('http://localhost:8082')
        self.webView.setUrl(html_path)
        self.webViewWidget.setLayout(self.webViewlayout)
        self.content.addWidget(self.webViewWidget)
        self.webView.setContentsMargins(0, 0, 0, 0)
        self.webViewlayout.setContentsMargins(0, 0, 0, 0)
        self.python_bridge.responseSignal.emit('this is from serve')

    def openHtml(self, data):
        if data == 'timeSerise':
            return
        paradigms = os.listdir('./web-app')
        if data in paradigms:
            save_path_dir = QDir.currentPath() + "/data/" + data
            save_path_def = QDir.currentPath() + "/edfFile/" + data
            if not os.path.exists(save_path_dir):
                os.makedirs(save_path_dir)
            if not os.path.exists(save_path_def):
                os.makedirs(save_path_def)
            html_path = QtCore.QUrl.fromLocalFile(
                QDir.currentPath() + "/web-app/"+data+"/index.html")
            self.webView.setUrl(html_path)

    def initDevTools(self):
        if self.devToolsStatus == True:
            return
        self.devToolsStatus = True
        dev_view = QtWebEngineWidgets.QWebEngineView()
        self.webViewlayout.addWidget(dev_view)
        self.webView.page().setDevToolsPage(dev_view.page())

    def _sub_close(self, message):
            self.python_bridge.getFromServer.emit(
                json.dumps({"id": 0, "action": 'close-time-serise'}))
   
    # 阻抗计算
    def getImpendenceData(self, message):
        boardData = self.currentData
        if boardData.shape[0] == 0 or boardData.shape[1] == 0:
            return json.dumps(dict({"impedences": [], "railed": []}))
        channels = self.board.get_eeg_channels(int(self.boardId))
        boardData = boardData[1: len(channels)+1]
        railed = self.getRailedPercentage(boardData)
        meanData = np.array([np.mean(boardData, axis=1)]).T
        boardData -= meanData
        stdData = np.std(boardData, axis=1)
        impedences = [
            ((np.sqrt(2) * item * 1.0e-6 / 6.0e-9 - 2200) / 1000) for item in stdData
        ]
        impedences = ','.join([str(i) for i in impedences])
        return json.dumps(dict({"impedences": impedences, "railed": railed}))
    # 脱落检测计算
    def getRailedPercentage(self, boardData):
        railed = []
        for channel in range(len(boardData)):
            percetage = DataFilter.get_railed_percentage(boardData[channel], 24) * 100
            railed.append(percetage)
        railed = ','.join([str(i) for i in railed])
        return railed
        # 设置相关
   
    def homePage(self):
        html_path = QtCore.QUrl.fromLocalFile(
            QDir.currentPath() + "/mainPage/index.html")
        self.webView.setUrl(html_path)

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.closeTimeSeriseWindow()
        print('send close brain figure')
        return super().closeEvent(a0)

    def fullScreen(self, essage):
        self.showFullScreen()

    def exitFullScreen(self, message):
        self.showNormal()

    def openFileDialog(self, message):
        fileName, fileType = QFileDialog.getOpenFileName(self, "选取文件")
        return fileName

    # 添加 多个文件
    def openFilesDialog(self, message):
        fileNames, fileType = QFileDialog.getOpenFileNames(self, "选取文件")
        return fileNames
    # 选取文件夹

    def openDirectory(self, message):
        directory = QFileDialog.getExistingDirectory(None, "选取文件夹")
        return directory

    def startCustomParadigm(self, message):
        if message['data']['customIp'] == "":
            return
        try:
            self.SocketCustomClient = SocketCustomClient(self)
            self.SocketCustomClient.init(
                message['data']['customIp'], message['data']['customPort'])
            self.SocketCustomClient.start()
            return 'ok'
        except:
            return 'fail'
        return 'fail'

    def endCustomParadigm(self, message):
        self.endTaskSaveData(message)
        if self.SocketCustomClient != None:
            self.SocketCustomClient.end()
            self.SocketCustomClient = None
        return 'ok'

    def getCustomInsertMarker(self, message):
        print(message)
        if message['action'] == 'start':
            self.startStream()
        
        if message['action'] == 'stop':
            self.stopStream()

        if message['action'] == 'trigger':
            self.trigger(int(message['data']))

    # 获取实时数据
    def getCurrentBoardData(self, message):
        print('send data')
        return self.currentData 
        

    def postTimeSeriseChannelShow(self, message):
        return 'ok'

    def filterBoardData(self, message):
        print('send filter data')
        self.conn2.send({"action": 'filter-show-data', "data": message})
    # 获取实时数据

    def getCurrentData(self, data):
        self.currentData = data
        

    def startImpendenceTest(self, message):
        self.startSession(message)

    def updateBadChannel(self, message):
        self.badChannel = message

    def endImpendenceTest(self, data):
        return 'ok'

    # 创建保存数据线程
    def startSession(self, message):
        print('send start session')
        self.message = message
        QTimer.singleShot(150, self.sendConfigStartSesssion)
    
    def sendConfigStartSesssion(self):
        self.conn2.send({'action': 'start-session', "data":self.message})

    def startStream(self, message):
        print('send start stream')
        self.conn2.send({'action': 'start-stream', "data":''})

    def stopStream(self, message):
        print('send stop stream')
        self.conn2.send({'action': 'stop-stream', "data":''})


    def stopSession(self, message):
        print('send stop session')
        self.conn2.send({'action': 'stop-session', "data":''})

    def trigger(self, number):
        print('send trigger')
        self.conn2.send({'action': 'stop-session', "data":number})


    def openTimeSeriseWindow(self, message):
        print('send open time serise', message)
        self.conn2.send({'action': 'open-window', "data":message})

    
    def closeTimeSeriseWindow(self):
        print('send hide time serise window')
        self.conn2.send({'action': 'close-window', "data":'1'})

        
    def endTaskSaveData(self, message):
        print('get file name')
        self.conn2.send({'action': 'end-task', "data":''})

    def getTaskEndFile(self, message):
        print('message', message)

    def get_Signal(self, conn2 ):
        self.conn2 = conn2

    def recv_signal(self):
        # if self.conn2 == None:
        #     return
        # res = self.conn2.recv()
        # if res['action'] == 'current-data':
        #     self.getCurrentBoardData(res['data'])
        #     return
            
        # if res['action'] == 'current-file':
        #     self.getTaskEndFile(res['data'])
        #     return
        return


def MainWindowFunc(conn2):
    app = QApplication(sys.argv)
    m = MainWindow()
    m.get_Signal(conn2)
    m.show()
    sys.exit(app.exec_())


def brainWindowFunc(conn1):
    app = QApplication(sys.argv)
    m = BrainWindow()
    m.get_Signal(conn1)
    sys.exit(app.exec_())

def main():
    conn1, conn2 = Pipe()
    p = Process(target=MainWindowFunc, args=(conn1,))
    p.start()
    p2 = Process(target=brainWindowFunc, args=(conn2,))
    p2.start()

if __name__ == '__main__':
    main()
