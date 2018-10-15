# urllib模块提供了读取Web页面数据的接口
import time
import urllib.request
# re模块主要包含了正则表达式
import re

# 定义一个getHtml()函数
from decorator.timekill import clock


def get_Html(targeturl):

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
    req = urllib.request.Request(url=targeturl, headers=headers)
    html = urllib.request.urlopen(req).read().decode("utf-8")

    # with open("file", 'w', encoding='utf-8') as new:  # 将html保存为file文件
    #     new.write(html)
    return html

@clock
def get_Image(html,x):
    regJpg = r'source-data-lazy-img="(//img.*jpg)"'  # 正则表达式，得到图片地址

    imgreJpg = re.compile(regJpg)  # re.compile() 可以把正则表达式编译成一个正则表达式对象.

    imglist = re.findall(imgreJpg, html)  # re.findall() 方法读取html 中包含 imgre（正则表达式）的数据
    for imgurl in imglist:

        # print('这是第 '+str(x)+' 条数据：'+imgurl)
        imgurl='https:'+imgurl
        print('这是第 ' + str(x) + ' 条数据：' + imgurl)
        urllib.request.urlretrieve(imgurl, 'C:\\Users\\Administrator\\Desktop\\imaStorage\\%s.jpg' % x)
        # 核心是urllib.urlretrieve()方法,直接将远程数据下载到本地，图片通过x依次递增命名
        x += 1
    return x
x = 1
for i in range(10):
    html = get_Html("https://search.jd.com/search?keyword=%E7%94%B5%E8%84%91&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E7%94%B5%E8%84%91&ev=exbrand_%E6%88%B4%E5%B0%94%EF%BC%88DELL%EF%BC%89%5E&page="+str(1)+"&s=1&click=0")
    x=get_Image(html,x)
