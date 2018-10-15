# 导入 socket、sys 模块
import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 设置端口号
port = 5001

# 连接服务，指定主机和端口
s.connect(('192.168.11.165', 5001))

# 接收小于 1024 字节的数据
msg = s.recv(1024)

s.close()

print (msg.decode('utf-8'))