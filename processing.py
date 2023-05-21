from brainflow.data_filter import DataFilter, FilterTypes, WindowOperations, DetrendOperations, AggOperations, NoiseTypes
import brainflow
import numpy as np
import mne
import pywt

class Processsing(object):
    def __init__(self):
        super(Processsing, self).__init__()
        self.name = 'processing'
        self.sampling_rate = 1000

    def detrend(self, data):
        for channel in range(len(data)):
            DataFilter.detrend(data[channel], DetrendOperations.LINEAR.value)

    def remove_environmental_noise(self, data):
        for channel in range(len(data)):
            DataFilter.remove_environmental_noise(
                data[channel], self.sampling_rate, NoiseTypes.FIFTY_AND_SIXTY)

    def filter(self, data, low, high):
        for channel in range(len(data)):
            DataFilter.perform_bandpass(data[channel], self.sampling_rate, low, high, 2,
                                                    FilterTypes.BUTTERWORTH, ripple=0)

    def refrence(self, data, badChannel, refrenceType, refrenceChannels):
        refrence_data = []
        count = 0
        if refrenceType == 2:
            for i in range(len(data)):
                if i in badChannel:
                    continue
                if len(refrence_data) == 0:
                    refrence_data = data[i]
                else:
                    refrence_data += data[i]
                count += 1
            data -= (refrence_data / count)
        elif refrenceType == 1:
            for i in range(len(data)):
                if i in badChannel:
                    continue
                if i not in refrenceChannels:
                    continue
                if len(refrence_data) == 0:
                    refrence_data = data[i]
                else:
                    refrence_data += data[i]
                count += 1
            data -= (refrence_data / count)
        else:
            
            data -= data[refrenceChannels[0]]
        return data 

    def sample(self, data, triggers, start, end):
        labels = data[-1]
        features= []
        features_label = []
        for i in range(len(labels)):
            label = labels[i]
            if label in triggers:
                subData = data[: , i+ start * self.sampling_rate: i+ self.sampling_rate * end]
                features.append(subData)
                features_label.append(label)
        return np.array(features), features_label
    
    def sample_filter(self, features, low, high):
        for item in range(len(features)):
            data = features[item]
            for channel in range(len(data)):
                DataFilter.perform_bandpass(data[channel], self.sampling_rate, low, high, 2,
                                                        FilterTypes.BUTTERWORTH, ripple= 0)

    def sample_detrend(self, features, start, end):
        feature_de = []
        for item in range(len(features)):
            data = features[item]
            detrend_feature = np.mean(data[:, :, start * self.sampling_rate: end * self.sampling_rate])
            data -= detrend_feature
            feature_de.append(data)
        return feature_de
    
    def down_sample(self, data, down_sample):
        DataFilter.perform_downsampling(data, self.sampling_rate, down_sample)
    
    def badChannel(self, data, badChannel):
        result = np.delete(data, badChannel, axis=1)
        return result

    def plotEEGOriginData(self, filePath, channels, boardId):
        data = np.loadtxt(filePath)
        data = data.T
        data = np.ascontiguousarray(np.array(data))
        eeg_channel = brainflow.BoardShim.get_eeg_channels(int(boardId))
        origin_data = data[eeg_channel]
        for channel in range(len(origin_data)):
            DataFilter.detrend(origin_data[channel], DetrendOperations.LINEAR.value)
            DataFilter.remove_environmental_noise(origin_data[channel], self.sampling_rate,NoiseTypes.FIFTY_AND_SIXTY)
            DataFilter.perform_bandpass(data[channel], self.sampling_rate, 0.5, 100, 2,
                                                        FilterTypes.BUTTERWORTH, ripple= 0)
        label = data[-1]
        origin_data = np.concatenate((origin_data, np.array([label])), axis=0)
        ch_types = ['eeg' for i in range(len(origin_data) - 1)]
        ch_types.append('misc')
        channels.append('trigger')
        info = mne.create_info(ch_names=channels, sfreq=1000, ch_types=ch_types, verbose=False)
        mne_data = mne.io.RawArray(origin_data, info)
        mne_data.plot(scalings=25, title=filePath)
        
    # 暂未开启
    def ica(self, data, icaExcludeChannel):
        data = data.transpose(1,0,2)
    
    def processing(self, files, channel, config, boardId):
        features = []
        for file in files:
            origin_data = np.loadtxt(file)
            origin_data = origin_data.T
            eeg_channel = brainflow.BoardShim(int(boardId))
            eeg_data = origin_data[eeg_channel]
            badChannel = []
            labels = origin_data[-1]

            if 'detrend' in config['checkList']:
                if config['detrend']== 1:
                    self.detrend(eeg_data)
            
            if 'wlt_denoising' in config['checkList']:
                if config['wlt_denoising']== 1 or config['wlt_denoising']==2:
                    self.remove_environmental_noise(eeg_data)
                if config['wlt_denoising']== 0  or config['wlt_denoising']==2:
                    for channel in range(len(eeg_data)):
                        item = eeg_data[channel]
                        coeffs = pywt.wavedec(item, 'db4', level=4)
                        threshold = np.sqrt(2 * np.log(len(origin_data)))
                        thresholded_coeffs = [pywt.threshold(c, threshold, mode='soft') for c in coeffs]
                        reconstructed_signal = pywt.waverec(thresholded_coeffs, 'db4')
                        eeg_data[channel] = reconstructed_signal

            if 'filter' in config['checkList']:
                self.filter(eeg_data, config['low'], config['high'])

            if 'badChannel' in config['checkList']:
                for i in range(len(channel)):
                    if channel[i] in config['badChannel']:
                        badChannel.append(i)

            if 'refrence' in config['checkList']:
                eeg_data = self.refrence(eeg_data, badChannel, config['refrence'],  config['refrenceChannel'])
            
            if 'sample' in config['checkList']:
                slice_trigger = dict({})
                for item in config['triggers']:
                    if item['trigger'] == 0:
                        continue
                    slice_trigger[item['trigger']] = {'startTime': item['startTime'], 'endTime': item['endTime']}
                
                for index in labels:
                    label = labels[index]
                    if label == 0:
                        continue
                    if label in slice_trigger:
                        sub_data = origin_data[:, index + self.sampling_rate * slice_trigger[label]['startTime'] : index + self.sampling_rate * slice_trigger[label]['endTime'] ]
                        features.append(sub_data)

            if 'sampleDetrend' in config['checkList'] and 'sample' in config['checkList']:
                sample_data = []
                if int(config['sampleDetrend']) == 1:
                    for item in features:
                        detrend_mean = np.mean(item, axis=1)
                        item -= detrend_mean
                        sample_data.append(item)
                else:
                    for item in features:
                        detrend_mean = np.mean(item[config['sampleDetrendStart'] * self.sampling_rate, config['sampleDetrendEnd']], axis=1)
                        item -= detrend_mean
                        sample_data.append(item)
                features = sample_data

            if 'sample_filter' in config['checkList'] and 'sample' in config['checkList']:
                for item in features:
                    self.sample_filter(item, config['samplelow'], config['samplehigh'])
                        
            if 'down_sample' in config['checkList']:
                if 'sample' in config['checkList']:
                    features = features[:, ::self.sampling_rate/config['downSample']]
                else: 
                    features = features[:,:, ::self.sampling_rate/config['downSample']]

    def createScript(self, files, channel, config, boardId, fileName):
        print('this is create script')
        script1 = f"""
import numpy as np
import mne
from brainflow.data_filter import DataFilter, FilterTypes, WindowOperations, DetrendOperations, AggOperations, NoiseTypes
import brainflow
import pywt
features = []
files = {files}
channel = {channel}
config = {config}
boardId = {boardId}
sampling_rate = {self.sampling_rate}
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
        # 对一维信号进行相关基线处理

        for channel in range(len(eeg_data)):
            DataFilter.detrend(
                eeg_data[channel], DetrendOperations.LINEAR.value)
                """

        script3 = """"""
        if 'wlt_denoising' in config['checkList']:
            script3 = """
        # 对一维脑电进行相关去噪
        for channel in range(len(eeg_data)):
            DataFilter.remove_environmental_noise(eeg_data[channel], sampling_rate,NoiseTypes.FIFTY_AND_SIXTY)"""

        script4 = """"""
        if 'filter' in config['checkList']:
            script4 = """
        # 对一维信号进行滤波处理
        for channel in range(len(eeg_data)):
            DataFilter.perform_bandpass(eeg_data[channel], sampling_rate, config['low'], config['high'], 2,
                                            FilterTypes.BUTTERWORTH, ripple= 0)"""

        script5 = """"""
        if 'badChannel' in config['checkList']:
            script5 = """
            # 选择相关坏导
        for i in range(len(channel)):
            if channel[i] in config['badChannel']:
                badChannel.append(i)"""

        script6 = """"""
        if 'refrence' in config['checkList']:
            script6 = f"""
        # 参考处理
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
        # 样本进行相关切片

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
        # 对样本数据进行相关基线校正
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
        # 对样本进行滤波处理
        for item in features:
            # sample_filter(item, config['samplelow'], config['samplehigh'])
            for it in range(len(features)):
                data = features[it]
                for channel in range(len(data)):
                    DataFilter.perform_bandpass(data[channel], sampling_rate,  config['samplelow'],  config['samplehigh'], 2,
                                                            FilterTypes.BUTTERWORTH, ripple= 0)
                """

        script10 = """"""
        if 'down_sample' in config['checkList']:
            if 'sample' in config['checkList']:
                script10 = """
        # 降采样
        features = features[:, ::sampling_rate/config['downSample']]
                """
            else: 
                script10 = """
        # 降采样
        features = features[:,:, ::sampling_rate/config['downSample']]
                """

        script = script1 + script2 + script3 + script4 + script5 + \
                script6 + script7 + script8 + script9 + script10
        print(script)
        filename = fileName # 指定保存的文件名

            # 打开文件并写入脚本内容
        with open(filename, "w") as file:
                file.write(script)