
import os
import sys
import json
import time
import random
import datetime
import csv
import numpy as np
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import QDir, QTimer, Qt, QObject
from PyQt5.QtWidgets import *
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, DetrendOperations
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

    # def saveBoardDataThread(self):
    #     while 1:
    #         time.sleep(5*60)
    #         if self.board == None:
    #             return
    #         if self.MindBridgefileName == '':
    #             return
    #         if not os.path.exists(self.MindBridgefileName):
    #             open(self.MindBridgefileName, 'w').close()

    #         data = self.board.get_board_data()
    #         with open(self.MindBridgefileName, 'a+') as file:
    #             DataFilter.write_file(data, self.MindBridgefileName, 'a+')
    #         file.close()
    # # 建立连接

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
        time.sleep(2)
        self.startStream(message)

    def startStream(self, message):
        time_now = datetime.datetime.now()
        time_string = time_now.strftime("%Y_%m_%d_%H_%M_%S")
        self.MindBridgefileName = self.dir_path+"/data/" + time_string + '.csv'
        if not os.path.exists(self.MindBridgefileName):
            open(self.MindBridgefileName, 'w').close()
        if self.board == None:
            return 'fail'
        if self.boartStatus == 'startStream':
            return 'ok'
        if self.board != None:
            self.board.start_stream(num_samples=45000,streamer_params = 'file://'+self.MindBridgefileName+':w')
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
        self.board.insert_marker(float(number))

    def deleteLastLine(self, filename):
        import csv
        # 读取CSV文件并存储数据
        with open(filename, 'r') as file:
            lines = list(csv.reader(file))

        # 检查文件是否为空
        if len(lines) == 0:
            print("CSV文件为空，无法删除最后一行。")
        else:
            # 删除最后一行数据
            lines.pop()

            # 将数据写回CSV文件
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(lines)
            print("已成功删除最后一行数据。")
            
    def endTaskSaveData(self, message):
        self.deleteLastLine(self.MindBridgefileName)
        data = self.board.get_board_data()
        DataFilter.write_file(data, self.MindBridgefileName, 'a')
        # dataNow = self.board.get_board_data()
        # data = np.loadtxt(self.MindBridgefileName).T
        # os.remove(self.MindBridgefileName)
        # data = np.ascontiguousarray(np.array(data))
        # if len(data) != 0:
        #     data = np.concatenate((data, dataNow), axis=1)
        # else:
        #     data = dataNow
        # datafilter = DataFilter()
        # datafilter.write_file(
        #     data=data, file_name=self.brainflow_file_name, file_mode='w')
        time_now = datetime.datetime.now()
        time_string = time_now.strftime("%Y_%m_%d_%H_%M_%S")
        self.MindBridgefileName = self.dir_path+"/data/" + time_string + '.csv'
        if not os.path.exists(self.MindBridgefileName):
            open(self.MindBridgefileName, 'w').close()
        return ''

    def postCurrentData(self, message):
        if self.conn1 == None:
            return
        data = self.getCurrentData()
        # self.conn1.send(data)

    def get_Signal(self, conn1):
        self.conn1 = conn1

