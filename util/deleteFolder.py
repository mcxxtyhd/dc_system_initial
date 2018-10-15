import os
import shutil

# 如果文件夹存在 删除文件或者文件夹下面的所有内容
def deleteFolderFile(folderpath):
    if os.path.exists(folderpath):  # 判断文件夹是否存在
        shutil.rmtree(folderpath)
        # delList = os.listdir(folderpath )
        #
        # for f in delList:
        #     filePath = os.path.join( folderpath, f )
        #     shutil.rmtree(filePath,True)
        #     print ("文件夹: " + filePath +" 删除成功!")
        #
        # os.rmdir(folderpath)

# deleteFolderFile("C:\\TheoTestShellConfig")


