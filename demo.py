import numpy as np
import matplotlib.pyplot as plt
import mne
from mne import create_info
from mne.io import RawArray
from mne_realtime import RtEpochs, MockRtClient

# 创建随机数据
sfreq = 250
ch_names = ['Fz', 'Cz', 'Pz']
ch_types = ['eeg'] * 3
info = create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)
plt.show(block=False)
while True:
    # Acquire new data
    raw = RawArray(np.random.randn(len(ch_names), sfreq * 5), info)
    raw.plot(block=False, show=False)
    plt.pause(1)
# # # 创建实时数据流
# client = MockRtClient(raw)
# rt_epochs = RtEpochs(client, event_id=1, tmin=-0.1, tmax=1.0)

# # 创建绘图窗口
# fig, ax = plt.subplots(1, 1)
# lines = ax.plot(rt_epochs.times, np.zeros([len(rt_epochs.ch_names), len(rt_epochs.times)]))[0]


# # # 实时更新绘图
# # for epoch in rt_epochs.iter_evoked():
# #     data = epoch.data
# #     lines.set_ydata(data.T)
# #     plt.draw()
# #     plt.pause(0.001)




# import numpy as np
# import matplotlib.pyplot as plt
# from mne.viz import plot_topomap

# # Create empty EEG data and channel locations
# ch_names = ['Fp1', 'Fp2', 'C3', 'C4', 'P3', 'P4', 'O1', 'O2']
# ch_locs = np.random.rand(len(ch_names), 2) * 10  # random locations
# data = np.zeros(len(ch_names))

# # Create figure and axes
# fig, ax = plt.subplots()
# map_ax = plt.axes([0.7, 0.1, 0.25, 0.25])

# # Plot topomap
# plot_topomap(data, ch_locs, show=False, axes=map_ax)

# # Show figure
# plt.show(block=False)
# def update_data(new_data):
#     data[:] = new_data
#     plot_topomap(data, ch_locs, show=False, axes=map_ax, contours=0)
#     fig.canvas.draw_idle()

# # Example usage

# while True:
#     # Acquire new data
#     new_data = np.random.rand(len(ch_names))
    
#     # Update EEG data and redraw topomap
#     update_data(new_data)
    
#     # Pause to allow time for drawing
#     plt.pause(0.1)