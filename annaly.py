import mne
import os 
import numpy as np
from matplotlib import pyplot as plt 
from brainflow import data_filter, DataFilter, DetrendOperations, WindowOperations
from brainflow.data_filter import FilterTypes
import pywt
import scipy
from scipy.signal import filtfilt, lfilter
files = os.listdir('./data/svp1_2')
showFiles = []
import mne 
import numpy as np
from brainflow import DataFilter
from matplotlib import pyplot as plt
from scipy import signal

## 功能：计算z分数和snr
#  patpowavedata--频域数据
#  foi_idx--关注的频率点下标
#  Author：nongying, 13011802988@163.com
fs = 1000
files = []
dirs = os.listdir('./data/svp1_2')
for file in dirs:
    if '.txt' in file:
        continue
    files.append(file)
    
def zsnr(patpowavedata, foi_idx):
    ## 计算z分数
    num_freq = len(patpowavedata)
    num_mean_plus = 10
    num_freqoi = len(foi_idx)
    zscore = np.ones((num_freqoi)) * np.nan  # 6个关注频率
    x = 0
    for zfreq in foi_idx:  # 关注频率
        # 计算关注频率 前10 和后10 的均值，排除直接相邻的一个
        a = np.hstack((patpowavedata[zfreq - num_mean_plus:zfreq - 2],
                        patpowavedata[zfreq + 2:zfreq + num_mean_plus]))
        b = np.mean(a)  # 求均值power
        d = np.std(a)  # 求标准差

        # 计算 幅值与均值的比值
        
        zz = (patpowavedata[zfreq] - b) / d
        zscore[x] = zz
        x = x + 1  # 横坐标6个关注频率

    ## 计算SNR
    patsnr = np.ones((num_freq)) * np.nan
    for idx in range(num_mean_plus, num_freq - num_mean_plus):  # powspctrm 矩阵为66*165
        # 计算幅值前10 和后10 的均值，排除直接相邻的一个
        a = np.hstack((patpowavedata[idx - num_mean_plus:idx - 2],
                        patpowavedata[idx + 2:idx + num_mean_plus]))
        b = np.mean(a)
        # 计算 幅值与均值的比值
        snr = patpowavedata[idx] / b
        patsnr[idx] = snr

    # for idx in [i for i in range(num_mean_plus)] + [i for i in range(num_freq - num_mean - 1, num_freq)]:
    #     patsnr[idx] = 0  # powspctrm矩阵边缘的snr为0
    patsnr = np.nan_to_num(patsnr)
    return zscore, patsnr

feature = []
count = 0
for file in files:
    originData = np.loadtxt('./data/svp1_2/' + file).T
    print(originData.shape)
    labels = originData[-1]
    print(labels)
    data = originData[0: len(originData), 1:33]
    # for index in range(len(data)):
    #     DataFilter.detrend(data[index], DetrendOperations.NO_DETREND.value)
    #     DataFilter.perform_bandpass(data[index], fs, 0.1, 100, 2,
    #                                     FilterTypes.BESSEL.value, 0)
    mean = np.mean(data, axis=0)
    # 重参考
    for index in range(len(data)):
        data[index] -= mean
    # 低通滤波
    data = mne.filter.filter_data(data, sfreq=fs, l_freq=0.1, h_freq=100, verbose=False)
    # channels = ['poz', "oz", 'pz','poz', "oz", 'pz','poz', "oz",'poz', "oz", 'pz','poz', "oz", 'pz','poz', "oz",'poz', "oz", 'pz','poz', "oz", 'pz','poz', "oz",'poz', "oz", 'pz','poz', "oz", 'pz','poz', "oz"]
    channels = ["OZ", 'PZ','O1', "P3", "T5",'FPZ',
              "A1", "T3","F7", "F3", "C3", "FP1",
              "FZ", "FP2", "F4", "F8", "T4", "A2", 
              "T6", "O2", "P4", "C4", 'CZ', "HOE"]
    # 获取每个trial 的数据
    trial_data = []
    start = False
    for index in range(len(labels)):
        label = labels[index]
        if int(label) == 0:
            continue
        if int(label) == -1:
            index_start = int(index-0.5*fs)
            index_end = index_start+ int(fs* 20.5)
            print(index_start, index_end)
            subData = data[:,index_start:index] 
            print(subData.shape)
            detrend_data =np.array([np.mean(data[:, index_start-100:index_start], axis=1)]).T
            subData -= detrend_data  
            print(detrend_data.shape)
            if len(trial_data) != 0 and len(subData[0]) != len(trial_data[0]) :
                continue
            trial_data.append(subData)
            # break
    # 将每个trial 进行平均
    for index in range(len(trial_data)):
        if len(feature) == 0:
            feature = trial_data[index]
            count += 1
        else: 
            feature += trial_data[index]
            count += 1
feature /= count
psd_size = DataFilter.get_nearest_power_of_two(int(1024*16))
xtick = np.array([1.2, 2.4, 3.6, 4.8, 6, 7.2])
foi_idx = []
print('====')
print(np.array(feature).shape)
for index in range(len(feature)):
    foi_idx = []
    ch_feature = feature[index]
    [freq,pxx]  = signal.welch(ch_feature, fs, nperseg=int(1024* 16), average="median", window='hann')
    freq = freq[0: 130]
    pxx = pxx[0:130]
    count = 0
    for idx in range(len(freq)):
        freqi = freq[idx]
        if count >= len(xtick):
            break
        if freqi - xtick[count] < 0.3 and freqi - xtick[count] > 0:
            count += 1
            foi_idx.append(idx)
    zScore, patsnr = zsnr(np.array(pxx), foi_idx)
    for i in foi_idx:
        freqi = freq[i]
        plt.axvline(freqi, linestyle='dashed', color='red')
    plt.plot(freq, patsnr)
    plt.title(channels[index],loc='left')
    plt.savefig('./img/'+"condition1_" + str(index)+channels[index] + '.jpg')
    plt.show()
