import numpy as np
import os
from matplotlib import pyplot as plt
from brainflow import data_filter, DataFilter, DetrendOperations, WindowOperations
from brainflow.data_filter import FilterTypes
from scipy import signal
from pyedflib import highlevel
import json
import scipy.io as sio


class Result(object):
    def __init__(self):
        super(Result, self).__init__()
        self.dir_path = '.'
        self.dir_path = os.getcwd()
        self.dir_path = self.dir_path.replace("\\", "/", 5)

    def readAllFiles(self):
        return os.listdir('./edfFile/svp1_2')

    def zsnr(self, patpowavedata, foi_idx, number):
        # 计算z分数
        num_freq = len(patpowavedata)
        num_mean_plus = number
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
        # 计算SNR
        patsnr = np.ones((num_freq)) * np.nan
        for idx in range(num_mean_plus, num_freq - num_mean_plus):  # powspctrm 矩阵为66*165
            # 计算幅值前10 和后10 的均值，排除直接相邻的一个
            a = np.hstack((patpowavedata[idx - num_mean_plus:idx - 2],
                            patpowavedata[idx + 2:idx + num_mean_plus]))
            b = np.mean(a)
            # 计算 幅值与均值的比值
            snr = patpowavedata[idx] / b
            patsnr[idx] = snr
        patsnr = np.nan_to_num(patsnr)
        return zscore, patsnr

    def readEdfFile(self, fileName):
        signals, signal_headers, header = highlevel.read_edf(fileName)
        return signals, signal_headers, header

    # def count164z(self, zScore, threshold, base_freq_idx):
    #     num_electrode = zScore.shape[0]
    #     num_base = 0  # 6Hz frequency band counts
    #     num_singular = 0  # 1.2Hz frequency band counts
    #     zdata164 = [np.empty((num_electrode, zScore.shape[1])), np.empty(
    #         (num_electrode, zScore.shape[1]))]
    #     idxMarked = [np.empty(num_electrode, dtype=np.int64),
    #                           np.empty(num_electrode, dtype=np.int64)]
    #     for e in range(num_electrode):
    #         if zScore[e, base_freq_idx] > threshold:  # Check for 6Hz frequency band
    #             num_base += 1
    #             zdata164[0][e, :] = zScore[e, :]
    #             # Record the electrode with 6Hz frequency band
    #             idxMarked[0][num_base - 1] = e
    #             if zScore[e, 0] > threshold:  # Check for 1.2Hz frequency band
    #                 num_singular += 1
    #                 zdata164[1][e, :] = zScore[e, :]
    #                 # Record the electrode with 1.2Hz frequency band
    #                 idxMarked[1][num_singular - 1] = e
    #             else:
    #                 # Check if there are more than 3 high-frequency bands
    #                 aa = np.sum(zScore[e, :] > threshold)
    #                 if aa >= 3:
    #                     num_singular += 1
    #                     zdata164[1][e, :] = zScore[e, :]
    #                     # Record the electrode with 1.2Hz frequency band
    #                     idxMarked[1][num_singular - 1] = e
    #     return num_base, num_singular, zdata164, idxMarked

    def count164z(self, zScores, channels,baseFrequency, ZScoreStandard):
        countbase = 0
        countOdd = 0
        for item in zScores:
            if int(item[0]* 10) == int(baseFrequency *10) and item[1] > ZScoreStandard:
                countbase =1
            if int(item[0] * 10) != int(baseFrequency* 10) and item[1] > ZScoreStandard:
                countOdd += 1
        return countbase, countOdd
    def drawCsv(self, csvFile):
        print('csv file')

    def createReport(self, message):
        print(message)

    def getResultInfo(self, message):
        # file = message['data']['fileName']
        file = 'C:/Users/admin/Desktop/mindBridgeSoftware/HBCI/test_data/32_12/2023_04_19_11_01_08/6motion/result/FPVS-result.mat'
        data = sio.loadmat(file)
        return data

    def createImages(self, message):
        print('sss')
        #   for i in foi_idx:
        #     freqi = freq[i]
        #     plt.axvline(freqi, linestyle='dashed', color='red')
        #     plt.ylim(0, np.max(patsnr))
        #     plt.plot(freq, patsnr)
            
        #     stringScore = ''
        #     zScore = zScore.tolist()
        #     for id in range(len(zScore)):
        #         stringScore += str(xtick[id]) + ":"+ str(round(zScore[id], 2)) + "    "
        #     channel_data["zScore"] = stringScore
        #     channel_data['data'] = [freq, patsnr]
        #     channel_Score[channels[index]] =channel_data
        #     plt.xlabel(stringScore)
        #     plt.title(channels[index],loc='left')
            # plt.savefig(imagesdir+'/'+ str(index)+'-'+str(headerInfo[index]) + '.jpg')
            # imagePath.append(imagesdir+'/'+ str(index)+'-'+str(headerInfo[index]) + '.jpg')
    def createInfoByColor(self, message):
        file = message['data']['fileName']
    
    def createExprimentSsvepResult(self, message):
            file = message['data']['fileName']
            startTrialTime = float(message['data']['startTrialTime'])
            endTrialTime = float(message['data']['endTrialTime'])
            # imagesdir = self.dir_path +'/img/'+ file.replace('.edf', '') 
            # signals, signal_headers, header = self.readEdfFile(file)
            info = sio.loadmat(file.replace('.bdf', '.mat'))
            fs = info["sampleRate"][0][0]
            signals = info['data']
            # print(signals.shape)
            channels = [channel.replace(' ', '', 10) for channel in info['channels']]
            signals = signals.T
            signals = np.ascontiguousarray(signals)
            # headerInfo = []
            # sample_rate = []
            # for head in signal_headers:
            #     headerInfo.append(head['label'])
            #     sample_rate.append(head['sample_rate'])
            # if not os.path.exists(imagesdir):
            #     os.makedirs(imagesdir)
            # fs = sample_rate[0]
            selectComputedChannel = message['data']['selectComputedChannel']
            rereference = message['data']['rereference']
            xtick = message['data']['frequency']
            baseFrequency = message['data']['basefrequency']
            numMeanPlus = message['data']['number']
            labels = signals[-1]
            signals = signals[1: 33]
            data = signals[:len(signals)-1]
            for index in range(len(data)):
                DataFilter.detrend(data[index], DetrendOperations.NO_DETREND.value)
                DataFilter.perform_bandpass(data[index], int(fs), message['data']['filterlow'], message['data']['filterHigh'], 2,
                                                FilterTypes.BUTTERWORTH.value, 0)
            if rereference :
                mean = np.mean(data, axis=0)
                # 重参考
                for index in range(len(data)):
                    data[index] -= mean
            trial_data = []
            trial_index = 0
            select_train = message['data']['selectTrial']
            for index in range(len(labels)):
                label = labels[index]
                if int(label) == 0:
                    continue
                if int(label) == -1:
                    if trial_index == len(select_train) or trial_index > len(select_train) or int(select_train[trial_index]) == 0 :
                        trial_index += 1
                        continue
                    trial_index += 1
                    index_start = int(index-float(startTrialTime)*fs)
                    index_end = int(index + float(endTrialTime)* fs)
                    subData = data[:,index_start:index_end] 
                    if subData.shape[1] == (startTrialTime + endTrialTime) * fs:
                        detrend_data = np.array([np.mean(data[:, index-int(fs*float(message['data']['baseLineTime'])):index], axis=1)]).T
                        subData -= detrend_data
                        subData = subData[:, 0: message['data']['paradigmTime'] * fs]
                        trial_data.append(subData)
                    
            # 将每个trial 进行平均
            feature = []
            count = 0
            if len(trial_data) == 0:
                return []
            for index in range(len(trial_data)):
                if len(feature) == 0:
                    feature = trial_data[index]
                    count += 1
                else: 
                    feature += trial_data[index]
                    count += 1
            feature /= count
            psd_size = DataFilter.get_nearest_power_of_two(len(feature[0]))
            foi_idx = []
            channel_Score = dict({})
            for index in range(len(feature)):
                if channels[index] == 'HOE':
                    continue
                if channels[index] == 'marker':
                    continue
                if channels[index] not in selectComputedChannel:
                    continue
                channel_data = dict({})
                foi_idx = []
                ch_feature = feature[index]
                [freq,pxx]  = signal.welch(ch_feature, fs, nperseg=psd_size, average="median", window='hann')
                freq = freq[0: 150]
                pxx = pxx[0: 150]
                count = 0
                # plt.cla()
                for idx in range(len(freq)):
                    freqi = freq[idx]
                    if count >= len(xtick):
                        break
                    if freqi - xtick[count] < 0.1 and freqi - xtick[count] > 0:
                        count += 1
                        foi_idx.append(idx)
                zScore, patsnr = self.zsnr(np.array(pxx), foi_idx, numMeanPlus)
                # for i in foi_idx:
                #     freqi = freq[i]
                #     plt.axvline(freqi, linestyle='dashed', color='red')
                # plt.ylim(0, np.max(patsnr))
                # plt.plot(freq, patsnr)
                
                stringScore = []
                zScore = zScore.tolist()
                for id in range(len(zScore)):
                    stringScore.append([xtick[id], round(zScore[id], 2)])
                base, odd = self.count164z(stringScore,channels, float(message['data']['basefrequency']), float(message['data']['ZScore']))
                channel_data['base'] = base
                channel_data['odd'] = odd
                channel_data["zScore"] = stringScore
                channel_data['freq'] = freq.tolist()
                channel_data['patsnr'] = patsnr.tolist()
                channel_data['freq-index'] = foi_idx
                channel_data['xtick'] = xtick
                channel_Score[channels[index]] = channel_data
                # plt.xlabel(stringScore)
                # plt.title(channels[index],loc='left')
                # plt.show()
                # plt.savefig(imagesdir+'/'+ str(index)+'-'+str(headerInfo[index]) + '.jpg')
                # imagePath.append(imagesdir+'/'+ str(index)+'-'+str(headerInfo[index]) + '.jpg')
            # return imagePath
            print('file', file)
            file = file.replace('/data/', '/result/').replace(".mat", '-result.json')
            with open(file, "w") as f:
                json.dump(channel_Score, f)
            f.close()
            # sio.savemat(file, json.dumps(channel_Score)) 
            return 'ok'

if __name__ == '__main__':
    res = Result()
    res.drawImages('')