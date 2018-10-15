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
local_address = '192.168.84.1'

theo = agent(local_address, '1434', 'dc_system', 'sa', '123')

# 1.1 初始化客户端的控件情况数据
@app.route("/initAgentPluginsSituation", methods=["POST"])
def init_agent_plugin_situation():
    # 拿到访问的ip
    agent_address=str(request.form.get("agent_address"))
    # 拿到访问的计算机名称
    agent_name = str(request.form.get("agent_name"))

    theo.init_agent_plugins(agent_address,agent_name)

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

# 1.1.1 附件读取完毕  给服务端一个响应信息
@app.route("/postTargetPluginReactDone", methods=["POST"])
def update_agent_plugin_react_done():
    # 拿到访问的ip
    agent_address=str(request.form.get("agent_address"))

    # 去数据库更新 控件情况
    theo.update_agent_plugins_react_done(agent_address)

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

# 2.3 配置文件更新部分同服务器同步完毕
@app.route("/postConfigReactDone", methods=["POST"])
def update_target_configs_situation():
    # 拿到访问的ip
    agent_ipaddress=str(request.form.get("agent_address"))

    # 执行更新操作
    theo.configs_done_reaction(agent_ipaddress)

    return jsonify({"data":'successfully'})

# 3.1 客户端连接服务端获取控件服务的操作动作信息
@app.route("/getAgentPluginsAction", methods=["POST"])
def get_agent_plugin_situation_action():
    # 拿到访问的ip
    agent_address=str(request.form.get("agent_address"))

    agent_actions=theo.get_agent_plugins_action(agent_address)
    return jsonify({"data": agent_actions})

# 4.1 获得客户端所有的进程名称
@app.route("/postAgentTaskPlugins", methods=["POST"])
def get_all_task_list():
    # 拿到访问的ip
    agent_address=str(request.form.get("agent_address"))
    # 拿到所有的进程信息
    tasks_list = request.form.get("tasks_list")

    # 根据目标客户端的服务  同所有的进程列表进行匹配
    theo.update_target_agent_services(agent_address,tasks_list)
    return jsonify({"data": 'successfully'})

# 5  更新客户端的“上次响应时间”
@app.route("/updateAgentRequestTime", methods=["POST"])
def update_agent_lastrequesttime():
    # 拿到访问的ip
    agent_address=str(request.form.get("agent_address"))

    # 根据目标客户端的服务  同所有的进程列表进行匹配
    theo.update_agent_lastrequesttime(agent_address)
    return jsonify({"data": 'successfully'})


# 10.1 获取客户端程序的操作
@app.route("/getAgentAction", methods=["POST"])
def get_agent_action():
    # 拿到访问的ip
    agent_address=str(request.form.get("agent_address"))

    agent_action=theo.get_target_agent_action(agent_address)
    return jsonify({"data": agent_action})

# 10.2 表明客户端完成响应
@app.route("/postAgentReactDone", methods=["POST"])
def post_agent_reaction():
    # 拿到访问的ip
    agent_address=str(request.form.get("agent_address"))

    agent_action=theo.post_agent_reaction_done(agent_address)
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
