import numpy as np

def extract_DE_new(epoch_std, Fs):
    time_sec = 1 * Fs
    NFFT = 2**np.ceil(np.log2(time_sec)).astype(int)
    f = Fs/2 * np.linspace(0, 1, NFFT//2)
    window = np.hanning(time_sec)

    de = np.zeros((epoch_std.shape[0], 5))
    for channel in range(epoch_std.shape[0]):
        section_de = np.zeros((int(len(epoch_std[channel]) / time_sec), 5))
        for section in range(int(len(epoch_std[channel]) / time_sec)):
            section_data = epoch_std[channel, section*time_sec:(section+1)*time_sec]
            Pxx = np.abs(np.fft.fft(section_data * window, NFFT))
            section_de[section] = band_DE(Pxx, f)

        de_mean = np.mean(section_de, axis=0)
        de[channel] = de_mean

    diff_entropy = de.T.flatten()
    rasm_feature = RASM(de).T.flatten()
    return diff_entropy, rasm_feature

def band_DE(Pxx, f):
    band = np.array([[1, 3], [4, 7], [8, 13], [14, 30], [31, 48]])
    psd = np.zeros((1, 5))
    for i in range(band.shape[0]):
        idx = np.where((f >= band[i, 0]) & (f <= band[i, 1]))[0]
        psd[0, i] = np.mean(Pxx[idx])
        psd[0, i] = np.mean(Pxx[idx]**2)
    band_DE = np.log10(psd)
    return band_DE

def RASM(de):
    rasm_feature = np.zeros((15, de.shape[1]))
    rasm_feature[0] = de[0] / de[16]
    rasm_feature[1] = de[1] / de[17]
    rasm_feature[2] = de[2] / de[18]
    rasm_feature[3] = de[3] / de[19]
    rasm_feature[4] = de[4] / de[20]
    rasm_feature[5] = de[5] / de[21]
    rasm_feature[6] = de[6] / de[22]
    rasm_feature[7] = de[7] / de[23]
    rasm_feature[8] = de[8] / de[24]
    rasm_feature[9] = de[10] / de[25]
    rasm_feature[10] = de[11] / de[26]
    rasm_feature[11] = de[12] / de[27]
    rasm_feature[12] = de[13] / de[28]
    rasm_feature[13] = de[14] / de[29]
    rasm_feature[14] = de[15] / de[30]
    return rasm_feature

import numpy as np
from scipy.signal import periodogram, hanning

def extract_PSD_new(epoch_data, Fs):
    # extract PSD feature from epoch_data
    # epoch_data: channels * time data matrix
    # Fs: scalar, sampling frequency
    # PSD: feature vector
    nfft = 512  # FFT 长度
    noverlap = 0  # 无重叠
    range_ = 'onesided'  # 频率范围为 [0, Fs/2]，只取一侧频谱
    PSD = []

    for channel in range(epoch_data.shape[0]):
        section_psd = []
        for section in range(int(epoch_data.shape[1] / Fs)):
            section_data = epoch_data[channel, section * Fs : (section + 1) * Fs]
            f, Pxx = periodogram(section_data, window=hanning(Fs), nfft=nfft, fs=Fs)
            section_psd.append(band_psd(Pxx, f))
        
        psd_mean = np.mean(section_psd, axis=0)
        PSD.append(psd_mean)
    
    PSD = np.array(PSD).reshape(1, -1)
    return PSD

def band_psd(Pxx, f):
    band = np.array([[1, 3], [4, 7], [8, 13], [14, 30], [31, 48]])
    psd = np.zeros((1, band.shape[0]))

    for i in range(band.shape[0]):
        idx = np.where((f >= band[i, 0]) & (f <= band[i, 1]))
        psd[0, i] = np.mean(Pxx[idx])

    return psd