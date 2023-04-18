from PyQt5.QtCore import QDir, QTimer, Qt
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtCore import QDir, QTimer, Qt
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWidgets import *
import random
import os

class Paradigms(QtCore.QObject):
    def __init__(self, parent=None):
        super(Paradigms, self).__init__(parent)
        self.main = parent
        self.timeDownCountNumber = 3
        self.timer1 = None
        self.timer2 = None
        self.imageWi = []
        self.count = 0
        self.targetIndex = 0
        self.totalTrial= 0
        self.trialNumber = 0
        self.lantency = 83
        self.width = parent.width
        self.height = parent.height
        self.flashViewlayout = parent.flashViewlayout
        self.trigger = parent.trigger
        self.endSingleTask = parent.endSingleTask
        
    def start(self, data):
        self.targetIndex = int(data["targetIndex"])
        self.totalTrial= int(data['totalTrial'])
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
        showIamges = self.flashImageArray(data)
        self.createImageWidgets(showIamges)
        self.flashViewlayout.addWidget(self.focusPoint)
        self.timeDownCount()


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
        self.main.endsingleTask()
        self.timer.stop()
        self.timeDownCountNumber = 3
        for i in reversed(range(self.flashViewlayout.count())): 
             self.flashViewlayout.itemAt(i).widget().setParent(None)
        self.imageWi = []
        self.count = 0
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
    
    def createImageWidgets(self,images, ):
        for i in range(len(images)):
            path = QDir.currentPath() + "/web" + images[i]
            image = QLabel()
            image.setContentsMargins(0,0,0,0)
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
        totalTrial= int(data['totalTrial'])
        targetImages = []
        objectImages = []
        if data['selectModel'] == '3color':
            targetImages = images[data['colorTarget']]
            objectImages = images[data['colorObject']]
        else:
            targetImages = images['o']
            objectImages = images['b']
        showImages = []
        for i in range(totalTrial* trialNumber):
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
        for item in os.listdir('./web/assets/'):
            imgDirPath = './web/assets/' + item
            imgs = dict({})
            for imgPath in os.listdir(imgDirPath):
                if '.m' in imgPath:
                    continue
                filesPath = [ "/assets/" +item+ '/'+ imgPath + '/' +path  for path in os.listdir(imgDirPath+'/' + imgPath)]
                imgs[imgPath] = filesPath
            
            imagesPathAll[item] = imgs
        self.imagePathAll = imagesPathAll
        return imagesPathAll[data]