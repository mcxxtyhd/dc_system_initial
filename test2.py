import os
a_path=r'D:\pythonProject\testDeploy\pluginFirst22222.zip'

if os.path.exists(a_path):
    print(str(a_path)+',is existed!')
    #do something
else:
    print(str(a_path) + ',not exists!')
