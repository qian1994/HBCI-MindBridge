
import numpy as np
import mne
from brainflow.data_filter import DataFilter, FilterTypes, WindowOperations, DetrendOperations, AggOperations, NoiseTypes
import brainflow
import pywt
from scipy import signal

files = ['C:/Users/admin/Desktop/mindBridgeSoftware/cnsc/data/svp1_2/FPVS_2size_2023_04_17_16_25_10.csv']
channel = ['FP1', 'FP2', 'T7', 'CZ', 'T8', 'O1', 'O2', 'OZ']
config = {'checkList': ['detrend', 'wlt_denoising', 'badChannel', 'filter', 'refrence', 'sample', 'segmentation', 'sample_filter', 'sample_detrend', 'down_sample'], 'detrend': '1', 'trigger': [], 'low': 0, 'high': 100, 'triggers': [{'startTime': 0, 'endTime': '10', 'trigger': -1}], 'segmentation': '5', 'selectTriggers': [], 'samplelow': 0.5, 'samplehigh': 50, 'sampleDetrendStart': '', 'sampleDetrendEnd': '', 'sampleDetrend': '0', 'downSample': 200, 'outPutType': 'npy', 'ica': 0, 'productId': 5, 'badChannel': ['OZ', 'O2'], 'refrenceChannel': [], 'refrence': '2', 'feature': {'checkList': ['characteristicWave', 'spatialPattern', 'psd', 'DE', 'statistic', 'PLV'], 'characteristicWave': [[1, 3], [4, 8]]}, 'createScript': '0', 'wlt_denoising': '2'}
boardId = 5
sampling_rate = 1000

def get_features(files, channel, config, boardId):
    features = []
    features_label = []
    for file in files:
        origin_data = np.loadtxt(file)
        origin_data = origin_data.T
        eeg_channel = brainflow.BoardShim.get_eeg_channels(int(boardId))
        eeg_data = origin_data[eeg_channel]
        badChannel = []
        labels = origin_data[-1]
        
        # 对一维信号进行相关基线处理
        for index in range(len(eeg_data)):
            DataFilter.detrend(eeg_data[index], DetrendOperations.LINEAR.value)

                
        # 对一维脑电进行相关去噪
        wlt_denoising = int(config['wlt_denoising'])
        if wlt_denoising== 1 or wlt_denoising==2:
            for index in range(len(eeg_data)):
                DataFilter.remove_environmental_noise(
                    eeg_data[index], sampling_rate, NoiseTypes.FIFTY_AND_SIXTY)

        if wlt_denoising== 0  or wlt_denoising==2:
            for channel_item in range(len(eeg_data)):
                item = eeg_data[channel_item]
                coeffs = pywt.wavedec(item, 'db4', level=4)
                threshold = np.sqrt(2 * np.log(len(origin_data)))
                thresholded_coeffs = [pywt.threshold(c, threshold, mode='soft') for c in coeffs]
                reconstructed_signal = pywt.waverec(thresholded_coeffs, 'db4')
                eeg_data[channel_item] = reconstructed_signal[0: len(eeg_data[channel_item])]
        
        # 对一维信号进行滤波处理
        for index in range(len(eeg_data)):
            DataFilter.perform_bandpass(eeg_data[index], sampling_rate, config['low'], config['high'], 2,
                                            FilterTypes.BUTTERWORTH, ripple= 0)
            # 选择相关坏导
        for i in range(len(channel)):
            if channel[i] in config['badChannel']:
                badChannel.append(i)
        
        # 参考处理
        refrence_data = []
        count = 0
        refrenceType = config['refrence']
        refrenceChannels = config['refrenceChannel']
        if int(refrenceType) == 2:
            for i in range(len(eeg_data)):
                if i in badChannel:
                    continue
                if len(refrence_data) == 0:
                    refrence_data = eeg_data[i]
                else:
                    refrence_data += eeg_data[i]
                count += 1
            eeg_data -= (refrence_data / count)
        elif int(refrenceType) == 1:
            for i in range(len(data)):
                if i in badChannel:
                    continue
                if i not in refrenceChannels:
                    continue
                if len(refrence_data) == 0:
                    refrence_data = eeg_data[i]
                else:
                    refrence_data += eeg_data[i]
                count += 1
            eeg_data -= (refrence_data / count)
        else:
            eeg_data -= eeg_data[refrenceChannels[0]]
        
        
        # 样本进行相关切片

        slice_trigger = dict({})
        for item in config['triggers']:
            if item['trigger'] == 0:
                continue
            slice_trigger[item['trigger']] = {'startTime': item['startTime'], 'endTime': item['endTime']}
        
        for index in range(len(labels)):
            label = labels[index]
            if label == 0:
                continue
            if label in slice_trigger:
                sub_data = origin_data[:, index + int(sampling_rate * float(slice_trigger[label]['startTime']) ): index + int(sampling_rate * float(slice_trigger[label]['endTime'] ))]
                features.append(sub_data)
                features_label.append(int(label))
        features = np.array(features)
        
        
        segmentation_data = []
        segmentation_label = []
        length = features.shape[2]
        for i in range(len(features)):
            for j in range(int(config['segmentation'])):
                sub_data = features[i,:, j * int(length / int(config['segmentation'])) : (j+1) * int(length / int(config['segmentation']))]
                segmentation_data.append(sub_data)
                segmentation_label.append(features_label[i])
        features_label = segmentation_label
        features = np.array(segmentation_data)
            
        # 对样本进行滤波处理
        for item in range(len(features)):
            data = features[item]
            for index in range(len(data)):
                DataFilter.perform_bandpass(data[index], sampling_rate, config['samplelow'], config['samplehigh'], 2,
                                                                FilterTypes.BUTTERWORTH, ripple= 0)
        
        # 降采样
        down_sample_data = np.zeros((len(features), len(features[0]), int(config['downSample'] * len(features[0, 0]) / sampling_rate)))
        for i in range(len(features)):
            for j in range(len(features[0])):
                down_sample_data[i, j] = signal.resample(features[i, j], int(config['downSample'] * len(features[i, j]) / sampling_rate))
                