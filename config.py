impedence64 = [
    'FC1', 'FC3', 'C1', 'C3', 'FC5','C5','FT7','F9',
    'F7','F5','F3','F1','AF7','FPZ','AFZ','FP1',
    'FP2','FZ',"FCZ",'F2','AF8','F4','F6','F8',
    'F10','FT8','C6','FC6','C4','C2','FC4','FC2',
    'O1','P1','P3','P5','PO7','P7','LPA', "US",
    'P9','TP7','T7','CP5','CP3','CP1','CPZ','PZ',
    'POZ','CP2','CZ','CP4','CP6','T8 ','TP8','P10',
    'LPA','P8','P6','PO8','P2','P4','O2','OZ']

impedence23 = ["OZ", 'PZ','O1', "P3", "P7",'LPA',
              "T7", "F7", "F3", "C3", "FP1", "FPZ",
              "FP2", "F4", 'FZ',"F8", "T8", "US", 
              "P8", "O2", "P4", "C4", 'CZ', "RPA"]

impedence32 = ["O1", 'C3', "CP3", 'P3', "P7", "TP7", "T7","LPA", 
               "FT7", "F7", "FC3", "F3", "CZ", "FCZ", "FZ",'FP1',
               "FP2", "F4", "C4", "FC4","F8", "FT8", "P8", "RPA",
               "TP8", "T8", "CP4", "P4", "O2", "CPZ", "PZ", "OZ"]

impedence8 = ["FP1", 'FP2', "T7", 'CZ', "T8", "O1", "O2", "OZ"]

impedence16 = ["FP1", 'FP2', "FPZ","F7",  "FZ",  "F8",  
               "T7", "CZ", "T8", "P7", "PZ", "P8", "O1", "O2", "OZ"]

impedences = {
    "8": impedence8,
    "16": impedence16,
    "20": impedence23,
    "32": impedence32, 
    "64": impedence64
}

products = [{
    'name': 'MindBridge-8',
    'id': '5'
}, {
    'name': 'MindBridge-16',
    'id': "516"
}, {
    'name': 'MindBridge-32',
    'id': "532"
},
{
    'name': 'MindBridge-10-20',
    'id': "520"
}, {
    'name': 'MindBridge-64',
    'id': "564"
}]

class MindBridge(object):
    def __init__(self):
        self.channelImpedences = impedences
        self.products = products