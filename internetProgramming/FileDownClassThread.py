import os
import threading
import urllib.request
import zipfile

# 查看文件的下载进度
from decorator.timekill import clock
from util.deleteFolder import deleteFolderFile


class FileDownClass(threading.Thread):
    def __init__(self, url, path, filename):
        threading.Thread.__init__(self)
        self.url = url
        self.path = path
        self.filename = filename

    # 解压文件
    @staticmethod
    def extractFile(filepath,filepathWithOutZip):
        # 如果存在旧版本的就删除
        if os.path.exists(filepathWithOutZip):
            deleteFolderFile(filepathWithOutZip)

        myzip = zipfile.ZipFile(filepath)

        # 根据逗号分隔文件名
        mystr = myzip.filename.split(".")
        # 然后解压逗号前的文件名
        myzip.extractall(mystr[0])
        #关闭
        myzip.close()

        # 之后删除压缩包
        if os.path.exists(filepath):
            os.remove(filepath)

    @clock
    def run(self):

        def cbk(a, b, c):
            '''回调函数
            @a:已经下载的数据块
            @b:数据块的大小
            @c:远程文件的大小
            '''
            per = 100.0 * a * b / c
            if per > 100:
                per = 100
            print('%.2f%%' % per)

        print('-------------------------------------')

        # 1、从服务器上下载文件

        # 1.1拼凑保存的路径(带zip的)
        filepath = os.path.join(self.path, self.filename)

        # 1.1.1 拼凑不带zip的解压目录
        filepathWithOutZip=filepath[0:len(filepath)-4]

        # 1.2创建目录
        if not os.path.exists(self.path):
            os.mkdir(self.path)

        # 1.3第一个是下载文件的路径，第二个是保存的路径，第三个是回调函数
        urllib.request.urlretrieve(self.url, filepath, cbk)

        # 2、解压文件包
        FileDownClass.extractFile(filepath,filepathWithOutZip)

        print('组件更新成功')
        print('-------------------------------------')

