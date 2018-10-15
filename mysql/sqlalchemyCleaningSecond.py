# 导入:
import threading

from sqlalchemy import Column, String, create_engine,INT
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
from decorator.timekill import clock
from mysql.convertMethod import convertMethod

# 因为多个线程操纵一个表的更新 会有风险 所以放弃这种做法


Base = declarative_base()

# 定义数据库映射对象:
class DataFormat(Base):
    # 表的名字:
    __tablename__ = 'formativetableprimarykey_test_copy2'

    # 表的结构:
    formativeID = Column(INT(), primary_key=True)

    # 出院科室
    Discharge_department_name = Column(String(200))

    # 结果(存放数字)
    Lis_test_result_quantitative = Column(String(200))
    # 结果(存放字符串)
    Lis_test_result_qualitative_2 = Column(String(200))


# 创建过滤器
theoFilter=convertMethod()

class threadCleaning(threading.Thread):
    def __init__(self,sess,perNum,cTime,aTime,tName,lock):
        threading.Thread.__init__(self)
        self.sess = sess
        self.perNum = perNum
        self.cTime = cTime
        self.aTime = aTime
        self.tName = tName
        self.lock = lock

    def run(self):
         # 4038194
        while self.cTime<self.aTime:
            numFirst = int(self.perNum * self.cTime)
            numSecond = int(self.perNum * self.cTime + self.perNum)
            print(str(self.tName)+'处理第：'+str(numFirst)+'条数据到'+str(numSecond)+'条数据正在处理')

            # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
            dataFormat = self.sess.query(DataFormat).slice(numFirst, numSecond).all()

            for singlerData in dataFormat:
                # 方法51
                result51 = theoFilter.method51(singlerData.Discharge_department_name)
                # 赋值
                singlerData.Discharge_department_name = result51
                # 一定要flush()，否则会有语句丢失
                self.sess.flush()

            self.cTime+=1


@clock
def testTime():
    print('主线程开始')
    # 总记录数
    tAllNum=500000
    # 开的线程个数
    tThreadNum=4
    # 每次循环在数据库检查的条数
    tRecordNum=10000
    # 每个线程的循环个数
    tNumPerThread=tAllNum/tThreadNum
    tNumPerThread =tNumPerThread/tRecordNum
    # 初始化所有的线程，以便于之后的start 以及 join
    allThread=[]
    sessions=[]

    for i in range(tThreadNum):
        # 初始化数据库连接:
        engine = create_engine('mysql+pymysql://root:root@localhost:3306/formativedata')
        # 创建DBSession类型:
        DBSession = sessionmaker(bind=engine)
        # 创建Session:
        session = DBSession()
        sessions.append(session)

        # 创建锁
        counter_lock = threading.Lock()

        # 第一个参数是每次循环执行多少个
        # 第二个参数是 从多少条数据开始
        # 第三个参数是 在多少条数据结束
        # 给2的原因是怕除数有余
        single=threadCleaning(session,tRecordNum,i*tNumPerThread,i*tNumPerThread+tNumPerThread,'线程'+str(i),counter_lock)
        allThread.append(single)

    for h in allThread:
        h.start()

    for x in allThread:
        x.join()

    # 最后才提交以及结束
    for y in sessions:
        # 最后提交
        y.commit()
        # 关闭Session:
        y.close()

    print('主线程结束')

testTime()


