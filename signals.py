from PyQt5.QtCore import QDir, QTimer, Qt, QObject
from PyQt5.QtCore import pyqtSignal
def Singletonfunc(cls):
    _instance = {}
    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]
    return _singleton
@Singletonfunc
class Signal(QObject):
    _mainClose = pyqtSignal(str)
