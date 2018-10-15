#根据url生成二维码
import qrcode
def qrcodeWithUrl(url):
    img=qrcode.make(url)
    #保存图片
    savePath=r'1.png'
    img.save(savePath)

#根据输入内容生成二维码
content=input('请输入内容：')
qrcodeWithUrl(content)
print('二维码已生成！')