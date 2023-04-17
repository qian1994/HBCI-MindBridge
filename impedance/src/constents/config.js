
const products = [{
    name: 'MindBridge-8',
    id: 5
}, {
    name: 'MindBridge-16',
    id: "516"
}, {
    name: 'MindBridge-32',
    id: "532"
}, {
    name: 'MindBridge-64',
    id: "564"
}]

const impedence64 = [
    'FCZ', 'FC2', 'FC4', 'FC6', 'FT8',
    'T7',
    'C5',
    'C3',
    'C1',
    'CZ',
    'C2',
    'C4',
    'C6',
    'T8',
    'M1',
    'TP7',
    'CP5',
    'CP3',
    'CP1',
    'CPZ',
    'CP2',
    'CP4',
    'CP6',
    'TP8',
    'M2',
    'P7',
    'P5',
    'P3',
    'P1',
    'PZ',
    'P2',
    'P4',
    'P6',
    'P8',
    'PO7',
    'PO5',
    'PO3',
    'POZ',
    'PO4',
    'PO6',
    'PO8',
    'CB1',
    'O1',
    'OZ',
    'O2',
    'CB2',
    'HEO',
    'VEO']

const impedence23 = ["FP1", 'FP2', "F7", 'F3', "FZ", "F4", "F8", "A1", "T3", "C3", "CZ", "C4", "T4", "A2", "T5", "P3", "PZ", "P4", "T6", "O1", "OZ", "O2"]

const impedence32 = ["FP1", 'FP2', "F7", 'F3', "FZ", "F4", "F8","FT7", "FC3", "FCZ", "FC4", "FT8", "A1", "T3", "C3", "CZ", "C4", "T4", "A2","TP7", "CP3", "CPZ", "CP4", "TP8", "T5", "P3", "PZ", "P4", "T6", "O1", "OZ", "O2"]

const impedences = {
    "23": impedence23,
    "32": impedence32, 
    "64": impedence64
}
const models = ['1contrast', '2size', '3color']
export default { products, models, impedences }