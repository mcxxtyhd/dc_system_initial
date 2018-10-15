# urllib模块提供了读取Web页面数据的接口
import urllib.request
# re模块主要包含了正则表达式
import re

# 定义一个getHtml()函数
def get_Html(targeturl):

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
    req = urllib.request.Request(url=targeturl, headers=headers)
    html = urllib.request.urlopen(req).read().decode('utf-8')

    with open("file", 'w', encoding='utf-8') as new:  # 将html保存为file文件
        new.write(html)
    return html


def get_Image(html):
    reg = r'data-original="(http.*/90)"'  # 正则表达式，得到图片地址
    # 匹配data-original="http://img95.699pic.com/photo/50032/0838.jpg_wh300.jpg!/fh/300//quality/90"
    imgre = re.compile(reg)  # re.compile() 可以把正则表达式编译成一个正则表达式对象.
    imglist = re.findall(imgre, html)  # re.findall() 方法读取html 中包含 imgre（正则表达式）的数据
    x = 0
    for imgurl in imglist:
        print(imgurl)
        urllib.request.urlretrieve(imgurl, 'C:\\Users\\Administrator\\Desktop\\imaStorage\\%s.jpg' % x)
        # 核心是urllib.urlretrieve()方法,直接将远程数据下载到本地，图片通过x依次递增命名
        x += 1


html = get_Html("http://699pic.com/zhuanti/hangpai.html")
get_Image(html)
