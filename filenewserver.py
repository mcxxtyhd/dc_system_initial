import re
import socket
import sys
import traceback
from aiohttp import web

from util.getFileTargetConfigContent import getFileTargetConfigContent

def download(request):
    r = web.FileResponse(request.match_info['fileName'])
    r.enable_compression()
    return r

def setup_routes(app):
    app.router.add_get('/{fileName}', download)

try:
    # 从配置文件获取对应的网关正则表达式信息
    local_address = getFileTargetConfigContent('server.config', 'localhost_address=')

    file_server_port= getFileTargetConfigContent('server.config', 'file_server_port=')

    app = web.Application()
    setup_routes(app)
    web.run_app(app, host=local_address, port=file_server_port)
except Exception:
    print('**************错误信息 开始**************')
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback, limit=100, file=sys.stdout)
    print('**************错误信息 结束**************')
finally:
    input('程序运行失败...')
