import numpy as np 
from brainflow.data_filter import DataFilter, FilterTypes, WindowOperations, DetrendOperations
from scipy import signal
import os
import sklearn
from sklearn.preprocessing import StandardScaler as scaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import Perceptron
from sklearn.neighbors import KNeighborsClassifier
import joblib
from PyQt5.QtCore import QDir
from pyedflib import highlevel
import json
from brainflow import board_shim, BrainFlowInputParams
def preprocess(data, name):
    if data is None:  # val/test can be empty
        return None
    feature, labels = data
    feature = abs(feature)
    print('feature',feature)
    feature = feature.reshape(len(feature), -1)
    # Scale to mean 0 and std 1.
    if name == "train":
        scaler.fit(feature)
    feature = scaler.transform(feature)
    # Shuffle train set.
    if name == "train":
        feature, labels = sklearn.utils.shuffle(feature, labels)
    return [feature, labels]

class P300Model(object):
    def __init__(self):
        super(P300Model, self).__init__()
        self.characters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','1','2','3','4','5','6','7','8','9','_']
        self.number = ['0','1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.board = None
    def predict(self,data, channels, samplate_rate):
        origin_data = self.feature(data, channels, samplate_rate)
        test_data = []
        keys = list(origin_data.keys())
        for key in keys:
            test_data.append(origin_data[key])
        pre1 = self.model1.predict(np.array(test_data))
        pre4 = self.model4.predict(np.array(test_data))
        pre = pre4 + pre1
        preb = self.model4.predict_proba(np.array(test_data))
        res = np.where(pre == 0)
        max_num = 0
        max_index = 0
        sec_num = 0
        sec_index = 0
        problity = preb[res, 0][0]
        if len(problity) < 2:
            numb_index = 0
            return self.characters[numb_index]
        for i in range(len(problity)):
            if problity[i] > max_num:
                max_index = i 
                max_num = problity[i]
        for j in range(len(problity)):
            if problity[j] > sec_num and j != max_index:
                sec_index = j 
                sec_num = problity[j]
        num1= keys[res[0].tolist()[max_index]]
        num2= keys[res[0].tolist()[sec_index]]
        max_num = int(num1%100)
        min_num = int(num2%100)
        numb_index = 0
        if max_num > min_num:
            numb_index =  max_num - 7 + (min_num-1) * 6
        else:
            numb_index =  min_num - 7 + (max_num-1) * 6
        if numb_index < 0 or numb_index >= len( self.characters):
            numb_index = 0

        return self.characters[numb_index]
    
    def feature(self, data, channels, samplate_rate):
        data = data.T
        label = data[-1]
        data = data[channels]
        origin_data = np.mean(data, axis=0)
        data_mean = np.mean(origin_data)
        data_std = np.std(origin_data)
        origin_data = (origin_data-data_mean)/data_std
        origin_data = np.array(origin_data.tolist())
        DataFilter.detrend(origin_data, DetrendOperations.CONSTANT.value)
        DataFilter.calc_stddev(origin_data)
        for channel in range(len(origin_data)):
            DataFilter.detrend(origin_data[channel], DetrendOperations.NO_DETREND.value)
            DataFilter.remove_environmental_noise(origin_data[channel], 1000, noise_type=1)
            DataFilter.perform_bandpass(origin_data[channel], 1000, 1.5, 24, 4,
                                                    2, ripple= 0)
        # def_data = mne.filter.filter_data(origin_data, sfreq=samplate_rate, l_freq=0.5, h_freq=1.5, verbose=False)
        # origin_data = mne.filter.filter_data(origin_data, sfreq=samplate_rate, l_freq=0.5, h_freq=24, verbose=False)
        # origin_data = origin_data - def_data
        json = dict({})
        for i in range(len(label)):
            if label[i] > 0:
                if json.get(label[i]) != None:
                    data = np.array(json[label[i]])
                    data += signal.resample(origin_data[i+int(samplate_rate* 0.1): i+int(samplate_rate*0.8)], 300).tolist()
                    json[label[i]] = data.tolist()
                else:
                    json[label[i]] = signal.resample(origin_data[i+int(samplate_rate* 0.1): i+int(samplate_rate*0.8)], 300).tolist()
        return json

    def cumpute_index(self, targetWords):
        targetIndex = dict({})
        train_character_index = []
        for index in range(len(self.characters)):
            targetIndex[self.characters[index]] = [int(index/6)+1, int(index%6) + 6 + 1]
        for word in targetWords:
            train_character_index.append(targetIndex[word])
        return train_character_index
    
    def createModels(self, files, uiInfo):
        save_path_dir = QDir.currentPath() + '/models'
        if not os.path.exists(save_path_dir):
            os.makedirs(save_path_dir)
        save_path_dir = QDir.currentPath() + '/models/p300/'
        if not os.path.exists(save_path_dir):
            os.makedirs(save_path_dir)
        models = []
        modelsName = ['RandomForestClassifier', 'Perceptron', 'KNeighborsClassifier', 'SVC', 'DecisionTreeClassifier']
        target_data = []
        target_labe = []
        none_target_data = []
        none_target_labe = []
        train_data = []
        train_label = []
        for file in files:
            fileName = file.replace('.csv', '').replace('.bdf', '')
            edffile = QDir.currentPath() + '/data/p300/'+ fileName + '.bdf'
            signals, signal_headers, header =  highlevel.read_edf(edffile)
            trialInfo = header['recording_additional']
            data = np.loadtxt('./data/p300/'+file)
            info = json.loads(trialInfo)
            targetWords = info['words'].split(',')
            character_index = []
            character_index = self.cumpute_index(targetWords)
            productId = int(header['equipment'])
            board = board_shim.BoardShim(productId, BrainFlowInputParams())
            sample_rate = board.get_sampling_rate(productId)
            channels = board.get_eeg_channels(productId)
            features = self.feature(data, channels, sample_rate)
            for key in features.keys():
                trial_index = int(key/100) - 1
                cur_index = key%100 -1
                if cur_index in character_index[trial_index]:
                    target_data.append(features[key])
                    target_labe.append(1)
                    train_data.append(features[key])
                    train_label.append(1)
                else: 
                    none_target_data.append(features[key])
                    none_target_labe.append(0)
                    train_data.append(features[key])
                    train_label.append(0)
        shuffle_ix = np.random.permutation(np.arange(len(train_label)))
        train = np.array(train_data)[shuffle_ix]
        label = np.array(train_label)[shuffle_ix]
        train_set_data = train[0: int(len(train) * 0.8)]
        train_labels = label[0: int(len(label) * 0.8)]
        test_set_data = train[int(len(train) * 0.8): len(train)]
        test_labels = label [int(len(label) * 0.8): len(label)]
        train_set = [train_set_data, train_labels]
        test_set = [test_set_data, test_labels]
        for index_model in range(len(models)) :
            model = models[index_model]
            model = model()
            name = modelsName[index_model]
            if name  not in uiInfo['trainModel']:
                continue
            processed_train_data = preprocess(train_set, "train")
            processed_test_data = preprocess(test_set, "test")
            model.fit(*processed_train_data)
            test_data_scro, test_labels_scro = processed_test_data
            pre = model.predict(test_data_scro)
            acc = model.score(test_data_scro, test_labels_scro)
            joblib.dump(model, filename= QDir.currentPath() + '/models/p300/' + name + '.pkl')