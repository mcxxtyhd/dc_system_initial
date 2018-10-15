from flask import Flask, jsonify, request
# 初始化数据库连接:
from agent_client import agent
import pymssql
import sys
import time
import traceback

from util.getlocalhostAddress import getlocaladdress

app = Flask(__name__)

# 获得本机ip
local_address = '192.168.11.229'

# 1.1 初始化客户端的控件情况数据
@app.route("/getTest", methods=["POST"])
def init_agent_plugin_situation():
    # 拿到访问的ip
    # agent_address = str(request.form.get("agent_address"))
    test_id = str(request.args.get("userid"))
    test_funcname = str(request.args.get("funcname"))

    if test_id=='33':
        if test_funcname=='mytest':
            print('1111')
            test_newvarchar = 'True'
        else:
            print('2222')
            test_newvarchar = 'False'
    else:
        print('3333:'+str(test_id))
        test_newvarchar = 'False'
    return test_newvarchar

if __name__ == "__main__":
    time_load=5

    while True:
        try:
            app.run(host=local_address, port=5001)
        except Exception:
            print('**************错误信息 开始**************')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback, limit=100, file=sys.stdout)
            print('**************错误信息 结束**************')
        finally:
            input('服务端运行失败...')
            time.sleep(time_load)
