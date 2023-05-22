from brainflow.data_filter import DataFilter, FilterTypes, WindowOperations, DetrendOperations, AggOperations, NoiseTypes
import brainflow
import numpy as np
import mne
import pywt
from scipy import signal
from scipy.linalg import eigh

class Processsing(object):
    def __init__(self):
        super(Processsing, self).__init__()
        self.name = 'processing'
        self.sampling_rate = 1000

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
    # 计算统计特征
    def extract_statistic_feature(epoch_signal):
        statistic_feature = []
        temp_feature = []

        for channel in range(epoch_signal.shape[0]):
            X_1 = np.mean(epoch_signal[channel, :])
            X_2 = np.std(epoch_signal[channel, :], ddof=1)
            X_3 = 0
            total_point = len(epoch_signal[channel, :])

            for point in range(total_point - 1):
                X_3 += abs(epoch_signal[channel, point + 1] - epoch_signal[channel, point]) / (total_point - 1)

            X_4 = X_3 / X_2
            X_5 = 0

            for point in range(total_point - 2):
                X_5 += abs(epoch_signal[channel, point + 2] - epoch_signal[channel, point]) / (total_point - 2)

            X_6 = X_5 / X_2
            X_1_6 = [X_1, X_2, X_3, X_4, X_5, X_6]
            statistic_feature.extend(X_1_6)

            abs_X_1 = abs(X_1)
            temp_feature.append(abs_X_1)

        statistic_feature = np.array(statistic_feature)
        temp_feature = np.array(temp_feature)

        return statistic_feature
    
    # DE 特征
    def extract_DE_new(epoch_std, Fs):
        time_sec = 1 * Fs
        NFFT = 2**np.ceil(np.log2(time_sec)).astype(int)
        f = Fs/2 * np.linspace(0, 1, NFFT//2)

        de = np.zeros((epoch_std.shape[0], 5))  # 存储 DE 特征的数组
        for channel in range(epoch_std.shape[0]):
            for section in range(epoch_std.shape[1] // time_sec):
                window = np.hanning(time_sec)
                section_data = epoch_std[channel, section*time_sec:(section+1)*time_sec]
                Pxx = np.abs(np.fft.fft(section_data * window, NFFT))
                section_de = band_DE(Pxx, f)
                de[section, :] = np.mean(section_de, axis=0)

        diff_entropy = de.flatten()  # 将 de 数组展平成一维数组

        rasm_channel = RASM(de)
        rasm_feature = rasm_channel.flatten()

        return diff_entropy, rasm_feature
    def  eeg_spatial_pattern(eegData):
        # 计算协方差矩阵
        cov_matrix = np.cov(eegData)
        
        # 计算特征值和特征向量
        eigenvalues, eigenvectors = eigh(cov_matrix)
        
        # 排序特征值和特征向量
        sorted_indices = np.argsort(eigenvalues)[::-1]
        sorted_eigenvalues = eigenvalues[sorted_indices]
        sorted_eigenvectors = eigenvectors[:, sorted_indices]
        
        # 提取主成分
        eeg_pattern = sorted_eigenvectors[:]
        
        return eeg_pattern
    # 暂未开启
    def ica(self, data, icaExcludeChannel):
        data = data.transpose(1,0,2)
    
    def processing(self, files, channel, config, boardId):
        features = []
        features_label = []
        print(files, channel, config, boardId)
        for file in files:
            origin_data = np.loadtxt(file)
            origin_data = origin_data.T
            eeg_channel = brainflow.BoardShim.get_eeg_channels(int(boardId))
            eeg_data = origin_data[eeg_channel]
            badChannel = []
            labels = origin_data[-1]

            if 'detrend' in config['checkList']:
                if config['detrend']== 1:
                     for index in range(len(eeg_data)):
                         DataFilter.detrend(eeg_data[index], DetrendOperations.LINEAR.value)
            
            if 'wlt_denoising' in config['checkList']:
                wlt_denoising = int(config['wlt_denoising'])
                if wlt_denoising== 1 or wlt_denoising==2:
                    for index in range(len(eeg_data)):
                        DataFilter.remove_environmental_noise(
                            eeg_data[index], self.sampling_rate, NoiseTypes.FIFTY_AND_SIXTY)

                if wlt_denoising== 0  or wlt_denoising==2:
                    for index in range(len(eeg_data)):
                        item = eeg_data[index]
                        coeffs = pywt.wavedec(item, 'db4', level=4)
                        threshold = np.sqrt(2 * np.log(len(origin_data)))
                        thresholded_coeffs = [pywt.threshold(c, threshold, mode='soft') for c in coeffs]
                        reconstructed_signal = pywt.waverec(thresholded_coeffs, 'db4')
                        eeg_data[index] = reconstructed_signal[0: len(eeg_data[index])]

            if 'filter' in config['checkList']:
                 for index in range(len(eeg_data)):
                    DataFilter.perform_bandpass(eeg_data[index], self.sampling_rate, config['low'], config['high'], 2,
                                                    FilterTypes.BUTTERWORTH, ripple=0)

            if 'badChannel' in config['checkList']:
                for i in range(len(channel)):
                    if channel[i] in config['badChannel']:
                        badChannel.append(i)

            if 'refrence' in config['checkList']:
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
            
            if 'sample' in config['checkList']:
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
                        sub_data = origin_data[:, index + int(self.sampling_rate * float(slice_trigger[label]['startTime']) ): index + int(self.sampling_rate * float(slice_trigger[label]['endTime'] ))]
                        features.append(sub_data)
                        features_label.append(int(label))

            features = np.array(features)
            if 'segmentation' in config['checkList'] and 'sample' in config['checkList']:
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
                        
            if 'sampleDetrend' in config['checkList'] and 'sample' in config['checkList']:
                sample_data = []
                if int(config['sampleDetrend']) == 1:
                    for item in features:
                        detrend_mean = np.mean(item, axis=1)
                        item -= detrend_mean
                        sample_data.append(item)
                else:
                    for item in features:
                        detrend_mean = np.mean(features[:,:,int(float(item[config['sampleDetrendStart']]) * self.sampling_rate): int(float(item[config['sampleDetrendEnd']]) * self.sampling_rate)], axis=1)
                        item -= detrend_mean
                        sample_data.append(item)
                features = sample_data
            features = np.array(features)

            if 'sample_filter' in config['checkList'] and 'sample' in config['checkList']:
                 for item in range(len(features)):
                    data = features[item]
                    for index in range(len(data)):
                        DataFilter.perform_bandpass(data[index], self.sampling_rate, config['samplelow'], config['samplehigh'], 2,
                                                                FilterTypes.BUTTERWORTH, ripple= 0)
                        
            if 'down_sample' in config['checkList']:
                if 'sample' in config['checkList']:
                    down_sample_data = np.zeros((len(features), len(features[0]), int(config['downSample'] * len(features[0, 0]) / self.sampling_rate)))
                    for i in range(len(features)):
                        for j in range(len(features[0])):
                            down_sample_data[i, j] = signal.resample(features[i, j], int(config['downSample'] * len(features[i, j]) / self.sampling_rate))
                else: 
                    down_sample_data = np.zeros((len(features),  int(config['downSample']* len(features[0]) / self.sampling_rate)))
                    for i in range(len(features)):
                        down_sample_data[i] = signal.resample(features[i], int(config['downSample'] * len(features[i]) / self.sampling_rate))

                features = down_sample_data
            
        print(np.array(features).shape, features_label)

        characteristicWaveData = []
        if 'characteristicWave' in config['feature']['checkList']:
            if 'down_sample_data' in config['checkList']:
                sampling_rate = int(config['downSample'])
                
            if 'sample' in config['checkList']:
                new_feature = np.zeros((len(features), len(features[0]),len(config['feature']['characteristicWave']), len(features[0][0])))
                for item in range(len(features)):
                    for channel in range(features[0]):
                        single_features = features[item, channel]
                        for wave_index in range(len(config['feature']['characteristicWave'])):
                            wave = config['feature']['characteristicWave'][wave_index]
                            wave_data =  DataFilter.perform_bandpass(single_features, sampling_rate, wave[0], wave[1], 2,
                                                    FilterTypes.BUTTERWORTH, ripple=0)
                            new_feature[item, channel, wave_index] = wave_data
            else:
                new_feature = np.zeros((len(features), len(config['feature']['characteristicWave']), len(features[0])))
                for channel in range(features[0]):
                    single_features = features[item, channel]
                    for wave_index in range(len(config['feature']['characteristicWave'])):
                        wave = config['feature']['characteristicWave'][wave_index]
                        wave_data =  DataFilter.perform_bandpass(single_features, sampling_rate, wave[0], wave[1], 2,
                                                FilterTypes.BUTTERWORTH, ripple=0)
                        new_feature[item, channel, wave_index] = wave_data
            characteristicWaveData = new_feature
        print(characteristicWaveData.shape)
        spatialPattern = []
        if 'spatialPattern' in config['feature']['checkList']:
            print('spatialPattern')

        if 'psd' in config['feature']['checkList']:
            print('psd')
        
        if 'DE' in config['feature']['checkList']:
            print('DE')
        
        if 'PLV' in config['feature']['checkList']:
            print('PLV')
        
        if 'statistic' in config['feature']['checkList']:
            print('statistic')

        if config['createScript'] == '1':
            self.createScript(files, channel, config, boardId, './demo-script.py')
    
    def createScript(self, files, channel, config, boardId, fileName):
        print('this is create script')
        script1 = f"""
import numpy as np
import mne
from brainflow.data_filter import DataFilter, FilterTypes, WindowOperations, DetrendOperations, AggOperations, NoiseTypes
import brainflow
import pywt
from scipy import signal

files = {files}
channel = {channel}
config = {config}
boardId = {boardId}
sampling_rate = {self.sampling_rate}

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
        """
        script2 = """"""
        if 'detrend' in config['checkList']:
            script2 = """
        # 对一维信号进行相关基线处理
        for index in range(len(eeg_data)):
            DataFilter.detrend(eeg_data[index], DetrendOperations.LINEAR.value)

                """

        script3 = """"""
        if 'wlt_denoising' in config['checkList']:
            script3 = """
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
        """

        script4 = """"""
        if 'filter' in config['checkList']:
            script4 = """
        # 对一维信号进行滤波处理
        for index in range(len(eeg_data)):
            DataFilter.perform_bandpass(eeg_data[index], sampling_rate, config['low'], config['high'], 2,
                                            FilterTypes.BUTTERWORTH, ripple= 0)"""

        script5 = """"""
        if 'badChannel' in config['checkList']:
            script5 = """
            # 选择相关坏导
        for i in range(len(channel)):
            if channel[i] in config['badChannel']:
                badChannel.append(i)
        """

        script6 = """"""
        if 'refrence' in config['checkList']:
            script6 = f"""
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
        
        """

        script7 = """"""
        if 'sample' in config['checkList']:
            script7 = """
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
        
        """

        scriptSegment = """"""
        if 'segmentation' in config['checkList'] and 'sample' in config['checkList']:
            scriptSegment = """
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
        for item in range(len(features)):
            data = features[item]
            for index in range(len(data)):
                DataFilter.perform_bandpass(data[index], sampling_rate, config['samplelow'], config['samplehigh'], 2,
                                                                FilterTypes.BUTTERWORTH, ripple= 0)
        """

        script10 = """"""
        if 'down_sample' in config['checkList']:
            if 'sample' in config['checkList']:
                script10 = """
        # 降采样
        down_sample_data = np.zeros((len(features), len(features[0]), int(config['downSample'] * len(features[0, 0]) / sampling_rate)))
        for i in range(len(features)):
            for j in range(len(features[0])):
                down_sample_data[i, j] = signal.resample(features[i, j], int(config['downSample'] * len(features[i, j]) / sampling_rate))
                """
            else: 
                script10 = """
        # 降采样
        down_sample_data = np.zeros((len(features),  int(config['downSample']* len(features[0]) / sampling_rate)))
        for i in range(len(features)):
            down_sample_data[i] = signal.resample(features[i], int(config['downSample'] * len(features[i]) / sampling_rate))

                """

        script = script1 + script2 + script3 + script4 + script5 + \
                script6 + script7 + scriptSegment + script8 + script9 + script10
        filename = fileName # 指定保存的文件名


            # 打开文件并写入脚本内容
        with open(filename, "w") as file:
                file.write(script)
        file.close()
