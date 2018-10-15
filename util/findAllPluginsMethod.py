import os

def findAllPlugins(path):
    dirs = os.listdir(path)
    allPlugins=[]
    for dir in dirs:
        if dir[-4:] == '.zip':
            allPlugins.append(dir)
    return allPlugins

