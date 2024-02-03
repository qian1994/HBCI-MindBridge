from realtimeFigure import RealTimeFigure
import os
import sys
import json
import time
import datetime
import numpy as np
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import QCoreApplication, QStandardPaths
from brainflow.board_shim import BoardShim
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
import multiprocessing.connection as mp_conn
import multiprocessing
import signal
import requests
conn1, conn2 = Pipe()
sub_window = None
app = None

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
        screenRect = app.primaryScreen().geometry().getRect()
        self.width = screenRect[2] - screenRect[0]
        self.height = screenRect[3] - screenRect[1]
        self.resize(1200, 800)
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
        self.processing = None
        self.conn2 = None
        recive_data = Thread(target=self.recv_signal)
        recive_data.setDaemon(True)
        recive_data.start()
        self.currentData = []
        self.paradigms = None
        self.message = None
        self.taskEndData = None

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
            QDir.currentPath() + "/web-app/app/index.html")
        # html_path = QtCore.QUrl('http://localhost:8082/')
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
        boardData = self.getCurrent()
        if boardData.shape[0] == 0 or boardData.shape[1] == 0:
            return json.dumps(dict({"impedences": [], "railed": []}))
        railed = self.getRailedPercentage(boardData)
        meanData = np.array([np.mean(boardData, axis=1)]).T
        boardData -= meanData
        stdData = np.std(boardData, axis=1)
        impedences = [
            ((np.sqrt(2) * item * 1.0e-6 / 6.0e-9) / 1000) for item in stdData
        ]
        impedences = ','.join([str(i) for i in impedences])
        return json.dumps(dict({"impedences": impedences, "railed": railed}))
    # 脱落检测计算

    def getRailedPercentage(self, boardData):
        railed = []
        for channel in range(len(boardData)):
            percetage = DataFilter.get_railed_percentage(
                boardData[channel], 24)
            railed.append(percetage)
        railed = ','.join([str(i) for i in railed])
        return railed
        # 设置相关

    def homePage(self):
        html_path = QtCore.QUrl.fromLocalFile(
            QDir.currentPath() + "/web-app/app/index.html")
        self.webView.setUrl(html_path)

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.conn2.send({"action": 'close-app', "data": ''})
        time.sleep(0.01)
        os.kill(sub_window.pid, signal.SIGTERM)
        sys.exit(0)

    def showFiguresWidget(self, message):
        data = message['data']
        if 'wave' in data:
            self.conn2.send({'action': 'toggle-wave', "data": data['wave']})

        if 'fft' in data:
            self.conn2.send({'action': 'toggle-fft', "data": data['fft']})

        if 'headplot' in data:
            self.conn2.send({'action': 'toggle-headplot',
                            "data": data['headplot']})

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
            return 'fail'
        try:
            self.SocketCustomClient = SocketCustomClient(self)
            self.SocketCustomClient.init(
                message['data']['customIp'], message['data']['customPort'])
            self.SocketCustomClient.start()
            return 'ok'
        except:
            return 'fail'

    def endCustomParadigm(self, message):
        self.conn2.send({'action': 'task-end-file-custom', 'data': ''})
        if self.SocketCustomClient != None:
            self.SocketCustomClient.stop()
            self.SocketCustomClient = None
        return 'ok'

    def getCustomInsertMarker(self, message):
        if message['action'] == 'start':
            self.startStream()

        if message['action'] == 'stop':
            self.stopStream()

        if message['action'] == 'trigger':
            self.trigger(int(message['data']))

    def postTimeSeriseChannelShow(self, message):
        return 'ok'

    def filterBoardData(self, message):
        print('send filter data')
        self.conn2.send({"action": 'filter-show-data', "data": message})
    # 获取实时数据

    def startImpendenceTest(self, message):
        url = 'http://' + message['data']['ip'] + '/impedance'
        post_data = dict({})
        post_data['channel'] = '9'
        res = requests.post(url, data=json.dumps(post_data))
        if res.status_code == 200:
            self.startSession(message)
        self.startSession(message)

    def updateBadChannel(self, message):
        self.badChannel = message['bad-channel']

    def endImpendenceTest(self, message):
        url = 'http://' + message['data']['ip'] + '/command'
        post_data = dict({})
        post_data['command'] = 'reset'
        res = requests.post(url, data=json.dumps(post_data))
        if res.status_code == 200:
            return 'ok'
        return 'ok'

    def getCurrent(self):
        self.conn2.send({'action': 'get-current-data', 'data': ''})
        return np.array(self.currentData)

    # 创建保存数据线程
    def startSession(self, message):
        self.message = message
        self.conn2.send({'action': 'start-session', 'data': message})

    def startStream(self, message):
        self.conn2.send({'action': 'start-stream', 'data': message})

    def stopStream(self, message):
        self.conn2.send({'action': 'stop-stream', 'data': message})

    def stopSession(self, message):
        self.conn2.send({'action': 'stop-session', 'data': message})

    def trigger(self, number):
        self.conn2.send({'action': 'trigger', 'data': number})

    def openTimeSeriseWindow(self, message):
        self.conn2.send({'action': 'open-window', 'data': message})

    def closeTimeSeriseWindow(self):
        self.conn2.send({'action': 'close-window', 'data': ''})

    def setBrainWaveScale(self, message):
        self.conn2.send({'action': 'set-brain-wave-scale',
                        'data': message['data']['scale']})

    def get_Signal(self, conn2):
        self.conn2 = conn2

    def endCustomParadigmByBrainflow(self, file):
        self.python_bridge.getFromServer.emit(
            json.dumps({"id": 0, "data": 'stop-custom-paradigm', 'file': file}))

    def recv_signal(self):
        while True:
            if self.conn2 == None:
                continue
            res = ""
            if mp_conn.wait([self.conn2], timeout=0):
                res = self.conn2.recv()
            if res == '':
                continue
            if res['action'] == 'current-data':
                self.currentData = np.array(res['data'])
                continue

            if res['action'] == 'task-end-file-custom':
                self.endCustomParadigmByBrainflow(res['data'])

def brainWindowFunc(conn2):
    app = QApplication(sys.argv)
    m = RealTimeFigure()
    m.get_Signal(conn2)
    m.showMinimized()
    sys.exit(app.exec_())

if __name__ == '__main__':
    multiprocessing.freeze_support()
    conn1, conn2 = Pipe()
    p2 = Process(target=brainWindowFunc, args=(conn1,))
    p2.start()
    sub_window = p2
    app = QApplication(sys.argv)
    m = MainWindow()
    m.get_Signal(conn2)
    m.show()
    sys.exit(app.exec_())
