import sys
import traceback
from aiohttp import web
from util.getlocalhostAddress import getlocaladdress

def download(request):
    r = web.FileResponse(request.match_info['fileName'])
    r.enable_compression()
    return r

def setup_routes(app):
    app.router.add_get('/{fileName}', download)

if __name__ == '__main__':
    try:
        # 获得本机ip
        local_address = '192.168.84.1'
        app = web.Application()
        setup_routes(app)
        web.run_app(app, host=local_address, port=5000)
    except Exception:
        print('**************错误信息 开始**************')
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=100, file=sys.stdout)
        print('**************错误信息 结束**************')
    finally:
        input('程序运行失败...')
