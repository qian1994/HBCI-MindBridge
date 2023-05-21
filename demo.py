def createProcessingScript(file_Path, channel, config, boardid, sample_rate):
    script1 = f"""
# -*- coding: utf-8 -*-
import numpy as np
import mne
from brainflow.data_filter import DataFilter, FilterTypes, WindowOperations, DetrendOperations, AggOperations, NoiseTypes
import brainflow
import pywt
features = []
files = {file_Path}
channel = {channel}
config = {config}
boardId = {boardid}
sampling_rate = {sample_rate}
def get_features(files, channel, config, boardId):
    for file in files:
        origin_data = np.loadtxt(file)
        origin_data = origin_data.T
        eeg_channel = brainflow.BoardShim(int(config['productId']))
        eeg_data = origin_data[eeg_channel]
        badChannel = []
        labels = origin_data[-1]
        """
    script2 = """"""
    if 'detrend' in config['checkList']:
        script2 = """

        for channel in range(len(eeg_data)):
            DataFilter.detrend(
                eeg_data[channel], DetrendOperations.LINEAR.value)
            """

    script3 = """"""
    if 'wlt_denoising' in config['checkList']:
        script3 = """
        for channel in range(len(eeg_data)):
            DataFilter.remove_environmental_noise(eeg_data[channel], sampling_rate,NoiseTypes.FIFTY_AND_SIXTY)"""

    script4 = """"""
    if 'filter' in config['checkList']:
        script4 = """
        for channel in range(len(eeg_data)):
            DataFilter.perform_bandpass(eeg_data[channel], sampling_rate, config['low'], config['high'], 2,
                                            FilterTypes.BUTTERWORTH, ripple= 0)"""

    script5 = """"""
    if 'badChannel' in config['checkList']:
        script5 = """
        for i in range(len(channel)):
            if channel[i] in config['badChannel']:
                badChannel.append(i)"""

    script6 = """"""
    if 'refrence' in config['checkList']:
        script6 = f"""
        refrence_data = []
        count = 0
        for i in range(len(data)):
            if i in badChannel:
                continue
            if len(refrence_data) == 0:
                refrence_data = data[i]
            else:
                refrence_data += data[i]
            count +=1
        data -= (refrence_data / count)"""

    script7 = """"""
    if 'sample' in config['checkList']:
        script7 = """

        slice_trigger = dict()
        for item in config['triggers']:
            if item['trigger'] == 0:
                continue
            slice_trigger[item['trigger']] = {'startTime': item['startTime'], 'endTime': item['endTime']}
        
        for index in labels:
            label = labels[index]
            if label == 0:
                continue
            if label in slice_trigger:
                sub_data = origin_data[:, index + sampling_rate * slice_trigger[label]['startTime'] : index + sampling_rate * slice_trigger[label]['endTime'] ]
                features.append(sub_data)
            """

    script8 = """"""
    if 'sampleDetrend' in config['checkList'] and 'sample' in config['checkList']:
        script8 = """
        sample_data = []
        if int(config['sampleDetrend']) == 1:
            for item in features:
                detrend_mean = np.mean(item, axis=1)
                item -= detrend_mean
                sample_data.append(item)
        else:
            for item in features:
                detrend_mean = np.mean(item[config['sampleDetrendStart'] * sampling_rate, config['sampleDetrendEnd']], axis=1)
                item -= detrend_mean
                sample_data.append(item)
        features = sample_data
            """

    script9 = """"""
    if 'sample_filter' in config['checkList'] and 'sample' in config['checkList']:
            script9 = """
        for item in features:
            for it in range(len(features)):
                data = features[it]
                for channel in range(len(data)):
                    DataFilter.perform_bandpass(data[channel], sampling_rate,  config['samplelow'],  config['samplehigh'], 2,
                                                            FilterTypes.BUTTERWORTH, ripple= 0)
            """

    script10 = """"""
    if 'down_sample' in config['checkList']:
        if 'sample' in configs['checkList']:
            script10 = """
        features = features[:, ::sampling_rate/config['downSample']]
            """
        else: 
            script10 = """
        features = features[:,:, ::sampling_rate/config['downSample']]
            """

    script = script1 + script2 + script3 + script4 + script5 + \
            script6 + script7 + script8 + script9 + script10
    print(script)
    filename = "demo-script.py"  # 指定保存的文件名

        # 打开文件并写入脚本内容
    with open(filename, "w") as file:
            file.write(script)
    file.close()
    # 创建

def createFeatureScript(file):
     print('file')

def createDeepLearningScript(fileName):
     print('create DeepLearning script')
     
def createMechainLearningScript(file):
    print('createMechainLearningScript')

def createOnlineDetectionSystem(file):
    print('file')


files = ['aaa.csv', 'bbb.csf']
configs = {
        "checkList": ['detrend', 'wlt_denoising', 'trigger', 'badChannel','filter', 'refrence', 'sample','sample_filter','sample_detrend','down_sample'   ],
        "detrend": 1,
        "trigger": [],
        "low": 0,
        "high": 100,
        "triggers": [
          {
            "startTime": 0,
            "endTime": 0,
            "trigger": 0
          }
        ],
        "samplelow": 0.5,
        "samplehigh": 50,
        "sampleDetrendStart": '',
        "sampleDetrendEnd": '',
        "sampleDetrend": '0',
        "downSample": 200,
        "outPutType": 'npy',
        "ica": 0,
        "productId": 5,
        "badChannels": [],
        "refrenceChannel": [],
        "refrence": 0,
      }

channels = ['1', '2', '3', '4', '5', '6', '7', '8']
boardid = 5
sample_rate = 1000

createProcessingScript(files, channels, configs, boardid, sample_rate)