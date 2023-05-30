import numpy as np
import os
from matplotlib import pyplot as plt
from brainflow import data_filter, DataFilter, DetrendOperations, WindowOperations
from brainflow.data_filter import FilterTypes
from scipy import signal
from pyedflib import highlevel
import json
import scipy.io as sio
from scipy.io import loadmat
import math
from util import *
mode = ['1contrast', '2size', '3color', '4direction', '5spatial frequency', '6motion',
        '7object recognition', '8face', '9tool', '10familiar', '11self', '18shape']


class Result(object):
    def __init__(self):
        super(Result, self).__init__()
        self.dir_path = '.'
        self.dir_path = os.getcwd()
        self.dir_path = self.dir_path.replace("\\", "/", 5)

    def readAllFiles(self):
        return os.listdir('./edfFile/svp1_2')

    def getInfoByFileName(self, message):
        fileName = message['data']['fileName']
        fileName = fileName.replace('.edf', '.mat')
        fileName = fileName.replace('.bdf', '.mat')
        info = sio.loadmat(fileName)
        data_dict = {}
        info['data'] = ''
        for key in info.keys():
            if key[0] != '_':
                if isinstance(info[key], np.ndarray):
                    data_dict[key] = info[key].tolist()
                if key == 'badChannel':
                    if data_dict['badChannel'] and data_dict['badChannel'][0]:
                        data_dict['badChannel'] = data_dict['badChannel'][0][0][0].tolist(
                        )
                    else:
                        data_dict['badChannel'] = []
        return data_dict

    def getReportFileListSSVEP(self, message):
        pations = os.listdir('test_data')
        pationsTree = dict({})
        for dir in pations:
            if '.' in dir:
                continue
            files = []
            for file in os.listdir('test_data/'+dir):
                if '.' in file:
                    continue
                files.append(file)
            pationsTree[dir] = files
        return pationsTree

    def getImageByFileName(self, message):
        self.dir_path = os.getcwd()
        self.dir_path = self.dir_path.replace("\\", "/", 5)
        fileName = message['data'].replace('.edf', '')
        if fileName == '':
            return dict({"images": [], "trialInfo": ''})
        edffile = self.dir_path + '/edfFile/svp1_2/' + fileName + '.edf'
        signals, signal_headers, header = highlevel.read_edf(edffile)
        trialInfo = header['recording_additional']
        imagePath = self.dir_path + "/img/" + fileName + '/'
        if not os.path.exists(imagePath):
            return dict({"images": [], "trialInfo": trialInfo})
        images = os.listdir(imagePath)
        images = ','.join(
            [self.dir_path + "/img/" + fileName + '/' + i for i in images])
        return dict({"images": images, "trialInfo": trialInfo})

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

    def count164z(self, zScores, channels, baseFrequency, ZScoreStandard):
        countbase = 0
        countOdd = 0
        for item in zScores:
            if int(item[0] * 10) == int(baseFrequency * 10) and item[1] > ZScoreStandard:
                countbase = 1
            if int(item[0] * 10) != int(baseFrequency * 10) and item[1] > ZScoreStandard:
                countOdd += 1
        return countbase, countOdd

    def drawCsv(self, csvFile):
        print('csv file')

    def createReport(self, message):
        data = message['data']
        if 'pationcode' not in data:
            return 'fail'
        pationcode = data['pationcode']
        path = pationcode
        if data['time'] != '':
            path += '/' + data['time']
        currentRootPath = os.getcwd() + '/test_data/' + path
        paths = find_json_files(currentRootPath)
        if len(paths) == 0:
            return "no file"
        reports = []
        for filepath in paths:
            filepath = filepath.replace('\\', '/', 20)
            dactData = ''
            with open(filepath) as f:
                dactData = json.load(f)
            f.close()
            base = 0
            odd = 0
            for key in dactData.keys():
                if key == 'badChannel':
                    continue
                item = dactData[key]
                if type(item) != dict:
                    continue

                pathDir = filepath.split('/')
                pationcode = pathDir[len(pathDir) - 5]
                etime = pathDir[len(pathDir) - 4]
                mode = pathDir[len(pathDir) - 3]
                if item['base'] > 0:
                    base += 1
                if item['odd'] > 0:
                    odd += 1
            pScore = self.computedPScore(filepath, 6, 1.2)
            reports.append([pationcode, etime, mode, base, odd,
                           pScore['base'], pScore['odd'], pScore['avg'],  ''])
        storeData = [['pathoncode', 'time', 'mode', 'base', 'odd',
                      "base pscore", 'odd pscore', 'avg pscore', 'remarks']]
        storeData = np.concatenate(
            (np.array(storeData), np.array(reports)), axis=0)
        np.savetxt(os.getcwd() + '/test_data/' + path +
                   '/report.csv', storeData, delimiter=',', fmt='%s')
        return storeData.tolist()

    def getResultInfo(self, message):
        file = message['data']['fileName']
        data = sio.loadmat(file)
        return data

    def createPScore(self, message):
        print('this is create p score')

    def createImages(self, message):
        data = message['data']
        file = message['data']['file']
        zScore = data['zScore']
        label = data['label']
        stringScore = ''
        for item in zScore:
            stringScore += str(item[0]) + ":" + str(round(item[1])) + "    "
        fig = plt.figure()
        plt.title(label, loc='left')
        plt.xlabel(stringScore)
        for item in data['xtick']:
            plt.axvline(item, linestyle='dashed', color='red')
        plt.plot(data['freq'], data['patsnr'])
        fig.savefig(file.replace('-result.json', "-" + label+'.jpg'))
        return 'ok'
        # file = 'C:/Users/admin/Desktop/mindBridgeSoftware/HBCI/test_data/32_12/2023_04_19_11_01_08/6motion/result/FPVS-result.mat'
        # data = json.loads(file)
        # print(data)
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
        info = sio.loadmat(file.replace('.bdf', '.mat'))
        fs = info["sampleRate"][0][0]
        signals = info['data']
        channels = [channel.replace(' ', '', 10)
                    for channel in info['channels']]
        signals = signals.T
        signals = np.ascontiguousarray(signals)
        selectComputedChannel = message['data']['selectComputedChannel']
        rereference = message['data']['rereference']
        xtick = message['data']['frequency']
        baseFrequency = message['data']['baseFrequency']
        numMeanPlus = message['data']['number']
        labels = signals[-1]
        data = signals[:len(signals)-1]
        for index in range(len(data)):
            DataFilter.detrend(data[index], DetrendOperations.NO_DETREND.value)
            DataFilter.perform_bandpass(data[index], int(fs), message['data']['filterlow'], message['data']['filterHigh'], 2,
                                        FilterTypes.BUTTERWORTH.value, 0)
        if rereference:
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
                if trial_index == len(select_train) or trial_index > len(select_train) or int(select_train[trial_index]) == 0:
                    trial_index += 1
                    continue
                trial_index += 1
                index_start = int(index-float(startTrialTime)*fs)
                index_end = int(index + float(endTrialTime) * fs)
                subData = data[:, index_start:index_end]
                if subData.shape[1] == (startTrialTime + endTrialTime) * fs:
                    detrend_data = np.array([np.mean(
                        data[:, index-int(fs*float(message['data']['baseLineTime'])):index], axis=1)]).T
                    subData -= detrend_data
                    subData = subData[:, 0: message['data']
                                      ['paradigmTime'] * fs]
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
            [freq, pxx] = signal.welch(
                ch_feature, fs, nperseg=psd_size, average="median", window='hann')
            freq = freq[0: 150]
            pxx = pxx[0: 150]
            count = 0
            for idx in range(len(freq)):
                freqi = freq[idx]
                if count >= len(xtick):
                    break
                if freqi - xtick[count] < 0.1 and freqi - xtick[count] > 0:
                    count += 1
                    foi_idx.append(idx)
            zScore, patsnr = self.zsnr(np.array(pxx), foi_idx, numMeanPlus)
            stringScore = []
            zScore = zScore.tolist()
            for id in range(len(zScore)):
                stringScore.append([xtick[id], round(zScore[id], 2)])
            base, odd = self.count164z(stringScore, channels, float(
                message['data']['baseFrequency']), float(message['data']['ZScore']))
            channel_data['base'] = base
            channel_data['odd'] = odd
            channel_data["zScore"] = stringScore
            channel_data['freq'] = freq.tolist()
            channel_data['patsnr'] = patsnr.tolist()
            channel_data['freq-index'] = foi_idx
            channel_data['xtick'] = xtick
            channel_Score[channels[index]] = channel_data
            channel_Score['channels'] = channels
            channel_Score['base'] = message['data']['baseFrequency']

        file = file.replace(
            '/data/', '/result/').replace(".mat", '-result.json')
        with open(file, "w") as f:
            json.dump(channel_Score, f)
        f.close()
        return 'ok'

    # /
    #   input: file, basefreq_number, oddFreq_number
    #   output: pmin
    # /

    def computedPScore(self, fileName, basefreq_number, oddFreq_number):
        #  1: 获取每个电极的snr
        #  2: 计算 1.2hz的snr 于 基础的正常人的电极的个数
        #  3：计算 6hz 的snr 于 基础的正常人的电极个数
        #  4：计算 谐频率的均值  于 基础的正常人的 电极个数
        #  每个电极除以对应的正常人的个数   50 - NAN
        #  将每个电极重新进行平均，然后 * 100 得到p分数
        # basefreq = []
        # oddbalfreq = []
        # oddavg = []
        basefreq_number = basefreq_number
        oddFreq_number = oddFreq_number
        hs_SNRdata = loadmat('./hs_SNRdata.mat')
        # print(hs_SNRdata)
        # for item in hs_SNRdata["hs_SNRdata"][0][0]:
        # print(item.shape)
        basefreq = hs_SNRdata["hs_SNRdata"][0][0][0]
        oddbalfreq = hs_SNRdata["hs_SNRdata"][0][0][1]
        oddavg = hs_SNRdata["hs_SNRdata"][0][0][6]
        channels = hs_SNRdata["hs_SNRdata"][0][0][7]
        info_channel = dict({})
        count = 0
        for channel in channels:
            info_channel[channel[0][0]] = count
            count += 1
        # print(info_channel)
        # fileName = message['data']['fileName']
        fileName_array = fileName.split('/')
        current_mode = mode.index(fileName_array[len(fileName_array) - 3])
        with open(fileName) as f:
            data = json.load(f)
        pScoresByChannel = {}
        for key in data:
            if key in info_channel:
                index = info_channel[key]
                basefreq_current = basefreq[0][current_mode][index]
                oddbalfreq_current = oddbalfreq[0][current_mode][index]
                oddavg_current = oddavg[0][current_mode][index]
                # print(basefreq_current.shape, oddbalfreq_current.shape, oddavg_current.shape)
                # print(data[key]['zScore'])
                pScorestand = dict({})
                pScorestand['oddavg_avg'] = 0
                for item in data[key]['zScore']:
                    if item[0] == basefreq_number:
                        pScorestand['basefreq_number'] = item[1]
                    elif item[0] == oddFreq_number:
                        pScorestand['oddFreq_number'] = item[1]
                    else:
                        pScorestand['oddavg_avg'] += item[1]
                pScorestand['oddavg_avg'] /= (len(data[key]['zScore']) - 2)
                current_data = 0
                count = 0
                pScores = {}
                current_data = 0
                for i in basefreq_current:
                    if not math.isnan(i):
                        if item[1] > i:
                            current_data += 1
                        count += 1
                pScores['base'] = [count, current_data]
                current_data = 0
                count = 0
                for i in oddbalfreq_current:
                    if not math.isnan(i):
                        if item[1] > i:
                            current_data += 1
                        count += 1
                pScores['odd'] = [count, current_data]
                current_data = 0
                count = 0
                for i in oddavg_current:
                    if not math.isnan(i):
                        if item[1] > i:
                            current_data += 1
                        count += 1
                pScores['avg'] = [count, current_data]
                pScoresByChannel[key] = pScores
        p_min = {
            'base': 0,
            'odd': 0,
            'avg': 0
        }
        for key in pScoresByChannel:
            pScoresByChannelData = pScoresByChannel[key]
            p_min['base'] += pScoresByChannelData['base'][1] / \
                pScoresByChannelData['base'][0]
            p_min['odd'] += pScoresByChannelData['odd'][1] / \
                pScoresByChannelData['odd'][0]
            p_min['avg'] += pScoresByChannelData['avg'][1] / \
                pScoresByChannelData['avg'][0]
        p_min['base'] /= len(pScoresByChannel.keys())
        p_min['odd'] /= len(pScoresByChannel.keys())
        p_min['avg'] /= len(pScoresByChannel.keys())

        p_min['base'] *= 100
        p_min['odd'] *= 100
        p_min['avg'] *= 100

        return p_min

# if __name__ == '__main__':
#     res = Result()
#     res.computedPScore('')
