
# -*- coding: utf-8 -*-
import numpy as np
import mne
from brainflow.data_filter import DataFilter, FilterTypes, WindowOperations, DetrendOperations, AggOperations, NoiseTypes
import brainflow
import pywt
features = []
files = ['aaa.csv', 'bbb.csf']
channel = ['1', '2', '3', '4', '5', '6', '7', '8']
config = {'checkList': ['detrend', 'wlt_denoising', 'trigger', 'badChannel', 'filter', 'refrence', 'sample', 'sample_filter', 'sample_detrend', 'down_sample'], 'detrend': 1, 'trigger': [], 'low': 0, 'high': 100, 'triggers': [{'startTime': 0, 'endTime': 0, 'trigger': 0}], 'samplelow': 0.5, 'samplehigh': 50, 'sampleDetrendStart': '', 'sampleDetrendEnd': '', 'sampleDetrend': '0', 'downSample': 200, 'outPutType': 'npy', 'ica': 0, 'productId': 5, 'badChannels': [], 'refrenceChannel': [], 'refrence': 0}
boardId = 5
sampling_rate = 1000
def get_features(files, channel, config, boardId):
    for file in files:
        origin_data = np.loadtxt(file)
        origin_data = origin_data.T
        eeg_channel = brainflow.BoardShim(int(config['productId']))
        eeg_data = origin_data[eeg_channel]
        badChannel = []
        labels = origin_data[-1]

        for channel in range(len(eeg_data)):
            DataFilter.detrend(
                eeg_data[channel], DetrendOperations.LINEAR.value)
            
        for channel in range(len(eeg_data)):
            DataFilter.remove_environmental_noise(eeg_data[channel], sampling_rate,NoiseTypes.FIFTY_AND_SIXTY)

        for channel in range(len(eeg_data)):
            DataFilter.perform_bandpass(eeg_data[channel], sampling_rate, config['low'], config['high'], 2,
                                            FilterTypes.BUTTERWORTH, ripple= 0)
        for i in range(len(channel)):
            if channel[i] in config['badChannel']:
                badChannel.append(i)
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
        data -= (refrence_data / count)

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
            
        for item in features:
            for it in range(len(features)):
                data = features[it]
                for channel in range(len(data)):
                    DataFilter.perform_bandpass(data[channel], sampling_rate,  config['samplelow'],  config['samplehigh'], 2,
                                                            FilterTypes.BUTTERWORTH, ripple= 0)
            
        features = features[:, ::sampling_rate/config['downSample']]
            