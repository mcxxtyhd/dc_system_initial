import re
import socket

def getlocaladdress():
    # 下方代码为获取当前主机IPV4 和IPV6的所有IP地址(所有系统均通用)
    addrs = socket.getaddrinfo(socket.gethostname(),None)

    addressList='url:,'
    for item in addrs:
        addressList+=str(item[4][0])+','

    reg = r',(192.168.13.[0-9]{1,3}),'
    imgre = re.compile(reg)
    imglist = re.findall(imgre, addressList)

    if imglist:
        return imglist[0]
    else:
        regSecond = r',(192.168.[0-9]{1,3}.[0-9]{1,3}),'
        imgreSecond = re.compile(regSecond)
        imglistSecond = re.findall(imgreSecond, addressList)
        return imglistSecond[0]
