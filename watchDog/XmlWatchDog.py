import time

from watchdog.events import (FileSystemEventHandler)
from watchdog.observers import Observer

from xmlDemo.xmlOperator import xmlOperator


class TheoEventHandler(FileSystemEventHandler):
    def __init__(self,fileOperator):
        self.fileOperator=fileOperator

    def on_any_event(self, event):
        pass

    # 创建文件的事件
    def on_created(self, event):
        # 操作的是压缩文件
        if str(event.src_path).endswith(r'.zip'):
            fileName = TheoEventHandler.getFileName(self, event.src_path)
            print('增加了'+str(fileName)+'控件')
            # 对指定的xml文件进行增加节点的操作
            self.fileOperator.addNewPlugin(fileName)


    # 删除文件的事件
    def on_deleted(self, event):
        # 操作的是压缩文件
        if str(event.src_path).endswith(r'.zip'):
            fileName=TheoEventHandler.getFileName(self, event.src_path)
            print('删除了' +str(fileName)+ '控件')
            # 对指定的xml文件对应节点进行删除的操作
            self.fileOperator.deletePlugin(fileName)

    @staticmethod
    def getFileName(self,inString):
        filePath = str(inString)
        beginIndex = filePath.rindex('\\')
        fileName = filePath[beginIndex + 1:len(filePath)]
        return fileName


class NoOperatorEventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        pass

    # 创建文件的事件
    def on_created(self, event):
        # 操作的是压缩文件
        if str(event.src_path).endswith(r'.zip'):
            fileName = TheoEventHandler.getFileName(self, event.src_path)
            print('增加了'+str(fileName)+'控件')


    # 删除文件的事件
    def on_deleted(self, event):
        # 操作的是压缩文件
        if str(event.src_path).endswith(r'.zip'):
            fileName=TheoEventHandler.getFileName(self, event.src_path)
            print('删除了' +str(fileName)+ '控件')

    @staticmethod
    def getFileName(self,inString):
        filePath = str(inString)
        beginIndex = filePath.rindex('\\')
        fileName = filePath[beginIndex + 1:len(filePath)]
        return fileName

# if __name__ == "__main__":
#     baseDir = r'D:\pythonProject\testDeploy'
#     # 需要操作的xml文件
#     fileOperator = xmlOperator(r'D:\\pythonProject\\testDeploy\\config\\config.xml')
#
#     event_handler = TheoEventHandler(fileOperator)
#     observer = Observer()
#     observer.schedule(event_handler, baseDir, recursive=True)
#     observer.start()
#     try:
#         while True:
#             time.sleep(2)
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()