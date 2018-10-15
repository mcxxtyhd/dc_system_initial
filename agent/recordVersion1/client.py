import sys
import time
import traceback
from agent.recordVersion.TheoServerThread import AgentServer
from internetProgramming.FileDownClass import FileDownClass

try:
    while True:
        # 初始化agent端
        localserver = AgentServer(5002, 15)
        localserver.getConnectToServer('192.168.11.165', 5001)

        # 从服务端获取配置信息
        updateMsg = localserver.getMegFromServer()
        print('本地插件状态：'+str(updateMsg))
        # 对字符串数据进行格式化 将其变为字典格式
        updateMsg=eval(str(updateMsg))

        # 初始化控件更新记录
        updatedPlugins=[]
        updatePluginsNum = 0

        # 查找对应的插件是否需要更新
        for pluginName, isUpdate in updateMsg.items():
            if isUpdate=='YES':
                print('开始更新组件:'+pluginName)

                fc = FileDownClass('http://192.168.11.165:5000/'+str(pluginName), "C:\\TheoTestShell",pluginName)
                fc.execute()

                # 记录更新的控件
                updatedPlugins.append(pluginName)
                updatePluginsNum+=1

            else:
                print('-------------------------------------')
                print(pluginName+'组件无需更新')
                print('-------------------------------------')

        # # 如果有更新 就发送客户端更新成功的信息
        if len(updatedPlugins)>0:
            localserver.sendMegToServer(str(updatedPlugins))
        else:
            localserver.sendMegToServer('noUpdate')

        # 从服务端获取信息  表示这次agent连接完成  可以进行下一次循环了
        updateMsg = localserver.getMegFromServer()
        print(updateMsg)

        localserver.serversocket.close()

        # 循环检查是否有服务端发过来的消息
        time.sleep(localserver.checkPer)

except Exception:
    print('**************错误信息 开始**************')
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback,limit=100, file=sys.stdout)
    print('**************错误信息 结束**************')
finally:
    input('程序运行失败...')

