import sys
import threading
import traceback
from agent.recordVersion.TheoServerThread import AgentServer, serverThreadOperator

print('主线程线程开始')
try:
    # 初始化服务器
    localserver=AgentServer(5001,10)
    localserver.initServer(50)
    serverThreads=[]
    # 加了一个锁，防止xml文件误更新
    counter_lock = threading.Lock()

    for i in range(3):
        serverThread=serverThreadOperator(localserver,'D:\\pythonProject\\testDeploy\\config\\config.xml','D:\\pythonProject\\testDeploy',counter_lock)
        serverThread.start()
        serverThreads.append(serverThread)

    for t in serverThreads:
        t.join()
except Exception:
    print('**************错误信息 开始**************')
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback, limit=100, file=sys.stdout)
    print('**************错误信息 结束**************')
finally:
    input('程序运行失败...')
    print('主线程线程结束')





