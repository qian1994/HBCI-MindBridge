from brainflow.data_filter import DataFilter, FilterTypes, WindowOperations, DetrendOperations, AggOperations, NoiseTypes
import brainflow
import numpy as np
import mne
import pywt
from scipy import signal
from scipy.linalg import eigh
from scipy.signal import periodogram
import scipy.io as sio


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
            DataFilter.detrend(
                origin_data[channel], DetrendOperations.LINEAR.value)
            DataFilter.remove_environmental_noise(
                origin_data[channel], self.sampling_rate, NoiseTypes.FIFTY_AND_SIXTY)
            DataFilter.perform_bandpass(data[channel], self.sampling_rate, 0.5, 100, 2,
                                        FilterTypes.BUTTERWORTH, ripple=0)
        label = data[-1]
        origin_data = np.concatenate((origin_data, np.array([label])), axis=0)
        ch_types = ['eeg' for i in range(len(origin_data) - 1)]
        ch_types.append('misc')
        channels.append('trigger')
        info = mne.create_info(ch_names=channels, sfreq=1000,
                               ch_types=ch_types, verbose=False)
        mne_data = mne.io.RawArray(origin_data, info)
        mne_data.plot(scalings=25, title=filePath)
    # 计算统计特征

    def extract_statistic_feature(self, epoch_signal):
        statistic_feature = []
        temp_feature = []

        for channel in range(epoch_signal.shape[0]):
            X_1 = np.mean(epoch_signal[channel, :])
            X_2 = np.std(epoch_signal[channel, :], ddof=1)
            X_3 = 0
            total_point = len(epoch_signal[channel, :])

            for point in range(total_point - 1):
                X_3 += abs(epoch_signal[channel, point + 1] -
                           epoch_signal[channel, point]) / (total_point - 1)

            X_4 = X_3 / X_2
            X_5 = 0

            for point in range(total_point - 2):
                X_5 += abs(epoch_signal[channel, point + 2] -
                           epoch_signal[channel, point]) / (total_point - 2)

            X_6 = X_5 / X_2
            X_1_6 = [X_1, X_2, X_3, X_4, X_5, X_6]
            statistic_feature.append(X_1_6)

            abs_X_1 = abs(X_1)
            temp_feature.append(abs_X_1)

        statistic_feature = np.array(statistic_feature)
        temp_feature = np.array(temp_feature)

        return statistic_feature

    # DE 特征
    def extract_DE_new(self, epoch_std, Fs, bands):
        time_sec = 1 * Fs
        NFFT = 2**np.ceil(np.log2(time_sec)).astype(int)
        f = Fs/2 * np.linspace(0, 1, NFFT//2)

        de = np.zeros((epoch_std.shape[0], len(bands)))  # 存储 DE 特征的数组
        for channel in range(epoch_std.shape[0]):
            for section in range(epoch_std.shape[1] // time_sec):
                window = np.hanning(time_sec)
                section_data = epoch_std[channel,
                                         section*time_sec:(section+1)*time_sec]
                Pxx = np.abs(np.fft.fft(section_data * window, NFFT))
                section_de = self.band_DE(Pxx, f, bands)
                de[channel, :] = np.mean(section_de, axis=0)
        return de

    def band_DE(self, Pxx, f, bands):
        # [[1, 3], [4, 7], [8, 13], [14, 30], [31, 48]]
        band = np.array(bands)
        band_DE = np.zeros((band.shape[0],))
        for i in range(band.shape[0]):
            idx = np.where((f >= band[i, 0]) & (f <= band[i, 1]))
            psd = np.mean(Pxx[idx])
            band_DE[i] = np.log10(psd)
        return band_DE
    # PSD 特征

    def extract_PSD_new(self, epoch_data, Fs, bands):
        # extract PSD feature from epoch_data
        # epoch_data: channels * time data matrix
        # Fs: scalar, sampling frequency
        # PSD: feature vector
        nfft = DataFilter.get_nearest_power_of_two(Fs)  # FFT 窗长
        noverlap = 0  # 无重叠
        # range = 'onesided'  # 频率范围为 [0 Fs/2]，只取一半频率
        PSD = []

        for index in range(epoch_data.shape[0]):
            section_psd = []
            for section in range(epoch_data.shape[1] // Fs):
                section_data = epoch_data[index,
                                          section * Fs:(section + 1) * Fs]
                f, Pxx = periodogram(
                    section_data, window=np.hanning(Fs), nfft=nfft, fs=Fs)
                section_psd.append(self.band_psd(Pxx, f, bands))
            psd_mean = np.mean(section_psd, axis=0)
            PSD.append(psd_mean)
        psd = np.array(PSD)
        # psd = psd.transpose(0,2,1)
        psd = np.reshape(psd, (psd.shape[0], -1))
        # psd = np.reshape(psd.T, (1, psd.size))
        return psd

    def band_psd(self, Pxx, f, bands):
        # [[1, 3], [4, 7], [8, 13], [14, 30], [31, 48]]
        band = np.array(bands)  # delta, theta, alpha, beta, gamma 频带
        psd = np.zeros((1, band.shape[0]))
        for i in range(band.shape[0]):
            idx = np.where((f >= band[i, 0]) & (f <= band[i, 1]))[0]
            psd[0, i] = np.mean(Pxx[idx])
        return psd

    def eeg_spatial_pattern(self, eegData):
        # 计算协方差矩阵
        cov_matrix = np.cov(eegData)

        # 计算特征值和特征向量
        eigenvalues, eigenvectors = eigh(cov_matrix)

        # 排序特征值和特征向量
        sorted_indices = np.argsort(eigenvalues)[::-1]
        sorted_eigenvectors = eigenvectors[:, sorted_indices]

        # 提取主成分
        eeg_pattern = sorted_eigenvectors[:]

        return eeg_pattern
    # 暂未开启

    def ica(self, data, icaExcludeChannel):
        data = data.transpose(1, 0, 2)

    def processing(self, files, channel, config, boardId):
        all_features = []
        all_label = []
        for file in files:
            features = []
            features_label = []
            origin_data = np.loadtxt(file)
            origin_data = origin_data.T
            eeg_channel = brainflow.BoardShim.get_eeg_channels(int(boardId))
            eeg_data = origin_data[eeg_channel]
            badChannel = []
            labels = origin_data[-1]

            if 'detrend' in config['checkList']:
                if config['detrend'] == 1:
                    for index in range(len(eeg_data)):
                        DataFilter.detrend(
                            eeg_data[index], DetrendOperations.LINEAR.value)

            if 'wlt_denoising' in config['checkList']:
                wlt_denoising = int(config['wlt_denoising'])
                if wlt_denoising == 1 or wlt_denoising == 2:
                    for index in range(len(eeg_data)):
                        DataFilter.remove_environmental_noise(
                            eeg_data[index], self.sampling_rate, NoiseTypes.FIFTY_AND_SIXTY)

                if wlt_denoising == 0 or wlt_denoising == 2:
                    for index in range(len(eeg_data)):
                        item = eeg_data[index]
                        coeffs = pywt.wavedec(item, 'db4', level=4)
                        threshold = np.sqrt(2 * np.log(len(origin_data)))
                        thresholded_coeffs = [pywt.threshold(
                            c, threshold, mode='soft') for c in coeffs]
                        reconstructed_signal = pywt.waverec(
                            thresholded_coeffs, 'db4')
                        eeg_data[index] = reconstructed_signal[0: len(
                            eeg_data[index])]

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
            eeg_data = np.delete(eeg_data, badChannel, axis=0)
            if 'sample' in config['checkList']:
                slice_trigger = dict({})
                for item in config['triggers']:
                    if item['trigger'] == 0:
                        continue
                    slice_trigger[item['trigger']] = {
                        'startTime': item['startTime'], 'endTime': item['endTime']}

                for index in range(len(labels)):
                    label = labels[index]
                    if label == 0:
                        continue
                    if label in slice_trigger:
                        sub_data = eeg_data[:, index + int(self.sampling_rate * float(slice_trigger[label]['startTime'])): index + int(
                            self.sampling_rate * float(slice_trigger[label]['endTime']))]
                        if len(features) == 0:
                            features.append(sub_data)
                            features_label.append(int(label))
                        elif len(sub_data[0]) == len(features[0][0]):
                            features.append(sub_data)
                            features_label.append(int(label))
            features = np.array(features)
            if 'segmentation' in config['checkList'] and 'sample' in config['checkList']:
                segmentation_data = []
                segmentation_label = []
                length = features.shape[2]
                for i in range(len(features)):
                    for j in range(int(config['segmentation'])):
                        sub_data = features[i, :, j * int(length / int(config['segmentation'])): (
                            j+1) * int(length / int(config['segmentation']))]
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
                        detrend_mean = np.mean(features[:, :, int(float(item[config['sampleDetrendStart']]) * self.sampling_rate): int(
                            float(item[config['sampleDetrendEnd']]) * self.sampling_rate)], axis=1)
                        item -= detrend_mean
                        sample_data.append(item)
                features = sample_data
            features = np.array(features)

            if 'sample_filter' in config['checkList'] and 'sample' in config['checkList']:
                for item in range(len(features)):
                    data = features[item]
                    for index in range(len(data)):
                        DataFilter.perform_bandpass(data[index], self.sampling_rate, config['samplelow'], config['samplehigh'], 2,
                                                    FilterTypes.BUTTERWORTH, ripple=0)

            if 'down_sample' in config['checkList']:
                if 'sample' in config['checkList']:
                    down_sample_data = np.zeros((len(features), len(features[0]), int(
                        config['downSample'] * len(features[0, 0]) / self.sampling_rate)))
                    for i in range(len(features)):
                        for j in range(len(features[0])):
                            down_sample_data[i, j] = signal.resample(features[i, j], int(
                                config['downSample'] * len(features[i, j]) / self.sampling_rate))
                else:
                    down_sample_data = np.zeros((len(features),  int(
                        config['downSample'] * len(features[0]) / self.sampling_rate)))
                    for i in range(len(features)):
                        down_sample_data[i] = signal.resample(features[i], int(
                            config['downSample'] * len(features[i]) / self.sampling_rate))

                features = down_sample_data
                self.sampling_rate = int(config['downSample'])

            all_features.extend(features.tolist())
            all_label.extend(features_label)
        all_features = np.array(all_features)
        characteristic_wave_Data = []
        if 'characteristicWave' in config['feature']['checkList']:
            copied_feature = np.copy(all_features)
            sampling_rate = self.sampling_rate
            if 'down_sample_data' in config['checkList']:
                sampling_rate = int(config['downSample'])
            if 'sample' in config['checkList']:
                new_feature = np.zeros((len(copied_feature), len(copied_feature[0]), len(
                    config['feature']['characteristicWave']), len(copied_feature[0][0])))
                for item in range(len(copied_feature)):
                    for index in range(len(copied_feature[0])):
                        single_features = copied_feature[item, index]
                        for wave_index in range(len(config['feature']['characteristicWave'])):
                            wave = config['feature']['characteristicWave'][wave_index]
                            DataFilter.perform_bandpass(single_features, sampling_rate, int(wave[0]),int( wave[1]), 2,
                                                                    FilterTypes.BUTTERWORTH, ripple=0)
                            new_feature[item, index, wave_index] = single_features
            else:
                new_feature = np.zeros((len(copied_feature), len(
                    config['feature']['characteristicWave']), len(copied_feature[0])))
                for index in range(len(copied_feature)):
                    single_features = copied_feature[item, index]
                    for wave_index in range(len(config['feature']['characteristicWave'])):
                        wave = config['feature']['characteristicWave'][wave_index]
                        DataFilter.perform_bandpass(single_features, sampling_rate, int(wave[0]), int(wave[1]), 2,
                                                                FilterTypes.BUTTERWORTH, ripple=0)
                        new_feature[item, index, wave_index] = single_features
            characteristic_wave_Data = new_feature
        print('characteristic_wave_Data', characteristic_wave_Data.shape)
        spatial_pattern = []
        if 'spatialPattern' in config['feature']['checkList']:
            copied_feature = np.copy(all_features)
            if len(features.shape) == 3:
                for index in range(len(copied_feature)):
                    spatial_pattern.append(
                        self.eeg_spatial_pattern(copied_feature[index]))
            else:
                spatial_pattern = self.eeg_spatial_pattern(copied_feature)
        spatial_pattern = np.array(spatial_pattern)
        print('spatial_pattern',  spatial_pattern.shape)
        psd_feature = []
        if 'psd' in config['feature']['checkList']:
            bands = [1, 48]
            if len(config['feature']['characteristicWave']) > 0:
                bands = config['feature']['characteristicWave']
            copied_feature = np.copy(all_features)
            if len(features.shape) == 3:
                for index in range(copied_feature.shape[0]):
                    psd_feature.append(self.extract_PSD_new(
                        copied_feature[index], self.sampling_rate, bands))
            else:
                psd_feature = self.extract_PSD_new(
                    copied_feature, self.sampling_rate, bands)
        psd_feature = np.array(psd_feature)
        print("psd_feature", psd_feature.shape)
        de_feature = []
        if 'DE' in config['feature']['checkList']:
            bands = [1, 48]
            if len(config['feature']['characteristicWave']) > 0:
                bands = config['feature']['characteristicWave']
            copied_feature = np.copy(all_features)
            if len(features.shape) == 3:
                for index in range(copied_feature.shape[0]):
                    de_feature.append(self.extract_DE_new(
                        copied_feature[index], self.sampling_rate, bands))
            else:
                de_feature = self.extract_DE_new(
                    copied_feature, self.sampling_rate, bands)
        de_feature = np.array(de_feature)

        print('de_feature', de_feature.shape)
        if 'PLV' in config['feature']['checkList']:
            print('PLV')

        statistic_feature = []
        if 'statistic' in config['feature']['checkList']:
            copied_feature = np.copy(all_features)
            if len(features.shape) == 3:
                statistic_feature = np.zeros(
                    (copied_feature.shape[0], copied_feature.shape[1], 6))
                for index in range(copied_feature.shape[0]):
                    statistic_feature[index] = self.extract_statistic_feature(
                        copied_feature[index])
            else:
                statistic_feature = self.extract_statistic_feature(
                    copied_feature)

        print('statistic_feature', statistic_feature.shape)
        
        
        # if config['saveDataPath'] == '':
        #     return
        
        if config['createScript'] == '1':
            self.createScript(files, channel, config,
                              boardId, './demo-script.py')
            
        if config['isOutPutData'] == '1':
            save_mat_data = dict({})
            save_mat_data['origin_data'] = eeg_data.tolist()
            save_mat_data['processing_data'] = all_features.tolist()
            save_mat_data['processing_label'] = all_label
            save_mat_data['characteristic_wave_Data'] = characteristic_wave_Data.tolist()
            save_mat_data['spatialPattern'] = spatial_pattern.tolist()
            save_mat_data['psd'] = psd_feature.tolist()
            save_mat_data['DE'] = de_feature.tolist()
            save_mat_data['statistic'] = statistic_feature.tolist()
            print('this is create mat file')
        
            sio.savemat('./demo-script.mat', save_mat_data)
        print('this is create mat end')
    
    def createScript(self, files, channel, config, boardId, fileName):
        print('this is create script')

        script_package = """
import numpy as np
import mne
from brainflow.data_filter import DataFilter, FilterTypes, WindowOperations, DetrendOperations, AggOperations, NoiseTypes
import brainflow
import pywt
from scipy import signal
from scipy.linalg import eigh
from scipy.signal import periodogram
import scipy.io as sio

        """

        script_static_feature = """
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
        statistic_feature.append(X_1_6)

        abs_X_1 = abs(X_1)
        temp_feature.append(abs_X_1)

    statistic_feature = np.array(statistic_feature)
    temp_feature = np.array(temp_feature)

    return statistic_feature

        """

        script_de_new = """
def extract_DE_new(epoch_std, Fs, bands):
    time_sec = 1 * Fs
    NFFT = 2**np.ceil(np.log2(time_sec)).astype(int)
    f = Fs/2 * np.linspace(0, 1, NFFT//2)

    de = np.zeros((epoch_std.shape[0], len(bands)))  # 存储 DE 特征的数组
    for channel in range(epoch_std.shape[0]):
        for section in range(epoch_std.shape[1] // time_sec):
            window = np.hanning(time_sec)
            section_data = epoch_std[channel,
                                        section*time_sec:(section+1)*time_sec]
            Pxx = np.abs(np.fft.fft(section_data * window, NFFT))
            section_de = band_DE(Pxx, f, bands)
            de[channel, :] = np.mean(section_de, axis=0)

    return de

def band_DE(Pxx, f, bands):
    # [[1, 3], [4, 7], [8, 13], [14, 30], [31, 48]]
    band = np.array(bands)
    band_DE = np.zeros((band.shape[0],))
    for i in range(band.shape[0]):
        idx = np.where((f >= band[i, 0]) & (f <= band[i, 1]))
        psd = np.mean(Pxx[idx])
        band_DE[i] = np.log10(psd)
    return band_DE"""

        script_extract_PSD_new = """
        #PSD 特征
def  extract_PSD_new(epoch_data, Fs, bands):
    # extract PSD feature from epoch_data
    # epoch_data: channels * time data matrix
    # Fs: scalar, sampling frequency
    # PSD: feature vector
    nfft = DataFilter.get_nearest_power_of_two(Fs)  # FFT 窗长
    noverlap = 0  # 无重叠
    # range = 'onesided'  # 频率范围为 [0 Fs/2]，只取一半频率
    PSD = []

    for index in range(epoch_data.shape[0]):
        section_psd = []
        for section in range(epoch_data.shape[1] // Fs):
            section_data = epoch_data[index, section * Fs:(section + 1) * Fs]
            f, Pxx = periodogram(section_data, window=np.hanning(Fs), nfft=nfft, fs=Fs)
            section_psd.append(band_psd(Pxx, f, bands))
        psd_mean = np.mean(section_psd, axis=0)
        PSD.append(psd_mean)
    psd = np.array(PSD)
    # psd = psd.transpose(0,2,1)
    psd = np.reshape(psd,(psd.shape[0],-1))
    # psd = np.reshape(psd.T, (1, psd.size))
    return psd
def band_psd(Pxx, f, bands):
    # [[1, 3], [4, 7], [8, 13], [14, 30], [31, 48]]
    band = np.array(bands)  # delta, theta, alpha, beta, gamma 频带
    psd = np.zeros((1, band.shape[0]))
    for i in range(band.shape[0]):
        idx = np.where((f >= band[i, 0]) & (f <= band[i, 1]))[0]
        psd[0, i] = np.mean(Pxx[idx])
    return psd
        """

        script_spatial_pattern = """
def  eeg_spatial_pattern(eegData):
    # 计算协方差矩阵
    cov_matrix = np.cov(eegData)
    
    # 计算特征值和特征向量
    eigenvalues, eigenvectors = eigh(cov_matrix)
    
    # 排序特征值和特征向量
    sorted_indices = np.argsort(eigenvalues)[::-1]
    sorted_eigenvectors = eigenvectors[:, sorted_indices]
    
    # 提取主成分
    eeg_pattern = sorted_eigenvectors[:]
    
    return eeg_pattern
        """

        if 'statistic' not in config['feature']['checkList']:
            script_static_feature = ""

        if 'DE' not in config['feature']['checkList']:
            script_de_new = ""

        if "psd" not in config['feature']['checkList']:
            script_extract_PSD_new = ""

        if 'spatialPattern' not in config['feature']['checkList']:
            script_spatial_pattern = ""

        if 'statistic' not in config['feature']['checkList']:
            script_static_feature = ""
        script1 = f"""
files = {files}
channel = {channel}
config = {config}
boardId = {boardId}
sampling_rate = 1000
# 计算统计特征

def get_features(files, channel, config, boardId):
    all_features = []
    all_label = []
    for file in files:
        features = []
        features_label = []
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

        eeg_data  = np.delete(eeg_data, badChannel, axis=0)
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
                sub_data = eeg_data[:, index + int(sampling_rate * float(slice_trigger[label]['startTime']) ): index + int(sampling_rate * float(slice_trigger[label]['endTime'] ))]
                if len(features) == 0:
                    features.append(sub_data)
                    features_label.append(int(label))
                elif len(sub_data[0]) == len(features[0][0]):
                    features.append(sub_data)
                    features_label.append(int(label))
        features = np.array(features)
        
        """

        script_segment = """"""
        if 'segmentation' in config['checkList'] and 'sample' in config['checkList']:
            script_segment = """
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
        
        sampling_rate =  int(config['downSample'])

      
                """
        script_extend_all = """
        all_features.extend(features.tolist())
        all_label.extend(features_label)
    all_features = np.array(all_features)
    
        """
        script11 = """"""
        if 'characteristicWave' in config['feature']['checkList']:
            if 'sample' in config['checkList']:
                script11 = """
    characteristic_wave_Data = []
    copied_feature = np.copy(features)
    characteristic_wave_Data = np.zeros((len(copied_feature), len(copied_feature[0]),len(config['feature']['characteristicWave']), len(copied_feature[0][0])))
    for item in range(len(copied_feature)):
        for index in range(len(copied_feature[0])):
            single_features = copied_feature[item, index]
            for wave_index in range(len(config['feature']['characteristicWave'])):
                wave = config['feature']['characteristicWave'][wave_index]
                DataFilter.perform_bandpass(single_features, sampling_rate, int(wave[0]), int(wave[1]), 2,
                                        FilterTypes.BUTTERWORTH, ripple=0)
                characteristic_wave_Data[item, index, wave_index] = single_features
        """
            else:
                script11 = """
    new_feature = np.zeros((len(copied_feature), len(config['feature']['characteristicWave']), len(copied_feature[0])))
    for index in range(len(copied_feature)):
        single_features = copied_feature[item, index]
        for wave_index in range(len(config['feature']['characteristicWave'])):
            wave = config['feature']['characteristicWave'][wave_index]
            DataFilter.perform_bandpass(single_features, sampling_rate, int(wave[0]), int(wave[1]), 2,
                                    FilterTypes.BUTTERWORTH, ripple=0)
            new_feature[item, index, wave_index] = single_features
    characteristic_wave_Data = new_feature
    print('characteristic_wave_Data', characteristic_wave_Data.shape)
        """
        script12 = """"""
        if 'spatialPattern' in config['feature']['checkList']:
            script12 = """
    spatial_pattern = []

    copied_feature = np.copy(features)
    if len(features.shape) == 3:
        for index in range(len(copied_feature)):
            spatial_pattern.append(eeg_spatial_pattern(copied_feature[index]))
    else:
        spatial_pattern = eeg_spatial_pattern(copied_feature)
    spatial_pattern = np.array(spatial_pattern)
    print('spatial_pattern',  spatial_pattern.shape)
    """
        script13 = """"""
        if 'psd' in config['feature']['checkList']:
            script13 = """
    psd_feature = []
    bands = [1, 48]
    if len(config['feature']['characteristicWave']) > 0:
        bands = config['feature']['characteristicWave']
    copied_feature = np.copy(features)
    if len(features.shape) == 3:
        for index in range(copied_feature.shape[0]):
            psd_feature.append(extract_PSD_new(copied_feature[index], sampling_rate, bands))
    else:
        psd_feature = extract_PSD_new(copied_feature, sampling_rate, bands)
    psd_feature = np.array(psd_feature)
    print("psd_feature", psd_feature.shape)
        """
        script14 = """"""
        if 'DE' in config['feature']['checkList']:
            script14 = """
    de_feature = []
    bands = [1, 48]
    if len(config['feature']['characteristicWave']) > 0:
        bands = config['feature']['characteristicWave']
    copied_feature = np.copy(features)
    if len(features.shape) == 3:
        for index in range(copied_feature.shape[0]):
            de_feature.append(extract_DE_new(copied_feature[index], sampling_rate, bands))
    else:
        de_feature = extract_DE_new(copied_feature, sampling_rate, bands)
    de_feature = np.array(de_feature)
    print('de_feature', de_feature.shape)
        """
        if 'PLV' in config['feature']['checkList']:
            print('PLV')
        script15 = """"""

        if 'statistic' in config['feature']['checkList']:
            script15 = """
    statistic_feature = []
    copied_feature = np.copy(features)
    if len(features.shape) == 3:
        statistic_feature = np.zeros((copied_feature.shape[0], copied_feature.shape[1], 6))
        for index in range(copied_feature.shape[0]):
            statistic_feature[index] = extract_statistic_feature(copied_feature[index])
    else:
        statistic_feature = extract_statistic_feature(copied_feature)
        """
            
        script_save = """"""
        if config['isOutPutData'] == '1':
            script_save = """
    save_mat_data = dict({})
    save_mat_data['origin_data'] = eeg_data.tolist()
    save_mat_data['processing_data'] = features.tolist()
    save_mat_data['processing_label'] = features_label
    save_mat_data['characteristic_wave_Data'] = characteristic_wave_Data.tolist()
    save_mat_data['spatialPattern'] = spatial_pattern.tolist()
    save_mat_data['psd'] = psd_feature.tolist()
    save_mat_data['DE'] = de_feature.tolist()
    save_mat_data['statistic'] = statistic_feature.tolist()
    sio.savemat('./demo-script.mat', save_mat_data)

        """
        script = script_package + script_static_feature + script_de_new+script_static_feature+script_spatial_pattern+script_extract_PSD_new + script1 + script2 + \
            script3 + script4 + script5 + script6 + script7 + script_segment + script8 + \
            script9 + script10+script_extend_all + script11 + script12 + script13 + script14 + script15
        script += script_save

        filename = fileName  # 指定保存的文件名

        # 打开文件并写入脚本内容
        with open(filename, "w") as file:
            file.write(script)
        file.close()
