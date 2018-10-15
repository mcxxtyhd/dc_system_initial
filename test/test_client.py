import os
import sys
import time
import traceback

import requests

from util.getlocalhostAddress import getlocaladdress

# 获得本机ip
local_address = getlocaladdress()

# 第一次连接，检查一下是否需要增加此agent节点的控件情况列表
# 制定的wepapi地址
url_init = 'http://192.168.11.229:5001/getTest?userid=33&funcname=mytest'

# 携带参数调用api
result_init = requests.post(url_init)

# 获得当前地址的控件信息
plugins_configs = result_init.text

print("here is the data:"+str(plugins_configs))


