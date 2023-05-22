import numpy as np

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

def band_DE(Pxx, f):
    band = np.array([[1, 3], [4, 7], [8, 13], [14, 30], [31, 48]])
    band_DE = np.zeros((band.shape[0],))
    for i in range(band.shape[0]):
        idx = np.where((f >= band[i, 0]) & (f <= band[i, 1]))
        psd = np.mean(Pxx[idx])
        band_DE[i] = np.log10(psd)
    return band_DE

def RASM(de):
    rasm_feature = np.zeros((15, de.shape[1]))
    rasm_feature[0, :] = de[0, :] / de[16, :]
    rasm_feature[1, :] = de[1, :] / de[17, :]
    rasm_feature[2, :] = de[2, :] / de[18, :]
    rasm_feature[3, :] = de[3, :] / de[19, :]
    rasm_feature[4, :] = de[4, :] / de[20, :]
    rasm_feature[5, :] = de[5, :] / de[21, :]
    rasm_feature[6, :] = de[6, :] / de[22, :]
    rasm_feature[7, :] = de[7, :] / de[23, :]
    rasm_feature[8, :] = de[8, :] / de[24, :]
    rasm_feature[9, :] = de[9, :] / de[25, :]
    rasm_feature[10, :] = de[10, :] / de[26, :]
    rasm_feature[11, :] = de[11, :] / de[27, :]
    rasm_feature[12, :] = de[12, :] / de[28, :]
    rasm_feature[13, :] = de[13, :] / de[29, :]
    rasm_feature[14, :] = de[14, :] / de[30, :]
    return rasm_feature


import numpy as np
from scipy.signal import periodogram, hanning

def extract_PSD_new(epoch_data, Fs):
    # extract PSD feature from epoch_data
    # epoch_data: channels * time data matrix
    # Fs: scalar, sampling frequency
    # PSD: feature vector
    nfft = 512  # FFT 窗长
    noverlap = 0  # 无重叠
    range = 'onesided'  # 频率范围为 [0 Fs/2]，只取一半频率
    PSD = []

    for channel in range(epoch_data.shape[0]):
        section_psd = []
        for section in range(epoch_data.shape[1] // Fs):
            section_data = epoch_data[channel, section * Fs:(section + 1) * Fs]
            f, Pxx = periodogram(section_data, window=hanning(Fs), nfft=nfft, fs=Fs)
            section_psd.append(band_psd(Pxx, f))
        psd_mean = np.mean(section_psd, axis=0)
        PSD.append(psd_mean)

    psd = np.array(PSD)
    psd = np.reshape(psd.T, (1, psd.size))

    return psd

def band_psd(Pxx, f):
    band = np.array([[1, 3], [4, 7], [8, 13], [14, 30], [31, 48]])  # delta, theta, alpha, beta, gamma 频带
    psd = np.zeros((1, band.shape[0]))
    
    for i in range(band.shape[0]):
        idx = np.where((f >= band[i, 0]) & (f <= band[i, 1]))[0]
        psd[0, i] = np.mean(Pxx[idx])
    
    return psd


import numpy as np

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

import numpy as np
from scipy.signal import hilbert, firwin, filtfilt

def pn_eegPLV(eegData, srate, filtSpec, dataSelectArr=None):
    numChannels, numTimePoints, numTrials = eegData.shape
    
    if dataSelectArr is None:
        dataSelectArr = np.ones((numTrials, 1), dtype=bool)
    else:
        if not isinstance(dataSelectArr, np.ndarray) or dataSelectArr.dtype != bool:
            raise ValueError('Data selection array must be a logical array.')
    
    numConditions = dataSelectArr.shape[1]
    filtPts = firwin(filtSpec.order+1, filtSpec.range, fs=srate, pass_zero=False)
    filteredData = filtfilt(filtPts, [1], eegData, axis=1)
    
    plv = np.zeros((numTimePoints, numChannels, numChannels, numConditions))
    
    for channelCount in range(numChannels):
        filteredData[channelCount] = np.angle(hilbert(filteredData[channelCount]))
    
    for channelCount in range(numChannels-1):
        channelData = filteredData[channelCount]
        
        for compareChannelCount in range(channelCount+1, numChannels):
            compareChannelData = filteredData[compareChannelCount]
            
            for conditionCount in range(numConditions):
                phase_diffs = channelData[:, dataSelectArr[:, conditionCount]] - compareChannelData[:, dataSelectArr[:, conditionCount]]
                plv[:, channelCount, compareChannelCount, conditionCount] = np.abs(np.mean(np.exp(1j * phase_diffs), axis=1))
    
    plv = np.squeeze(plv)
    return plv


from scipy.linalg import eigh
def eeg_spatial_pattern(eegData):
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