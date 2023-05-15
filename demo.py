import mne

# 从文件加载原始数据
raw = mne.io.read_raw('your_data_file.fif', preload=True)

# 创建蒙太奇对象
montage = mne.channels.make_standard_montage('standard_1005')

# 应用蒙太奇
raw.set_montage(montage)

# 提取事件
events = mne.find_events(raw)

# 创建Evoked对象
evoked = mne.EvokedArray(data=raw.get_data(), info=raw.info, tmin=0)

# 创建拓扑图窗口
fig, ax = plt.subplots()

# 绘制脑电地形图
evoked.plot_topomap(times=[0], axes=ax, show=False)

# 显示绘图结果
plt.show()