import os
import sys
import json
import time
import random
import datetime
import numpy as np
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtCore import QDir, QTimer, Qt, QObject
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from jsBridge import JsBridge
from signals import Signal
from brainflow.data_filter import DataFilter, FilterTypes, DetrendOperations
from dataPorcessing import DataProcessing
import scipy.io as sio
from startSocketClient import SocketCustomClient
from realtimeFigure import RealTimeFigure
from threading import Thread, current_thread

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stackData = []
        self.dir_path = '.'
        self.dir_path = self.dir_path.replace("\\", "/", 5)
        self.time = time.time()
        self.boartStatus = None
        self.setStyleSheet("background-color:rgb(128, 128, 128)")
        self.boardId = 0
        self.board = None
        self.fileName = None
        self.brainflow_file_name = None
        self.timmer = None
        self.webView = None
        self.webViewWidget = None
        self.webViewlayout = None
        self.widget = QWidget()
        self.figure = None
        self.timmerSession = None
        self.ip_address = None
        self.content = QHBoxLayout()
        self.content.setSpacing(0)
        self.widget.setLayout(self.content)
        self.setWindowTitle('MindBridge')
        screenRect = app.primaryScreen().geometry().getRect()
        self.width = screenRect[2] - screenRect[0]
        self.height = screenRect[3] - screenRect[1]
        self.resize(1200, 600)
        self.content.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.widget.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.widget)
        self.createWebEng()
        self._signal = Signal()
        self._signal._mainClose[str].connect(self._sub_close)
        self.devToolsStatus = None
        self.dataprocessing = DataProcessing()
        self.filterParams = dict({
            'high': 45,
            "low": 5,
            "order": 2,
            "filterType": 0,
        })
        self.badChannel = None
        self.SocketCustomClient = None
        self.MindBridgefileName = ''

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
        # html_path = QtCore.QUrl.fromLocalFile(
        #     QDir.currentPath() + "/mainPage/index.html")
        html_path = QtCore.QUrl('http://localhost:8082')
        self.webView.setUrl(html_path)
        self.webViewWidget.setLayout(self.webViewlayout)
        self.content.addWidget(self.webViewWidget)
        self.webView.setContentsMargins(0, 0, 0, 0)
        self.webViewlayout.setContentsMargins(0, 0, 0, 0)
        self.python_bridge.responseSignal.emit('this is from serve')


    def saveBoardDataThread(self):
        while 1:
            time.sleep(5*60)
            if self.board == None:
                return
            if self.MindBridgefileName == '':
                return
            if not os.path.exists(self.MindBridgefileName):
                open(self.MindBridgefileName, 'w').close()

            data = self.board.get_board_data()
            with open(self.MindBridgefileName, 'a+') as file:
                DataFilter.write_file(data, self.MindBridgefileName, 'a+')
            file.close()

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

    def createFigures(self, message):
        try:
            channels = message['data']["channels"]
            self.figure = RealTimeFigure()
            self.figure.setChannel(channels)
            self.figure.show()
            self.startSession(message)
            self.startTimeOutPrepareSession()
        except Exception as e:
            print(e)


    def closeTimeSeriseWindow(self):
        if self.figure != None:
            self.figure.close()
            self.figure = None

    def postTimeSeriseChannelShow(self, message):
        channels = message['data']
        self.figure.chooseShowChannel(channels)
        return 'ok'

    def showTimeSerise(self):
        self.timmerSession = QTimer()  # 创建定时器
        self.timmerSession.timeout.connect(self.updateRealTimePlot)
        self.timmerSession.start(40)

    def closeFigures(self):
        self.timmerSession.stop()
        self.timmerSession.killTimer(self.timmerSession.timerId())

    def startTimeOutPrepareSession(self):
        QTimer.singleShot(1000, self.timmerPrePareSession)

    def timmerPrePareSession(self):
        if self.board != None and self.board.is_prepared():
            self.startStream('')
            QTimer.singleShot(2000, self.showTimeSerise)

    def filterBoardData(self, message):
        data = message['data']
        self.filterParams['low'] = data['low']
        self.filterParams['high'] = data['high']
        self.filterParams['filterType'] = data['filter']
        self.filterParams['order'] = data['order']
    # 获取实时数据

    def getCurrentData(self):
        numSeconds = 22
        showSeconds = 5
        exg_channels = BoardShim.get_exg_channels(int(self.boardId))
        sampling_rate = BoardShim.get_sampling_rate(int(self.boardId))
        numPoints = numSeconds * sampling_rate
        showPoints = showSeconds * sampling_rate
        if self.boartStatus == 'startStream':
            boardData = self.board.get_current_board_data(numPoints)
            boardData = boardData[exg_channels]
            if boardData.shape[0] == 0 or boardData.shape[1] == 0:
                return []
            if boardData.shape[1] < showPoints:
                return boardData
            elif boardData.shape[1] > showPoints and boardData.shape[1] < numPoints:
                return boardData[:, boardData.shape[1]-showPoints:boardData.shape[1]]
            elif boardData.shape[1] == numPoints:
                return boardData[:, numPoints-showPoints:numPoints]
        return []

    def updateRealTimePlot(self):
        data = self.getCurrentData()
        if len(data) == '':
            return
        sampling_rate = BoardShim.get_sampling_rate(int(self.boardId))
        boardData = data.copy()
        boardData = self.dataprocessing.handleFilter(data, sampling_rate, self.filterParams['low'],
                                                     self.filterParams['high'], self.filterParams['order'], self.filterParams['filterType'])
        self.figure.update(boardData)

    def getRelTimeDectation(self, message):
        if self.boartStatus != 'startStream':
            return 'fail'
        numSeconds = 10
        sampleRate = self.board.get_sampling_rate(self.boardId)
        numPoints = numSeconds * sampleRate
        boardData = self.board.get_current_board_data(numPoints)
        boardData = boardData[self.board.get_eeg_channels(self.boardId)]

    def startImpendenceTest(self, message):
        try:
            if self.board != None:
                return 'ok'
            self.startSession(message)
        except:
            return 'fail'
        return 'ok'

    def updateBadChannel(self, message):
        self.badChannel = message

    def endImpendenceTest(self, data):
        # try:
        #     self.stopStream('')
        #     self.stopSession('')
        # except:
        # return 'fail'
        return 'ok'

    # 阻抗计算
    def getImpendenceData(self, data):
        numSeconds = 3
        if self.board.is_prepared():
            sampleRate = BoardShim.get_sampling_rate(int(self.boardId))
            numPoints = numSeconds * sampleRate
            boardData = self.board.get_current_board_data(numPoints)
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
        else:
            return json.dumps(dict({"impedences": [], "railed": []}))
    # 脱落检测计算

    def getRailedPercentage(self, boardData):
        railed = []
        for channel in range(len(boardData)):
            percetage = DataFilter.get_railed_percentage(boardData[channel], 24) * 100
            railed.append(percetage)
        railed = ','.join([str(i) for i in railed])
        return railed

    # 创建保存数据线程

    def saveBoardDataThread(self):
        while 1:
            time.sleep(5*60)
            if self.board == None:
                return
            if self.MindBridgefileName == '':
                return
            if not os.path.exists(self.MindBridgefileName):
                open(self.MindBridgefileName, 'w').close()

            data = self.board.get_board_data()
            with open(self.MindBridgefileName, 'a+') as file:
                DataFilter.write_file(data, self.MindBridgefileName, 'a+')
            file.close()
    # 建立连接

    def startSession(self, message):
        try:
            if self.boartStatus == 'startStream' or self.board != None:
                return 'ok'
            data = message['data']
            boardId = int(data["productId"])
            params = BrainFlowInputParams()
            params.ip_port = 9521 + random.randint(1, 100)
            params.ip_address = data['ip']
            if self.ip_address == params.ip_address and self.boardId == boardId:
                return 'ok'
            if self.board != None:
                self.board.release_all_sessions()
            self.board = BoardShim(int(boardId), params)
            self.board.prepare_session()
            self.boardId = boardId
            self.ip_address = params.ip_address
            self.startStream(message)
            time_now = datetime.datetime.now()
            time_string = time_now.strftime("%Y_%m_%d_%H_%M_%S")
            self.MindBridgefileName = self.dir_path+"/data/" + time_string + '.csv'
            if not os.path.exists(self.MindBridgefileName):
                open(self.MindBridgefileName, 'w').close()
            threadSaveData = Thread(target=self.saveBoardDataThread)
            threadSaveData.setDaemon(True)
            threadSaveData.start()
        except:
            return 'fail'
        return 'ok'

    def startStream(self, message):
        if self.board == None:
            return 'fail'
        if self.boartStatus == 'startStream':
            return 'ok'
        if self.board != None:
            self.board.start_stream()
            self.boartStatus = "startStream"
            return 'ok'
        return 'fail'

    def stopStream(self, message):
        try:
            self.board.stop_stream()
            self.boartStatus = 'stopStream'
        except:
            print('stop stream fail')
            return 'fail'
        return 'ok'

    def stopSession(self, message):
        try:
            if self.boartStatus == "startStream":
                self.board.stop_stream()
                self.boartStatus = 'stopStream'
            if self.board != None:
                self.board.release_all_sessions()
        except:
            return 'fail'
        return 'ok'

    def trigger(self, number):
        self.board.insert_marker(int(number))

    def endSingleTask(self, message):
        self.python_bridge.getFromServer.emit(
            json.dumps({"id": 0, "data": 'stop-flash'}))

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

    # 设置相关
    def homePage(self):
        # if self.boartStatus == "startStream":
        #     data = self.board.get_board_data()
        # self.stopStream('')
        # self.board.release_all_sessions()
        # self.boartStatus = 'none'
        html_path = QtCore.QUrl.fromLocalFile(
            QDir.currentPath() + "/mainPage/index.html")
        self.webView.setUrl(html_path)
        # if self.timmerSession != None:
        #     self.closeFigures()

    def openTimeSeriseWindow(self, message):
        try:
            self.createFigures(message)
        except:
            return 'fail'
        return 'ok'

    def closeEvent(self, a0: QtGui.QCloseEvent):
        if self.timmer != None:
            self.killTimer(self.timmer.timerId())
        self.closeTimeSeriseWindow()
    
        return super().closeEvent(a0)

    def fullScreen(self, essage):
        self.showFullScreen()

    def exitFullScreen(self, message):
        self.showNormal()

        
    def endTaskSaveData(self, message):
        info = message['data']
        info['productId'] = int(info['productId'])
        info['sample_rage'] = 1000
        currentTimeString = self.MindBridgefileName.replace('.csv', '').replace('./data/', '')
        self.brainflow_file_name = self.dir_path+"/data/" + \
            '/' + 'MindBridge_' + currentTimeString + '.csv'
        self.mat_file_name = self.dir_path+"/edfFile/" + \
            "/"+'MindBridge_' + currentTimeString + '.mat'
        dataNow = self.board.get_board_data()
        data = np.loadtxt(self.MindBridgefileName).T
        os.remove(self.MindBridgefileName) 
        data = np.ascontiguousarray(np.array(data))
        if len(data) != 0:
            data = np.concatenate((data, dataNow), axis=1)
        else:
            data = dataNow
        datafilter = DataFilter()
        datafilter.write_file(data=data, file_name=self.brainflow_file_name, file_mode='w')
        info['data']= data.tolist()
        sio.savemat(self.mat_file_name, info)
        if self.SocketCustomClient != None:
            self.SocketCustomClient.send(json.dumps({"filePath": self.brainflow_file_name}))
        time_now = datetime.datetime.now()
        time_string = time_now.strftime("%Y_%m_%d_%H_%M_%S")
        self.MindBridgefileName = self.dir_path+"/data/" + time_string + '.csv'
        if not os.path.exists(self.MindBridgefileName):
            open(self.MindBridgefileName, 'w').close()
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

    # 获取实时数据
    def getCurrentBoardData(self, message):
        data = message['data']
        second = data['second']
        if self.boartStatus == 'startStream':
            numpoint = second * self.board.get_sampling_rate(self.boardId)
            data = self.board.get_current_board_data(numpoint)
            channel = self.board.get_eeg_channels(self.boardId)
            data = data[channel]
            if len(data):
                return json.dumps(data.tolist())
        return "[]"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = MainWindow()
    m.show()
    sys.exit(app.exec_())
