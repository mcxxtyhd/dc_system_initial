# 导入:
import threading

from sqlalchemy import Column, String, create_engine, INT
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
from decorator.timekill import clock
from mysql.convertMethod import convertMethod

Base = declarative_base()

# 定义数据库映射对象:
class DataFormat(Base):
    # 表的名字:
    __tablename__ = 'formativetableprimarykey_secondtry'

    # 表的结构:
    formativeID = Column(INT(), primary_key=True)

    # 患者编号
    Patient_ID = Column(String(200))
    # 新患者编号
    Patient_New_ID= Column(String(100))

    # 出院科室
    Discharge_department_name = Column(String(200))

    # 结果(存放数字)
    Lis_test_result_quantitative = Column(String(200))
    # 结果(存放字符串)
    Lis_test_result_qualitative_2 = Column(String(200))


# 创建过滤器
theoFilter=convertMethod()

class threadCleaning(threading.Thread):
    def __init__(self,perNum,cTime,aTime,tName,lock):
        threading.Thread.__init__(self)
        self.perNum = perNum
        self.cTime = cTime
        self.aTime = aTime
        self.tName = tName
        self.lock = lock

    def run(self):
        # 初始化数据库连接:
        engine = create_engine('mysql+pymysql://root:root@localhost:3306/formativedata')
        # 创建DBSession类型:
        DBSession = sessionmaker(bind=engine)
        # 创建Session:
        session = DBSession()

        testDic={}

        # 收集所有的患者编号组成一个字典
        dataFormat = session.query(DataFormat.Patient_ID).group_by(DataFormat.Patient_ID).all()
        n = 0
        for singlerData in dataFormat:
            if singlerData[0] not in testDic:
                n += 1
                testDic[singlerData[0]] = n


        # 开始替换数据
        while self.cTime < self.aTime:
            numFirst = int(self.perNum * self.cTime)
            numSecond = int(self.perNum * self.cTime + self.perNum + 1)
            print(str(self.tName) + '处理第：' + str(numFirst) + '条数据到' + str(numSecond) + '条数据正在处理')

            dataFormatData = session.query(DataFormat).slice(numFirst, numSecond).all()

            pre_string='qilulc'
            n=0
            for Data in dataFormatData:
                # 新的编号为16位
                Data.Patient_New_ID=pre_string+str(testDic.get(Data.Patient_ID)).zfill(16)
                session.flush()

            self.cTime += 1

        print(testDic)

        # 最后提交
        session.commit()
        # 关闭Session:
        session.close()


@clock
def testTime():
    print('主线程开始')
    # 总记录数  4038194
    tAllNum=4039000
    # 开的线程个数
    tThreadNum=1
    # 每次循环在数据库检查的条数
    tRecordNum=10000
    # 每个线程的循环个数
    tNumPerThread=tAllNum/tRecordNum/tThreadNum


    allThread=[]
    for i in range(tThreadNum):
        # 创建锁
        counter_lock = threading.Lock()

        # 第一个参数是每次循环执行多少个
        # 第二个参数是 从多少条数据开始
        # 第三个参数是 在多少条数据结束
        # 给2的原因是怕除数有余
        single=threadCleaning(tRecordNum,i*tNumPerThread,i*tNumPerThread+tNumPerThread+1,'线程'+str(i),counter_lock)
        allThread.append(single)

    for h in allThread:
        h.start()

    for x in allThread:
        x.join()

    print('主线程结束')

testTime()


