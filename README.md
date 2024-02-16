# HBCI

## Overview

The importance of high-quality software tools for advancing EEG research cannot be overstated. However, to our knowledge, there is a lack of an open-source EEG software platform that can cover information acquisition, visualization, and processing analysis and whose development is built on easy-to-learn high-level language. Moreover, many of the current powerful software packages are therefore commercial and lack certain third-party functionality extensions. Therefore, this study proposes the hybrid brain-computer interface (HBCI), a new and more flexible Python-based software tool consisting of four main modules: an EEG amplifier, a BCI paradigm, EEG data storage and EEG data analysis. An EEG amplifier compatible with the MindBridge-Nano (developed by Guangzhou Qianga Neuroscience Technology Co., Ltd.) hardware platform was used for real-time data acquisition and processing. The BCI paradigm facilitates the rapid integration of third-party paradigms and BCI experimental stimuli. EEG Data Storage is dedicated to data storage and online/offline visualization, while EEG data analysis provides various methods of data processing and analysis. The software platform in this study has several notable advantages: (i) comprehensive capabilities in terms of data collection, storage, processing, and visualization, effectively addressing the complexity of data processing and reducing the learning curve; (ii) support for data format conversion between CSV, OpenBCI, MNE, and EDF, enhancing the efficiency of EEG data sharing; (iii) leveraging Python and Matplotlib for rapid and high-quality real-time visualization of temporal, spectral, and spatial EEG data, providing users with intuitive feedback; and (iv) providing interfaces for third-party paradigms such as SSVEP, P300, and MI, demonstrating good extensibility. This enables researchers to quickly engage in BCI research analysis and inspires more ideas from the BCI community. The HBCI holds significant promise and significance in scientific research and brain information analysis.

See the document "HBCI_user_manual.pdf" for more information.

## Installation

This system uses python as the basic development language, uses PyQt5 as the underlying interface framework, and uses the hybrid development of h5+python, which enables h5 to edit the interface efficiently. In the real-time image display, matplotlib is used as the third-party image library. When python is running, multi-process is used to separate the real-time image interface and operation interface to ensure the efficient operation of the system. The h5 development uses the interface framework of vue for development, and JSBridge is used for communication between h5 and python.

```
python == 3.8.4
node == v12.22.12
VUE == 2.6.11
```

add python package

```
$ pip install -r requirements.txt
Then:
$ python app.py

```

edit home pages

```
edit home page 
$ cd main 
$ npm install 
Then
$ npm build 
```

same as edit data processing, impedance , convert file


## License

This software is licensed under the MIT license. For more information, read the file [MIT](https://choosealicense.com/licenses/mit/)

## Funding information

This work was partially supported by the STI 2030-Major Projects under grant 2022ZD0208900, the National Natural Science Foundation of China under grant 62076103, and the Major Projects of Colleges and Universities in Guangdong Province under grant 2023ZDZX2021.