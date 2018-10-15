import os
import uuid

from flask import Flask,request, make_response
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, create_engine, INT
from sqlalchemy.orm import sessionmaker
import pymssql


Base = declarative_base()

# 定义数据库映射对象:
class medicalImaging(Base):
    # 表的名字:
    __tablename__ = 'testTable'

    # 表的结构:
    test_id = Column(INT(), primary_key=True)

    test_name= Column(String(400))
    # 上传图片拼接的html
    test_allImage = Column(String(99999))


# DataEntry上传文件服务器
app = Flask(__name__)

@app.route('/up_file', methods=['GET', 'POST'])
def up_file():
    if request.method == "POST":

        # 初始化数据库连接:
        engine = create_engine('mssql+pymssql://sa:123@192.168.11.160:1434/testdatabase1?charset=utf8')
        # 创建DBSession类型:
        DBSession = sessionmaker(bind=engine)
        # 创建Session:
        session = DBSession()

        # 跨域访问的设置
        resp = make_response()
        resp.headers['Access-Control-Allow-Origin'] = '*'

        # 获得传来的影像学ID
        medical_image_id=request.form.get("medical_image_id")
        print('影像学ID为：'+str(medical_image_id))

        # 获得form上传文件
        uploaded_files = request.files.getlist("mulfile")

        # 初始化拼接的html
        all_Image_html_message=''

        # 遍历文件
        for file in uploaded_files:
            # 1、随机生成GUID为文件进行命名
            # 1.2获得图片的格式
            indexType=str(file.filename).rindex('.')
            fileType=file.filename[indexType:len(str(file.filename))]
            newFileName=str(uuid.uuid1())+fileType

            # 2、文件的地址信息平凑成html的img格式  保存到该影像学的上传图片信息(html)格式的字段
            file.save(os.path.join('templates\\files', newFileName))

            all_Image_html_message+=r'<img src="uploadImage/templates/files/'+newFileName+'" width="700" height="auto" max-width="700">'

        data = session.query(medicalImaging).get(medical_image_id)
        # 如果有值才叠加
        if data.test_allImage:
            data.test_allImage = str(data.test_allImage) + str(all_Image_html_message)
        else:
            data.test_allImage = str(all_Image_html_message)

        session.flush()
        # 最后提交事务
        session.commit()
        # 关闭Session:
        session.close()

        return resp

@app.route('/test', methods=['GET'])
def test():
    return 'asdadasd'

if __name__ == "__main__":
    app.run(host='192.168.11.160', port=6001)
