import numpy as np 
import datetime
import time 
import mne
from SaveData import EEGSAVEDATA
from config import MindBridge
from brainflow import BoardShim, data_filter, DetrendOperations
class ConvertFileFormat(object):
    def __init__(self):
        super(ConvertFileFormat, self).__init__()
        self.sampling_rate = 1000
        self.boardId = 5
        self.channels = []
    def toTXT(self, fileName, savePath):
        self.getChannelsByFile(fileName)
        savePathTxt = ''
        if savePath:
            fileName = fileName.split('/')
            savePathTxt = savePath+ '/'+fileName[len(fileName) -1]
        else:
            savePathTxt = fileName
        self.writeFileOpenbciFile(fileName,savePathTxt.replace('.csv', '.txt'), self.channels, self.sampling_rate)
        return 'ok'
    
    def getChannelsByFile(self, fileName):
        data = np.loadtxt(fileName).T
        if len(data) == 24:
            self.boardId = 5
        elif len(data) == 32:
            self.boardId = 516
        elif len(data) == 48:
            self.boardId = 532
        elif len(data) == 80:
            self.boardId = 564
        else:
            self.boardId = 520
        mindBridge = MindBridge()
        channels = []
        if str(self.boardId) == '5':
            channels = mindBridge.channelImpedences["8"]
        elif str(self.boardId) == '516':
            channels = mindBridge.channelImpedences["16"]
        elif str(self.boardId) == '520':
            channels = mindBridge.channelImpedences["20"]
        elif str(self.boardId) == '532':
            channels = mindBridge.channelImpedences["32"]
        else:
            channels = mindBridge.channelImpedences["64"]
        self.channels = channels

    def toEDF(self, fileName, otherInfo, savePath):
        self.getChannelsByFile(fileName)
        data = np.loadtxt(fileName).T
        channle = BoardShim.get_eeg_channels(self.boardId)
        marker = -1
        markerData = data[marker]
        for cha in channle:
            data[cha] = data[cha]
        data = data[channle].T
        data = np.concatenate((data, np.array([markerData]).T), axis=1)
        saveData = EEGSAVEDATA()
        fileName = fileName.replace('.csv', '.bdf') 
        channels = np.array(self.channels).copy().tolist()
        channels.append('trigger')
        print('======================')
        print(data.shape, np.array(channels).shape, channels)
        print('======================')

        if savePath:
            fileName = fileName.split('/')
            path = savePath+ '/'+fileName[len(fileName) -1]
            saveData.saveFile(path, data, channels, self.sampling_rate, otherInfo)
        else:
            saveData.saveFile(fileName, data, channels, self.sampling_rate, otherInfo)
        return 'ok'

    def toMNE(self, fileName, savePath):
        data = np.loadtxt(fileName).T
        self.getChannelsByFile(fileName)
        for i in BoardShim.get_eeg_channels(self.boardId):
            # data_filter.DataFilter.detrend(data[i], DetrendOperations.NO_DETREND.value)
            data[i] = data[i] / 1000000
        channels = ['index']
        otherLabels = ['Accel Channel 0','Accel Channel 1','Accel Channel 2', 'end', 'Other1', 'Other2', 'Other3', 'other4', 'other5', 'other6', 'other7', 'other8', 'other9', 'time', 'stim']
        channels_1 = [self.channels[i] for i in range(len(self.channels))]
        channels.extend(channels_1)
        channels.extend(otherLabels)
        ch_types = ['misc']
        ch_types_1 = ['eeg' for i in range(len(self.channels))]
        otherLabels_type = ['misc','misc','misc', 'misc', 'misc', 'misc', 'misc', 'misc', 'misc', 'misc', 'misc', 'misc', 'misc', 'misc', 'stim']
        ch_types.extend(ch_types_1)
        ch_types.extend(otherLabels_type)
        info = mne.create_info(ch_names=channels, sfreq=self.sampling_rate, ch_types=ch_types, verbose=False)
        mne_data = mne.io.RawArray(data, info, verbose=False)
        fileName = fileName.replace('.csv', '.fif')
        if savePath:
            fileName = fileName.split('/')
            print(savePath+ '/'+fileName[len(fileName) -1])
            mne_data.save(savePath+ '/'+fileName[len(fileName) -1])
        else:
            mne_data.save(fileName, overwrite=True)
        return 'ok'
    def textCreate(self,save_path, channels,sample_rate ):
        file = open(save_path, 'w')
        file.write("%OpenBCI Raw EEG Data\n")   
        file.write("%Number of channels = "+str(len(channels))+"\n")   
        file.write("%Sample Rate = "+str(sample_rate)+" Hz\n")   
        file.write("%Board = OpenBCI_GUI$OpenBCI_GUI$BoardCytonWifi"+str(self.boardId).replace('5', '')+"\n")   
 
        str_h = "Sample Index," 
        str_channels = ""
        for i in range(len(channels)):
            str_channels += "EXG Channel " + str(i) + ","
        str_other = "Accel Channel 0, Accel Channel 1, Accel Channel 2, Other, Other, Other, Other, Other, Other, Other, Analog Channel 0, Analog Channel 1, Analog Channel 2, Timestamp, Other, Timestamp (Formatted)\n"
        str_channels_header= str_h + str_channels + str_other
        file.write(str_channels_header)
        file.close()

    def writeFileOpenbciFile(self, file_name, save_path, channels, sampling_rate):
        timeStampFormat = []
        data = np.loadtxt(file_name)
        data[:, -12] = 0
        data = data.T
        for item in data[-3]:
            time_now = datetime.datetime.fromtimestamp(item)
            time_string = time_now.strftime("%Y-%m-%d %H:%M:%S")
            time_string += str(format(item%1, ".3f"))
            timeStampFormat.append(time_string)
        data_new = np.concatenate((data, np.array([timeStampFormat])), axis=0)
        self.textCreate(save_path,channels, sampling_rate)
        file = open(save_path, 'a+')
        time.sleep(1)
        np.savetxt(file, data_new.T, delimiter=',', fmt="%s")
        file.close()