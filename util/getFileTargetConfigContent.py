import re

def getFileTargetConfigContent(file_path,config_name):
    f = open(file_path, "r")
    lines = f.readlines()  # 读取全部内容 ，并以列表方式返回
    match_rule=str(config_name)+r"(.*)"
    for line in lines:
        imgre = re.compile(match_rule)
        imglist = re.findall(imgre, line)
        if imglist:
            return imglist[0]

