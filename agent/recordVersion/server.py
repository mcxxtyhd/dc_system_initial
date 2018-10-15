import sys
import traceback

from agent.recordVersion.TheoServer import AgentServer

try:
    localserver=AgentServer(5001,10)
    localserver.initServer(50, 'D:\\pythonProject\\testDeploy\\config\\config.xml',"D:\\pythonProject\\testDeploy")

except Exception:
    print('**************错误信息 开始**************')
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback,limit=100, file=sys.stdout)
    print('**************错误信息 结束**************')
finally:
    input('程序运行失败...')


