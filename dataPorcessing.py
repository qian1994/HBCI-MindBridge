from brainflow.data_filter import DataFilter, FilterTypes, WindowOperations, DetrendOperations, AggOperations
import numpy as np 
class DataProcessing(object):
    def __init__(self) :
        super(DataProcessing, self).__init__()
        self.name = "dataprocessing"

    def handleFFt(self, boardData, sampling_rate):
        psd_size = DataFilter.get_nearest_power_of_two(sampling_rate)
        fftArray = []
        if boardData.shape[1] < psd_size:
            return []
        for channel in range(len(boardData)):
            psd_data = DataFilter.get_psd_welch(boardData[channel], psd_size, psd_size // 2,
                                                    sampling_rate,
                                                    WindowOperations.BLACKMAN_HARRIS.value)
            fftArray.append(psd_data)
        return fftArray
    # 滤波处理
    def handleFilter(self, boardData, sampling_rate, low, high, order, filter):
        data = []
        for channel in range(len(boardData)):
            DataFilter.detrend(boardData[channel], DetrendOperations.LINEAR.value)
            DataFilter.remove_environmental_noise(boardData[channel], sampling_rate, noise_type=1)
            DataFilter.perform_bandpass(boardData[channel], sampling_rate, low, high, order,
                                                    filter, ripple= 0)
            DataFilter.perform_bandstop(boardData[channel], sampling_rate, 48.0, 52.0, 2,
                                        FilterTypes.BUTTERWORTH.value, 0)
            DataFilter.perform_bandstop(boardData[channel], sampling_rate, 58.0, 62.0, 2,
                                                FilterTypes.BUTTERWORTH.value, 0)
            data.append(DataFilter.perform_downsampling(boardData[channel], 20, AggOperations.EACH.value))
        return data
        return boardData
    