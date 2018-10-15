# 导入 socket、sys 模块
import socket
import sys

# 创建 socket 对象
from util.getlocalhostAddress import getlocaladdress

serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)

# 绑定端口号
port = 5001
serversocket.bind((getlocaladdress(), port))

# 设置最大连接数，超过后排队
serversocket.listen(20)

while True:
    # 建立客户端连接
    clientsocket, addr = serversocket.accept()

    print("连接地址: %s" % str(addr))

    msg = '欢迎访问菜鸟教程！' + "\r\n"
    clientsocket.send(msg.encode('utf-8'))
    clientsocket.close()