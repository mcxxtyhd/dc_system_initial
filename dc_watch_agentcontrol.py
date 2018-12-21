import os
import re
import socket
import time
import requests

from util.getFileTargetConfigContent import getFileTargetConfigContent


def getlocaladdress(match_rule):
    # 下方代码为获取当前主机IPV4 和IPV6的所有IP地址(所有系统均通用)
    addrs = socket.getaddrinfo(socket.gethostname(),None)

    addressList='url:,'
    for item in addrs:
        addressList+=str(item[4][0])+','

    reg = r',('+match_rule+'),'
    imgre = re.compile(reg)
    imglist = re.findall(imgre, addressList)

    return imglist[0]

# 获取本机IP的正则表达式
match_rule = getFileTargetConfigContent('dc_system_agent.config', 'netgateRe=')

# 获得本机ip
local_address = getlocaladdress(match_rule)

# 服务器地址
server_address=str(getFileTargetConfigContent('dc_system_agent.config', 'server_address='))+':'+str(getFileTargetConfigContent('dc_system_agent.config', 'server_control_port='))

# 循环检测以及重连的间隔时间
time_load=5

while True:
    try:
        while True:
            # *****************************    1、检查是否需要启动客户端程序       *************************************
            print('get operatation action...')
            # 捏造参数，为了让服务器知道访问的IP是多少
            param_get={'agent_address':str(local_address)}
            # 制定的wepapi地址
            url_get = 'http://'+str(server_address)+'/getAgentAction'
            # 携带参数调用api
            result_get = requests.post(url_get,data=param_get)
            # 获得当前地址的控件信息
            plugins_update=result_get.json()["data"]

            print(r"agent's action:" + str(plugins_update))

            # 如果有操作才进入判断
            # 首先不为空
            if plugins_update:
                if plugins_update!='empty':
                    service_name=r'dc_agentcontrol'
                    task_name=r'dc_agentcontrol.exe'
                    # 开启
                    if plugins_update=='turnon':
                        print('turn on client service...')

                        # # 开启服务
                        os.system('sc start ' + service_name)
                    # 关闭
                    else:
                        print('client service had shut down!')
                        # 关闭服务
                        os.system('sc stop ' + service_name)
                        os.system('taskkill /F /IM ' + task_name)

            # *****************************    2、表明客户端响应完毕       *************************************
            # 捏造参数，为了让服务器知道访问的IP是多少
            param_agent = {'agent_address': str(local_address)}
            # 制定的wepapi地址
            url_agent = 'http://'+str(server_address)+'/postAgentReactDone'
            # 携带参数调用api
            result_react = requests.post(url_agent, data=param_agent)

            time.sleep(time_load)

    except Exception:
        print('************** Exception **************')
        print('can not connect to the server...')
        print('************** Exception **************')

    finally:
        print('try to reconnect to the server...')
        time.sleep(time_load)