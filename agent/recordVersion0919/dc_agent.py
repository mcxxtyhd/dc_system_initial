import os
import sys
import time
import traceback

import requests

from internetProgramming.FileDownClass import FileDownClass
from util.getlocalhostAddress import getlocaladdress

# 获得本机ip
local_address = getlocaladdress()

# 初始化控件放在服务器的地址
target_agent_address = "C:/TheoTestShell"

# 循环检测以及重连的间隔时间
time_load=5

while True:
    try:
        # 第一次连接，检查一下是否需要增加此agent节点的控件情况列表
        # 捏造参数，为了让服务器知道访问的IP是多少
        param_init={'agent_address':str(local_address)}
        # 制定的wepapi地址
        url_init = 'http://192.168.11.162:5001/initAgentPluginsSituation'
        # 携带参数调用api
        result_init = requests.post(url_init,data=param_init)

        while True:

            # *****************************    1、检查是否需要更新控件包       *************************************
            print('checking all plugins if need update...')
            # 捏造参数，为了让服务器知道访问的IP是多少
            param_get={'agent_address':str(local_address)}
            # 制定的wepapi地址
            url_get = 'http://192.168.11.162:5001/getAgentPluginsSituation'
            # 携带参数调用api
            result_get = requests.post(url_get,data=param_get)
            # 获得当前地址的控件信息
            plugins_update=result_get.json()["data"]
            if plugins_update:
                for plugin in plugins_update:

                    # 更新下载控件的方法
                    fc = FileDownClass('http://192.168.11.162:5000/' + str(plugin), "C:\\TheoTestShell", plugin)
                    fc.execute()
                    print('plugin of '+str(plugin)+' update successfully!')

                # 之后调用另外一个接口对该agent的数据进行更改
                update_param = {'agent_address':str(local_address),'update_plugins': str(plugins_update)}
                # 制定的wepapi地址
                url_update = 'http://192.168.11.162:5001/updateAgentPluginsSituation'
                # 携带参数调用api
                result_update = requests.post(url_update, data=update_param)
            else:
                print('there is no updated plugins')

            print('check done')

            # *****************************    2.1、检查是否需要更新配置文件       *************************************
            config_param={'agent_address':str(local_address)}
            # 指定的wepapi地址
            url_config = 'http://192.168.11.162:5001/getPluginConfig'
            # 携带参数调用api
            result_configs = requests.post(url_config, data=config_param)
            # 获得当前地址的控件信息
            plugins_configs = result_configs.json()["data"]

            # 初始化控件存放的地址
            for single_plugin_and_id,single_config in plugins_configs.items():
                target_update_config={}

                # 提取出控件的名称
                single_plugin_data=str(single_plugin_and_id).split(',')
                single_plugin =single_plugin_data[0]
                print(str(single_plugin)+' has '+str(single_config)+' need to be loaded...')

                # 读取文件的所有信息
                file_path=target_agent_address+r'/'+str(single_plugin)+r'/'+str(single_config)
                f = open(str(file_path), encoding='utf-8')
                config_messages = f.readlines()

                # 调用接口将此文件的数据保存至对应的文件
                # 1.AddressIP 2.配置文件id  3.控件名称 4.配置文件名称
                target_update_config.update({str(local_address)+','+single_plugin_data[1]+','+str(single_plugin)+','+str(single_config):config_messages})
                config_update_param = {'agent_address': str(target_update_config)}

                # 指定的wepapi地址
                url_update_config = 'http://192.168.11.162:5001/updatePluginConfig'
                # 携带参数调用api
                result_update_configs = requests.post(url_update_config, data=config_update_param)

                print(str(single_config)+'reload done')

            # *****************************    2.2、检查是否需要更新配置文件       *************************************
            manual_param = {'agent_address': str(local_address)}
            # 指定的wepapi地址
            url_config_manualupdate = 'http://192.168.11.162:5001/getConfigManualUpdateData'
            # 携带参数调用api
            result_config_manualupdate = requests.post(url_config_manualupdate, data=manual_param)
            # 获得当前地址的控件信息
            plugins_config_Data = result_config_manualupdate.json()["data"]

            # 获得的应该是一个字典类型  key为控件加文件名的组合 value为文件内容(列表格式)
            for single_config_name,single_config_data in plugins_config_Data.items():
                target_config_file_path=target_agent_address+r'/'+str(single_config_name)

                print(str(target_config_file_path)+'has been updated')

                with open(target_config_file_path, "r+", encoding='utf-8') as single_plugin_configfile:
                    read_data = single_plugin_configfile.read()
                    single_plugin_configfile.seek(0)
                    single_plugin_configfile.truncate()  # 清空文件
                    # 写数据
                    single_plugin_configfile.write(single_config_data)

                print(str(target_config_file_path) + 'update successfully!')

            # # *****************************    3、检查是否需要启动或者停止服务       *************************************
            # 之后调用另外一个接口对该agent的数据进行更改
            actions_param = {'agent_address':str(local_address)}
            # 指定的wepapi地址
            url_update = 'http://192.168.11.162:5001/getAgentPluginsAction'
            # 携带参数调用api
            result_actions = requests.post(url_update, data=actions_param)
            # 获得当前地址的控件信息
            plugins_update = result_actions.json()["data"]

            # 遍历每个需要操作的action
            for single_action_key,single_action_value in plugins_update.items():
                if single_action_value=='turnoff':
                    # 如果为关闭服务
                    # 取任务名称
                    task_name=single_action_key[single_action_key.rindex('/')+1:len(single_action_key)]
                    os.system('taskkill /F /IM ' + task_name)
                    print('shut down service：'+str(single_action_key))
                else:
                    # 开启服务
                    os.system('start ' + single_action_key)

                    print('turn on service：'+str(single_action_key))

            time.sleep(time_load)
    except Exception:
        print('************** Exception BEGIN**************')
        print('can not connect to the server...')
        print('************** detail **************')
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=100, file=sys.stdout)
        print('************** Exception END**************')

    finally:
        print('try to reconnect to the server...')
        time.sleep(time_load)

