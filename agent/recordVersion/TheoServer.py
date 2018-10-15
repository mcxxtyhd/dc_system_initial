# 导入 socket、sys 模块
import socket

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
    def initServer(self, maxNum, xmlAddress,pluginsPath):
        fatherName= 'agent'
        fatherAttri= 'address'
        sonName='isUpdate'
        # 绑定端口号
        self.serversocket.bind((getlocaladdress(), self.port))

        # 设置最大连接数，超过后排队
        self.serversocket.listen(maxNum)

        while True:
            # 建立客户端连接
            clientsocket, addr = self.serversocket.accept()

            # 获得agent端的ip地址
            agentAddress = addr[0]
            print("连接地址: %s" % str(agentAddress))

            # 加载配置文件
            xmlOperatorAll = xmlOperator(xmlAddress)
            # 查看是否有对应的IP地址，没有就增加
            xmlOperatorAll.addNewAgent(agentAddress,findAllPlugins(pluginsPath))

            # 获得agent端的是否需要更新的信息
            updateMsg = xmlOperatorAll.getDataByXml(agentAddress)
            updatePluginsNum=0
            print('更新信息：' + str(updateMsg))
            clientsocket.send(str(updateMsg).encode('utf-8'))

            # 如果该客户端需要更改，那么等待客户端更新完毕的响应
            for pluginName, isUpdate in updateMsg.items():
                if isUpdate == 'YES':
                    updatePluginsNum+=1

            # 如果有大于1说明有插件更新，那么就agent端一定会返回消息给服务端 返回的内容即更新的控件名称
            if updatePluginsNum>0:
                rebackData = clientsocket.recv(1024)
                rebackData = eval(rebackData.decode('utf-8'))
                # 修改xml文件，将对应的客户端地址的是否更新置为NO
                xmlOperatorAll.editDataByXml(agentAddress,rebackData)
                print('配置文件更新成功')

            clientsocket.close()

        self.serversocket.close()

    def getConnectToServer(self,serverPath,port):
        # 连接服务，指定主机和端口
        self.serversocket.connect((serverPath, port))

    # 从服务器获得信息
    def getMegFromServer(self):
        # 接收小于 1024 字节的数据
        msg = self.serversocket.recv(1024)
        msg = msg.decode('utf-8')
        # 对字符串数据进行格式化 将其变为字典格式
        msg = eval(msg)
        return msg

    # 发送更新成功的消息到服务器
    def sendMegToServer(self,updatedPlugins):
        self.serversocket.send(updatedPlugins.encode('utf-8'))


