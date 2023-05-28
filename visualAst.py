from PyQt5.QtCore import QDir, QTimer, Qt
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtCore import QDir, QTimer, Qt
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWidgets import *
import random
import os
import json
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
class Ui_Paradigms(object):
    def setupUi(self, Paradigms):
        print('Ui_Paradigms widget')

class Paradigms(QWidget, Ui_Paradigms):
    def __init__(self):
        super(Paradigms, self).__init__()
        self.setupUi(self)
        self.timeDownCountNumber = 3
        self.timer1 = None
        self.timer2 = None
        self.imageWi = []
        self.count = 0
        self.targetIndex = 0
        self.totalTrial = 0
        self.trialNumber = 0
        self.lantency = 83
        self.setStyleSheet("background-color:rgb(128, 128, 128)")
        self.currentIndex = 0
        self.params = None
        self.state = None
    
    def init(self, jsbridge, width,height,trigger):
        if self.state == 'init':
            return
        self.flashViewlayout = QVBoxLayout()
        self.setLayout(self.flashViewlayout)
        self.flashViewlayout.setContentsMargins(0,0,0,0)
        self.python_bridge = jsbridge
        self.trigger = trigger
        self.width = width
        self.height = height
        self.resize(1200, 600)
        self.state = 'init'
        self.show()

    def startWindow(self,data, url=''):
        self.showFullScreen()
        if self.currentIndex > 0:
            QTimer.singleShot(500, self.sendData) 
            return
        # self.showFullScreen()
        self.webView = QWebEngineView()
        self.webView.settings().setAttribute(
            QtWebEngineWidgets.QWebEngineSettings.JavascriptEnabled, True)
        self.webViewWidget = QWidget()
        channel = QWebChannel(self.webView.page())
        self.webView.page().setWebChannel(channel)
        channel.registerObject("context", self.python_bridge)
        self.flashViewlayout.addWidget(self.webView)
        # 调试工具
        url = "file:///"+QDir.currentPath() + "/web-app/svp1_2/index.html#/motion"
        html_path = QtCore.QUrl(url)
        self.webView.setUrl(html_path)
        # dev_view = QtWebEngineWidgets.QWebEngineView()
        # self.flashViewlayout.addWidget(dev_view)
        # self.webView.page().setDevToolsPage(dev_view.page())
        self.currentIndex += 1
        self.params = data
        QTimer.singleShot(500, self.sendData) 

    def sendData(self):
        self.python_bridge.getFromServer.emit(json.dumps(self.params))

    def start(self,data):
        self.showFullScreen()
        self.targetIndex = int(data["targetIndex"])
        self.totalTrial = int(data['totalTrial'])
        self.trialNumber = int(data['trialNumber'])
        self.lantency =int(data['lantency'])
        if len(self.imageWi):
            self.timeDownCount()
            return
        self.focusPoint = QLabel()
        self.focusPoint.setContentsMargins(0,0,0,0)
        self.focusPoint.raise_()
        self.focusPoint.show()
        self.focusPoint.setFixedSize(100, 100)
        self.focusPoint.move(int(self.width/2-50), int(self.height/2-50))
        self.flashViewlayout.addChildWidget(self.focusPoint)
        showIamges = self.flashImageArray(data)
        self.createImageWidgets(showIamges)
        self.timeDownCount()
        self.show()

    def timeDownCount(self):
        if self.timeDownCountNumber <1:
            self.showFlash()
            return
        QTimer.singleShot(1000, self.timeDownCount) 
        self.focusPoint.setStyleSheet("QLabel{color:rgb(225,22,173);font-size:50px;font-weight:normal;font-family:Arial;}")
        self.focusPoint.setText(str(self.timeDownCountNumber))
        self.focusPoint.repaint()
        self.timeDownCountNumber -= 1
    
    def endTask(self):
        self.resize(self.width, self.height)
        self.move(0,0)
        self.timer.stop()
        self.timeDownCountNumber = 3
        for i in reversed(range(self.flashViewlayout.count())): 
             self.flashViewlayout.itemAt(i).widget().setParent(None)
        self.imageWi = []
        self.count = 0
        self.python_bridge.getFromServer.emit(
            json.dumps({"id": 0, "data": 'stop-flash'}))

    def doTimerTimeout(self): #定时中断相应
        if self.count == 0:
            self.trigger(-1)
        if self.count > len(self.imageWi)*2 -1:
            self.focusPoint.setFixedSize(0, 0)
            self.focusPoint.hide()
            self.focusPoint.destroy()
            self.endTask()
            return
        index = int(self.count/2)
        if self.count % 2 == 1:
            self.imageWi[index].hide()
        else:
            self.imageWi[index].show()
        if self.count % self.trialNumber== 0:
            self.trigger(1)
        if self.count % self.trialNumber == self.targetIndex:
            self.trigger(2)
        self.focusPoint.raise_()
        self.focusPoint.show()
        self.focusPoint.setFixedSize(10, 10)
        self.focusPoint.setStyleSheet("background-color:rgb(255, 0, 0)")
        self.focusPoint.move(int(self.width/2-5), int(self.height/2-5))
        self.count += 1

    def showFlash(self):
        self.focusPoint.raise_()
        self.focusPoint.show()
        self.focusPoint.setText('')
        self.focusPoint.setFixedSize(10, 10)
        self.focusPoint.setStyleSheet("background-color:rgb(255, 0, 0)")
        self.focusPoint.move(int(self.width/2-5), int(self.height/-5))
        self.timer=QTimer()  #创建定时器
        self.timer.setTimerType(Qt.PreciseTimer)
        self.timer.timeout.connect(self.doTimerTimeout)
        self.timer.start(self.lantency)  
    
    def createImageWidgets(self,images):
        for i in range(len(images)):
            path = QDir.currentPath()  + images[i]
            image = QLabel()
            image.setContentsMargins(0,0,0,0)
            image.setFixedSize(self.width, self.height)
            image.setStyleSheet("background-color:rgb(128, 0, 0)")
            image.move(0, 0)
            pix = QtGui.QPixmap(path)
            image.setFixedSize(self.width, self.height)
            image.setPixmap(pix)
            image.setScaledContents(True)
            image.hide()
            self.flashViewlayout.addWidget(image)
            self.imageWi.append(image)
    # 本地文件夹
    # 设置图片显示的顺序
    def flashImageArray(self,data):
        images = self.getImages(data['selectModel'])
        targetIndex =  int(data['targetIndex'])
        trialNumber = int(data['trialNumber'])
        totalTrial = int(data['totalTrial'])
        targetImages = []
        objectImages = []
        if data['selectModel'] == '3color':
            targetImages = images[data['colorTarget']]
            objectImages = images[data['colorObject']]
        else:
            targetImages = images['o']
            objectImages = images['b']
        showImages = []
        for i in range(totalTrial * trialNumber):
            if i % trialNumber == targetIndex:
                number = random.randint(0, len(targetImages)-1)
                imagePath = targetImages[number]
                showImages.append(imagePath)
                continue
            number = random.randint(0, len(objectImages)-1)
            imagePath = objectImages[number]
            showImages.append(imagePath)
        return showImages
    
    def getImages(self, data):
        imagesPathAll = dict({})
        for item in os.listdir('./assets/'):
            imgDirPath = './assets/' + item
            imgs = dict({})
            for imgPath in os.listdir(imgDirPath):
                if '.m' in imgPath:
                    continue
                filesPath = [ "/assets/" +item+ '/'+ imgPath + '/' +path  for path in os.listdir(imgDirPath+'/' + imgPath)]
                imgs[imgPath] = filesPath
            
            imagesPathAll[item] = imgs
        self.imagePathAll = imagesPathAll
        return imagesPathAll[data]

    def close(self) -> bool:
        self.state = None
        return super().close()