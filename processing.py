from brainflow.data_filter import DataFilter, FilterTypes, WindowOperations, DetrendOperations, AggOperations, NoiseTypes
import brainflow
import numpy as np 
import mne
class Processsing(object):
    def __init__(self):
        super(Processsing, self).__init__()
        self.name = 'processing'
        self.sampling_rate= 1000

    def detrend(self, data):
        for channel in range(len(data)):
            DataFilter.detrend(data[channel], DetrendOperations.LINEAR.value)

    def remove_environmental_noise(self, data):
        for channel in range(len(data)):
            DataFilter.remove_environmental_noise(data[channel], self.sampling_rate,NoiseTypes.FIFTY_AND_SIXTY)

    def filter(self, data, low, high):
        for channel in range(len(data)):
            DataFilter.perform_bandpass(data[channel], self.sampling_rate, low, high, 2,
                                                    FilterTypes.BUTTERWORTH, ripple= 0)
    
    def refrence(self, data):
        refrence_data = np.mean(data, axis=0)
        data = refrence_data
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
        mne_data.plot()
        
    # 暂未开启
    def ica(self, data, icaExcludeChannel):
        data = data.transpose(1,0,2)
    
    def processing(self, message):
        print(message)
