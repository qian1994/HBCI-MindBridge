import socket
from threading import Thread 
import socket

class SocketCustomClient(object):
    def __init__(self, mainThread = None):
        print('SocketCustomClient')
        self.name = 'SocketCustomClient'
        self.serve = None
        self.socThread = None
        self.mainThread = mainThread
    def init(self, ip, port):
        try:
            self.serve = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            self.serve.connect((ip, int(port)))
            self.serve.sendall(b'connect')
            socThread = Thread(target=self.startSock, args=(self))
            socThread.start()
        except:
            print('error')
    def startSock(self):
            while True:
                # 接收客户端数据
                data = self.serve.recv(1024)
                # 如果客户端已断开连接，则跳出循环
                if  data:
                    command = data.decode('utf-8')
                    self.recive(command)

    def recive(self, command):
        if command == 'start':
            print('开始执行指令...')
            # TODO: 执行开始指令的操作
            self.mainThread.getCustomInsertMarker({'start': 1})
        elif command == 'stop':
            print('停止执行指令...')
            # TODO: 执行停止指令的操作
            self.mainThread.getCustomInsertMarker({'stop': 1})
        else:
            print('接受打标命令', command)
            self.mainThread.getCustomInsertMarker({'marker': command})

    def stop(self):
        self.socThread.join()
        self.socThread = None
        self.serve.close()
        # 关闭客户端连接
        print('客户端已断开连接')
