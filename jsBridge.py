import os
import json
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import *
from config import MindBridge
import requests
from convertFileFormat import ConvertFileFormat
from eeg_positions import get_elec_coords
from util import *
from processing import Processsing
import numpy as np
from result import Result

class JsBridge(QtCore.QObject):
    responseSignal = pyqtSignal(str)
    getFromServer = pyqtSignal(str)

    def __init__(self, parent=None):
        super(JsBridge, self).__init__(parent)
        self.responseSignal.connect(self.responseCall)
        self.getFromServer.connect(self.postFromServer)
        self.mainwindow = parent
        self.dir_path = ''

    @QtCore.pyqtSlot(str, result=str)
    def requestFromClient(self, message):
        message = json.loads(message)
        data = None

        if message["action"] == 'trigger':
            data = self.trigger(message)

        if message["action"] == "start-session":
            self.startSession(message)
            data = 'ok'

        if message['action'] == 'stop-session':
            data = self.stopSession(message)

        if message['action'] == 'start-stream':
            data = self.startStream(message)

        if message['action'] == 'stop-stream':
            data = self.stopStream(message)

        if message['action'] == 'choose-file':
            data = self.choosefile(message)

        if message['action'] == 'choose-dir':
            data = self.chooseDir(message)

        if message['action'] == 'impendence-data':
            data = self.impendenceData(message)

        if message['action'] == 'update-bad-channel':
            data = self.updateBadChannel(message)

        if message['action'] == 'set-brain-wave-scale':
            data = self.setBrainWaveScale(message)

        if message['action'] == 'start-impendence-test':
            data = self.startImpendenceTest(message)

        if message['action'] == 'end-impendence-test':
            data = self.endImpendenceTest(message)

        if message['action'] == 'get-config':
            data = self.postConfigToPage(message)

        if message['action'] == 'get-bad-channel':
            data = self.getBadChannel(message)

        if message['action'] == 'get-battery-proportion':
            data = self.getBatterVertage(message)

        if message['action'] == 'get-applications':
            data = self.getApplication(message)

        if message['action'] == 'open-html':
            data = self.openHtml(message)

        if message['action'] == 'go-to-home-page':
            data = self.goToHomePage(message)

        if message['action'] == 'open-time-serise-window':
            data = self.openTimeSeriseWindow(message)

        if message['action'] == 'close-time-serise-window':
            data = self.closeTimeSeriseWindow(message)

        if message['action'] == 'post-time-serise-channel-show':
            data = self.postTimeSeriseChannelShow(message)

        if message['action'] == 'get-time-serise-channel-show':
            data = self.getTimeSeriseChannelShow(message)
        
        if message['action'] == 'init-board':
            data = self.initTestBoard(message)

        if message['action'] == 'full-screen':
            data = self.fullScreen(message)

        if message['action'] == 'exit-full-screen':
            data = self.exitFullScreen(message)

        if message['action'] == 'init-dev-tools':
            data = self.initDevTools(message)

        if message['action'] == 'get-current-board-data':
            data=self.getCurrentBoardData(message)

        if message['action'] == 'open-file-dialog':
            data=self.openFileDialog(message)

        if message['action'] == 'open-dir-dialog':
            data=self.openDirectory(message)

        if message['action'] == 'filter-board-dta':
            data=self.filterBoardData(message)

        if message['action'] == 'convert-file-format':
            data=self.convertFileFormat(message)

        if message['action'] == 'get-eeg-electron-position':
            data=self.getEEGElectronPosition(message)

        if message['action'] == 'start-custom-paradigm':
            data=self.startCustomParadigm(message)

        if message['action'] == 'stop-custom-paradigm':
            print('action', message)
            data=self.endCustomParadigm(message)

        if message['action'] == 'get-file-labels-by-file-name':
            data=self.getFileLabelsByFileName(message)

        # eeg processing data
        if message['action'] == 'get-productId-by-file-name':
            data=self.getProductIdByFileName(message)

        if message['action'] == 'processing-origin-data':
            data=self.processingOriginData(message)

        if message['action'] == 'plot-origin-data':
            data=self.plotOriginData(message)

        if message['action'] == 'show-figures-widget':
            data=self.showFiguresWidget(message)

        # 视觉评估报告相关
        if message['action'] == 'get-report-file-list-ssvep':
            data = self.getReportFileListSSVEP(message)
        
        if message['action'] == 'create-file-reaport-ssvep':
            data = self.createFileReportSSVEP(message)
        
        if message['action'] == 'create-expriment-ssvep-result':
            data = self.createExprimentSsvepResult(message)

        if message['action'] == 'get-info-by-file-name':
            data = self.getInfoByFileName(message)

        if message['action'] == 'get-result-info-by-file-ssvep':
            data = self.getResultInfoByFileName(message)

        if message['action'] == 'draw-image-by-label-ssvep':
            data = self.drawImageByLabelSSVEP(message)
        
        if message['action'] == 'get-result-files':
            data = self.getResultFiles(message)
        
        if message['action'] == 'get-experiment-image':
            data = self.drawImage(message)

        if message['action'] == 'end-signal-trial-task':
            data = self.endSignalTrialTask(message)

        if message['action'] == 'open-params-window':
            data = self.openParamsWindow(message)

        if message['action'] == 'start-ssvep-task':
            data = self.startSsvepTask(message)

        if message['action'] == 'end-total-task':
            data = self.endTotalTask(message)
        
        if message['action'] == 'start-flash-task':
            data = self.startFlashTask(message)
        
        if message['action'] == 'get-models':
            data = self.getModels(message)
        message['data'] = data
        return self.responseSignal.emit(json.dumps(message))

    @ QtCore.pyqtSlot(str, result = str)
    def context(self, message):
        self.handleMessage(message)

    def responseCall(self, message):
        return message

    def postFromServer(self, message):
        return message

    def handleMessage(self, message):
        print(message)

    def startSession(self, message):
        data=self.mainwindow.startSession(message)
        return data

    def startStream(self, message):
        self.mainwindow.startStream(message)

    def stopStream(self, message):
        self.mainwindow.stopStream(message)
        return 'ok'

    def stopSession(self, message):
        self.mainwindow.stopSession(message)
        return 'ok'


    def choosefile(self, message):
        print('message')

    def chooseDir(self, message):
        print("message")


    def trigger(self, message):
        self.mainwindow.trigger(message['data'])
        return 'ok'

    def startImpendenceTest(self, message):
        data=self.mainwindow.startImpendenceTest(message)
        return data

    def endImpendenceTest(self, message):
        data=self.mainwindow.endImpendenceTest(message)
        return data

    def impendenceData(self, message):
        data=self.mainwindow.getImpendenceData(message)
        return data

    def postConfigToPage(self, message):
        mindBridge=MindBridge()
        return json.dumps(dict({"channels": mindBridge.channelImpedences, "products": mindBridge.products}))


    def getApplication(self, message):
        data=os.listdir('./web-app')
        return data

    def openHtml(self, message):
        self.mainwindow.openHtml(message['data'])
        return 'ok'

    def goToHomePage(self, message):
        self.mainwindow.homePage()
        return 'ok'

    def openTimeSeriseWindow(self, message):
        return self.mainwindow.openTimeSeriseWindow(message)


    def postTimeSeriseChannelShow(self, message):
        data=self.mainwindow.postTimeSeriseChannelShow(message)
        return data

    def closeTimeSeriseWindow(self, message):
        data=self.mainwindow.closeTimeSeriseWindow(message)
        return data

    def fullScreen(self, message):
        self.mainwindow.fullScreen(message)

    def exitFullScreen(self, message):
        self.mainwindow.exitFullScreen(message)

    def initDevTools(self, message):
        self.mainwindow.initDevTools()

    def getCurrentBoardData(self, message):
        return self.mainwindow.getCurrentBoardData(message)

    def getFileLabelsByFileName(self, message):
        filePath=message['data']
        files_label=[]
        for file in filePath:
            data=np.loadtxt(file)
            data=data.T
            label=data[-1]
            label=label[label != 0]
            files_label.extend(label.tolist())
        return files_label

    def getProductIdByFileName(self, message):
        filePath=message['data']
        productId= 5
        for file in filePath:
            data=np.loadtxt(file)
            data=data.T
            print(data.shape)
            if len(data) == 24:
                productId=5
            elif len(data) == 32:
                productId=516
            elif len(data) == 40:
                productId= 520
            elif len(data) == 48:
                productId=532
            elif len(data) == 80:
                productId=564
        return productId

    def processingOriginData(self, message):
        data=message['data']
        filePath=data['files']
        channels=data['channels']
        boardId=data['boardId']
        config=data['config']
        process=Processsing()
        res=process.processing(filePath, channels, config, boardId)
        return 'ok'

    def plotOriginData(self, message):
        data=message['data']
        filePath=data['file']
        channels=data['channels']
        boardId=data['boardId']
        process=Processsing()
        res=process.plotEEGOriginData(filePath, channels, boardId)
        return 'ok'
    def getBatterVertage(self, message):
        # try:
        #     result = requests.get(
        #         'http://'+message['data']['ip'] + ':80/BatteryVoltage', timeout=1, headers={'Connection': 'close'})
        #     res = json.loads(result.text)
        #     Battery = res['BatteryProportion']
        #     return int(Battery / 10)
        # except Exception as e:
        #     print(e)
        #     return 0
        return 100

    def initTestBoard(self, message):
        try:
            result=requests.get(
                'http://'+message['data']['ip'] + ':80/all', timeout = 3, headers = {'Connection': 'close'})
            res=json.loads(result.text)
            result.close()
            if result.status_code != 200:
                return "fail"
            else:
                if message['data']['productId'] == '5' and res['num_channels'] == 8:
                    return 'ok'
                if message['data']['productId'] == '516' and res['num_channels'] == 16:
                    return 'ok'
                if message['data']['productId'] == '532' and res['num_channels'] == 32:
                    return 'ok'
                if message['data']['productId'] == '564' and res['num_channels'] == 64:
                    return 'ok'
                if message['data']['productId'] == '520' and res['CHIP_CHANNEL_NUM'] == 6:
                    return 'ok'

                return 'fail'
        except Exception as e:
            print(e)
            return 'false'
        return 'ok'

    def openFileDialog(self, message):
        fileName=self.mainwindow.openFileDialog(message)
        return fileName

    def openFilesDialog(self, message):
        fileNames=self.mainwindow.openFilesDialog(message)
        return fileNames

    def openDirectory(self, message):
        dir=self.mainwindow.openDirectory(message)
        return dir

    # 实时数据进行滤波处理
    def filterBoardData(self, message):
        data=self.mainwindow.filterBoardData(message)
        return data
    
    def setBrainWaveScale(self, message):
        data = self.mainwindow.setBrainWaveScale(message)

    def getBadChannel(self, message):
        if self.mainwindow.badChannel == None:
            return []
        return self.mainwindow.badChannel

    def updateBadChannel(self, message):
        return self.mainwindow.updateBadChannel(message['data'])

    def getEEGElectronPosition(self, message):
        coords=get_elec_coords(system = '1010', as_mne_montage = False)
        data=[coords['label'].tolist(), coords['x'].tolist(),
                coords['y'].tolist()]
        return data


    def getTimeSeriseChannelShow(self, message):
        return []

    def convertFileFormat(self, message):
        savePath = message['data']['savePath']
        files = message['data']['fileList']
        fileFormat = ConvertFileFormat()
        for file in files:
            if message['data']['type'] == 'edf':
                fileFormat.toEDF(file, message['data'], savePath)
            elif message['data']['type'] == 'openbci':
                fileFormat.toTXT(file, savePath)
            elif message['data']['type'] == 'mne':
                fileFormat.toMNE(file, savePath)
        return 'ok'


    def startCustomParadigm(self, message):
        self.mainwindow.startCustomParadigm(message)

    def endCustomParadigm(self, message):
        print('message', message)
        self.mainwindow.endCustomParadigm(message)

    def showFiguresWidget(self, message):
        self.mainwindow.showFiguresWidget(message)

    # 视觉评估报告相关
    def getReportFileListSSVEP(self, message):
        res = Result()
        data = res.getReportFileListSSVEP(message)
        return data
    
    def createFileReportSSVEP(self, message):
        res = Result()
        data = res.createReport(message)
        return data
    
    def createExprimentSsvepResult(self, message):
        res = Result()
        data = res.createExprimentSsvepResult(message)
        return data
    
    def getInfoByFileName(self, message):
        res = Result()
        data = res.getInfoByFileName(message)
        return data
    
    def getResultInfoByFileName(self, message):
        fileName = message['data']['fileName']
        with open(fileName) as f:
            data = json.load(f)
        f.close()
        return data
    
    def drawImageByLabelSSVEP(self, message):
        res = Result()
        data = res.createImages(message)
        return data
    
    def getResultFiles(self, message):
        res = Result()
        data = res.readAllFiles()
        return ','.join(data)
    
    def drawImage(self, message):
        res = Result()
        data = res.drawImages(message)
        if len(data) > 0:
            return 'ok'
        return 'fail'
    
    def endSignalTrialTask(self, message):
        data = self.mainwindow.endSingleTask(message)
        return data
    
    def openParamsWindow(self, message):
        self.mainwindow.openParamsWindow(message)
    
    def startSsvepTask(self, message):
        data = self.mainwindow.startssvepTask(message)
        return data
    
    def endTotalTask(self, message):
        data = self.mainwindow.endTotalTask(message)
        return data
    
    def startFlashTask(self, message):
        self.mainwindow.startFlashTask(message['data'])

    def getModels(self, message):
        models = os.listdir('./assets')
        return models
    
    def flush(self):
        pass
