import mne 
import matplotlib
import matplotlib.pyplot as plt
from pyedflib import highlevel
import numpy as np 
from brainflow import BoardShim

infile = './data/p300/BrainFlow-RAW_2022-12-31_16-59-19_0.fif'
# infile = './data/p300/BrainFlow-RAW_2022-12-31_16-59-19_0.bdf'
# infile = './data/svp1_2/922_2size_2023_04_05_20_06_56.fif'

raw = mne.io.read_raw(infile, preload=True)
raw.filter(l_freq=0.1, h_freq=40)
raw.plot()
plt.show()
# eeg = BoardShim.get_eeg_channels(532)
# print(eeg)
# signal , signal_header, header = highlevel.read_edf(infile)
# print(header)
# print(signal_header)
# print(signal)
# np.savetxt('./a.csv', signal.T)