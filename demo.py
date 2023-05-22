def createProcessingScript(file_Path, channel, config, boardId, sampling_rate):
    print('this is create script')
    script1 = f"""
import numpy as np
import mne
from brainflow.data_filter import DataFilter, FilterTypes, WindowOperations, DetrendOperations, AggOperations, NoiseTypes
import brainflow
import pywt
from scipy import signal
features = []
files = {files}
channel = {channel}
config = {config}
boardId = {boardId}
sampling_rate = {sampling_rate}
features_label = []

def get_features(files, channel, config, boardId):
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
    for channel in range(len(eeg_data)):
        DataFilter.detrend(eeg_data[channel], DetrendOperations.LINEAR.value)

            """

    script3 = """"""
    if 'wlt_denoising' in config['checkList']:
        script3 = """
    # 对一维脑电进行相关去噪
    wlt_denoising = int(config['wlt_denoising'])
    if wlt_denoising== 1 or wlt_denoising==2:
        for channel in range(len(eeg_data)):
            DataFilter.remove_environmental_noise(
                eeg_data[channel], sampling_rate, NoiseTypes.FIFTY_AND_SIXTY)

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
    for channel in range(len(eeg_data)):
        DataFilter.perform_bandpass(eeg_data[channel], sampling_rate, config['low'], config['high'], 2,
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
        for channel in range(len(data)):
            DataFilter.perform_bandpass(data[channel], sampling_rate, config['samplelow'], config['samplehigh'], 2,
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
    print(script)
    filename = 'demo-script.py' # 指定保存的文件名

        # 打开文件并写入脚本内容
    with open(filename, "w") as file:
            file.write(script)
# 创建

def createFeatureScript(file):
     print('file')

def createDeepLearningScript(fileName):
     print('create DeepLearning script')
     
def createMechainLearningScript(file):
    print('createMechainLearningScript')

def createOnlineDetectionSystem(file):
    print('file')


files = ['aaa.csv', 'bbb.csf']
configs = {
        "checkList": ['detrend', 'wlt_denoising', 'trigger', 'badChannel','filter', 'refrence', 'sample','sample_filter','sample_detrend','down_sample'   ],
        "detrend": 1,
        "trigger": [],
        "low": 0,
        "high": 100,
        "triggers": [
          {
            "startTime": 0,
            "endTime": 0,
            "trigger": 0
          }
        ],
        "samplelow": 0.5,
        "samplehigh": 50,
        "sampleDetrendStart": '',
        "sampleDetrendEnd": '',
        "sampleDetrend": '0',
        "downSample": 200,
        "outPutType": 'npy',
        "ica": 0,
        "productId": 5,
        "badChannels": [],
        "refrenceChannel": [],
        "refrence": 0,
      }

channels = ['1', '2', '3', '4', '5', '6', '7', '8']
boardid = 5
sample_rate = 1000

# createProcessingScript(files, channels, configs, boardid, sample_rate)



import numpy as np
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

# 输入数据
eegData = np.random.rand(32, 1000)  # 示例数据，32个通道，1000个时间点

# 计算 EEG 共空间模式
eeg_pattern = eeg_spatial_pattern(eegData)

# 打印结果
print(eeg_pattern.shape, eegData.shape)
