
import os
import sys
import json
import time
import random
import datetime
import numpy as np
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import QDir, QTimer, Qt, QObject
from PyQt5.QtWidgets import *
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, DetrendOperations
from dataPorcessing import DataProcessing
import scipy.io as sio
from threading import Thread, current_thread
from multiprocessing import Process, Pipe, Queue, Manager

class BrainWindow(QObject):
    def __init__(self):
        super().__init__()
        self.stackData = []
        self.dir_path = '.'
        self.dir_path = self.dir_path.replace("\\", "/", 5)
        self.time = time.time()
        self.boartStatus = None
        self.boardId = 0
        self.board = None
        self.fileName = None
        self.brainflow_file_name = None
        self.timmer = None
        self.figure = None
        self.timmerSession = None
        self.ip_address = None
      
        self.MindBridgefileName = ''
        # self.conn1 = None

    def createFigures(self, message):
        channels = message['data']["channels"]
        self.startSession(message)

    def filterBoardData(self, message):
        # self.conn1.send({'action': 'filter', 'data': message})
        print('config')
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
        print('up reld time')
        # self.conn1.send({'action': 'update', "data": data })

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

    def endTaskSaveData(self, message):
        info = message['data']
        info['productId'] = int(info['productId'])
        info['sample_ratse'] = 1000
        currentTimeString = self.MindBridgefileName.replace(
            '.csv', '').replace('./data/', '')
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
        datafilter.write_file(
            data=data, file_name=self.brainflow_file_name, file_mode='w')
        info['data'] = data.tolist()
        sio.savemat(self.mat_file_name, info)
        time_now = datetime.datetime.now()
        time_string = time_now.strftime("%Y_%m_%d_%H_%M_%S")
        self.MindBridgefileName = self.dir_path+"/data/" + time_string + '.csv'
        if not os.path.exists(self.MindBridgefileName):
            open(self.MindBridgefileName, 'w').close()
        return self.mat_file_name, self.brainflow_file_name
    def postCurrentData(self, message):
        if self.conn1 == None:
            return
        data = self.getCurrentData()
        # self.conn1.send(data)

    def get_Signal(self, conn1):
        self.conn1 = conn1

# def brainWindowFunc(conn1):
#     app = QApplication(sys.argv)
#     m = BrainWindow()
#     m.conn1 = conn1
#     message = {'data': {'productId': '532', 'ip': '127.0.0.1', 'model': '0', 'low': 5, 'high': 45, 'filter': 0, 'order': 2,
#                             'channels': ['O1', 'C3', 'CP3', 'P3', 'P7', 'TP7', 'T7', 'A1', 'FT7', 'F7', 'FC3', 'F3', 'CZ', 'FCZ', 'FZ', 'FP1', 'FP2', 'F4', 'C4', 'FC4',
#                                          'F8', 'FT8', 'P8', 'A2', 'TP8', 'T8', 'CP4', 'P4', 'O2', 'CPZ', 'PZ', 'OZ']}}
#     m.createFigures(message)
#     sys.exit(app.exec_())
