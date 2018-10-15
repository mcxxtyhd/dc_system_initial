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
local_address = '192.168.11.162'

theo = agent(local_address, '1434', 'dc_system', 'sa', '123')

# 1.1 初始化客户端的控件情况数据
@app.route("/initAgentPluginsSituation", methods=["POST"])
def init_agent_plugin_situation():
    # 拿到访问的ip
    agent_address=str(request.form.get("agent_address"))

    theo.init_agent_plugins(agent_address)

    return 'init successfully'

# 1.2 获得当前客户端的控件情况更新数据
@app.route("/getAgentPluginsSituation", methods=["POST"])
def get_agent_plugin_situation():
    # 拿到访问的ip
    agent_address=str(request.form.get("agent_address"))

    need_update_plugins=theo.get_agent_updatedplugins(agent_address)
    return jsonify({"data": need_update_plugins})

# 1.3 对更新了的控件信息在数据库中进行保存
@app.route("/updateAgentPluginsSituation", methods=["POST"])
def update_agent_plugin_situation():
    # 拿到访问的ip
    agent_address=str(request.form.get("agent_address"))
    plugins_update = str(request.form.get("update_plugins"))
    plugins_update=eval(plugins_update)

    # 去数据库读取当前ip需要更新的控件信息
    theo.update_agent_plugins(agent_address,plugins_update)

    return 'update successfully'

# 2.1.1客户端获取是否有配置文件更改的要求
@app.route("/getPluginConfig", methods=["POST"])
def get_agent_plugin_configs_situation():
    # 拿到访问的ip
    agent_address=str(request.form.get("agent_address"))

    agent_configs=theo.get_agent_plugins_config(agent_address)
    return jsonify({"data": agent_configs})

# 2.1.2 保存传来的文件内容
@app.route("/updatePluginConfig", methods=["POST"])
def update_agent_plugin_configs():
    # 拿到访问的ip
    agent_config_update_data=str(request.form.get("agent_address"))

    # 执行更新操作
    theo.update_agent_config(agent_config_update_data)

    return jsonify({"data": 'successfully'})

# 2.2.1 获得所需要更新的配置文件的内容
@app.route("/getConfigManualUpdateData", methods=["POST"])
def get_plugin_configs_data():
    # 拿到访问的ip
    agent_ipaddress=str(request.form.get("agent_address"))

    # 执行更新操作
    targets_config_content=theo.get_target_configs_data(agent_ipaddress)

    return jsonify({"data":targets_config_content})

# 3.1 客户端连接服务端获取控件服务的操作动作信息
@app.route("/getAgentPluginsAction", methods=["POST"])
def get_agent_plugin_situation_action():
    # 拿到访问的ip
    agent_address=str(request.form.get("agent_address"))

    agent_actions=theo.get_agent_plugins_action(agent_address)
    return jsonify({"data": agent_actions})

# 10.1 获取客户端程序的操作
@app.route("/getAgentAction", methods=["POST"])
def get_agent_action():
    # 拿到访问的ip
    agent_address=str(request.form.get("agent_address"))

    agent_action=theo.get_target_agent_action(agent_address)
    return jsonify({"data": agent_action})


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
