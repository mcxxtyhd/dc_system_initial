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

 # 初始化数据库连接:
engine = create_engine('mssql+pymssql://sa:123@192.168.11.160:1434/testdatabase1?charset=utf8')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建Session:
session = DBSession()

data = session.query(medicalImaging).get(2)
data.test_name='3333qweq'
session.commit()
session.close()
# for i in data:
#     print(i.test_name)

