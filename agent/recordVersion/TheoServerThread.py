# 导入 socket、sys 模块
import socket
import sys
import threading
import time
import traceback

from util.findAllPluginsMethod import findAllPlugins
from util.getlocalhostAddress import getlocaladdress
from xmlDemo.xmlOperator import xmlOperator


class AgentServer:
    # 初始化服务器
    def __init__(self,port,checkPer):
        self.port = port
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket = serversocket
        self.checkPer = checkPer

    # 开启服务器
    def initServer(self, maxNum):
        # 绑定端口号
        self.serversocket.bind((getlocaladdress(), self.port))

        # 设置最大连接数，超过后排队
        self.serversocket.listen(maxNum)

    def getConnectToServer(self,serverPath,port):
        # 连接服务，指定主机和端口
        self.serversocket.connect((serverPath, port))

    # 从服务器获得信息
    def getMegFromServer(self):
        # 接收小于 1024 字节的数据
        msg = self.serversocket.recv(1024)
        msg = msg.decode('utf-8')
        # # 对字符串数据进行格式化 将其变为字典格式
        # msg = eval(msg)
        return msg

    # 发送更新成功的消息到服务器
    def sendMegToServer(self,updatedPlugins):
        self.serversocket.send(updatedPlugins.encode('utf-8'))


class serverThreadOperator(threading.Thread):
    def __init__(self, agentServer,xmlAddress,pluginsPath,lock):
        threading.Thread.__init__(self)
        self.AgentServer = agentServer
        self.xmlAddress = xmlAddress
        self.pluginsPath = pluginsPath
        self.lock = lock

    def run(self):
        try:
            while True:
                print('-------------------------------------')

                # 建立客户端连接
                clientsocket, addr = self.AgentServer.serversocket.accept()

                # 获得agent端的ip地址
                agentAddress = addr[0]
                print("连接地址: %s" % str(agentAddress))

                # 加载配置文件
                xmlOperatorAll = xmlOperator(self.xmlAddress)
                # 查看是否有对应的IP地址，没有就增加
                xmlOperatorAll.addNewAgent(agentAddress,findAllPlugins(self.pluginsPath))

                # 获得agent端的是否需要更新的信息
                updateMsg = xmlOperatorAll.getDataByXml(agentAddress)
                updatePluginsNum=0
                print('更新信息：' + str(updateMsg))
                clientsocket.send(str(updateMsg).encode('utf-8'))

                # 接受服务端更新的消息
                rebackData = clientsocket.recv(1024)
                rebackData = rebackData.decode('utf-8')

                # 如果是'noupdate'则说明客户端不需要更新
                if rebackData=='noUpdate':
                    print("连接地址: %s无需更新" % str(agentAddress))
                else:
                    rebackData=eval(rebackData)

                    # 上锁！
                    self.lock.acquire()
                    try:
                        # 加载配置文件(重新读取否则会有错)
                        xmlOperatorAll = xmlOperator(self.xmlAddress)
                        # 修改xml文件，将对应的客户端地址的是否更新置为NO
                        xmlOperatorAll.editDataByXml(agentAddress, rebackData)
                    finally:
                        # 改完了一定要释放锁:
                        self.lock.release()

                clientsocket.send(str('服务器操作完毕').encode('utf-8'))
                clientsocket.close()

        except Exception:
            print('**************错误信息 开始**************')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback, limit=100, file=sys.stdout)
            print('**************错误信息 结束**************')
        finally:
            input('程序运行失败...')
