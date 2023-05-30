import socket
import time
import json
# 创建TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定IP地址和端口号
server_address = ('127.0.0.1', 8888)
server_socket.bind(server_address)

# 设置最大连接数
server_socket.listen(1)

print('等待客户端连接...')

while True:
    # 等待客户端连接
    client_socket, client_address = server_socket.accept()
    print('客户端已连接:', client_address)

    try:
        while True:
            # 接收客户端发送的数据
            print('this is send action trigger')
            time.sleep(1)
            client_socket.sendall(json.dumps({"action": "trigger", "data": 1}).encode('utf-8'))
            # data = client_socket.recv(1024)
            # 处理接收到的数据
            # ...
            # 发送响应给客户端
            # response = '收到消息：' + data.decode()
            # client_socket.sendall(response.encode())
            
    except Exception as e:
        print('发生异常:', e)
        
    finally:
        # 关闭客户端连接
        client_socket.close()
        print('客户端已断开连接')
