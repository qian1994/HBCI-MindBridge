import socket
from threading import Thread 
import socket
import json
class SocketCustomClient(object):
    def __init__(self, mainThread = None):
        print('SocketCustomClient')
        self.name = 'SocketCustomClient'
        self.serve = None
        self.socThread = None
        self.mainThread = mainThread
        self.flag = False
    def init(self, ip, port):
        try:
            self.serve = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            self.serve.connect((ip, int(port)))
            self.serve.sendall(b'connect')
            self.socThread = Thread(target=self.startSock)
            self.socThread.start()
        except Exception as e:
            print('发生异常:', e)  
    def startSock(self):
        while True:
            # 接收客户端数据
            if self.flag == True:
                break
            try:
                data = self.serve.recv(1024)
                # 如果客户端已断开连接，则跳出循环
                if  data:
                    command = data.decode('utf-8')
                    command = json.loads(command)
                    self.recive(command)
            except Exception as e:
                self.stop()
                print('发生异常:', e)  
                break
    def recive(self, command):
        if 'action' not in command:
            return
        action = command['action']
        data = command['data']
        if action == 'start':
            print('开始执行指令...')
            # TODO: 执行开始指令的操作
            self.mainThread.getCustomInsertMarker({'action': 'start', 'data': ''})
        elif action == 'stop':
            print('停止执行指令...')
            # TODO: 执行停止指令的操作
            self.mainThread.getCustomInsertMarker({'action': 'stop', 'data': ''})
        elif action == 'trigger':
            print('接受打标命令', data)
            self.mainThread.getCustomInsertMarker({'action': 'trigger', 'data': data})
        else:
            print('接受命令', command)


    def stop(self):
        print('this is stop')
        self.flag = True
        self.socThread.join()
        self.socThread = None
        self.serve.close()
        # 关闭客户端连接
        self.serve = None
        self.socThread = None
        self.flag = False
        print('客户端已断开连接')
