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
    Patient_New_ID = Column(String(100))

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

         # 4038194
        while self.cTime<=self.aTime:
            numFirst = int(self.perNum * self.cTime)
            numSecond = int(self.perNum * self.cTime + self.perNum+1)
            print(str(self.tName)+'处理第：'+str(numFirst)+'条数据到'+str(numSecond)+'条数据正在处理')

            # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
            dataFormat = session.query(DataFormat).slice(numFirst, numSecond).all()

            for singlerData in dataFormat:
                # 方法48  “结果”中的数值和字符串的转换
                # 前提是不为空
                if str(singlerData.Lis_test_result_quantitative) != 'N/A':
                    # 如果为字符串
                    # 就转到另外一个字段之中
                    if theoFilter.method48(singlerData.Lis_test_result_quantitative) == False:
                        # 新的字段放入此字符串
                        singlerData.Lis_test_result_qualitative_2 = singlerData.Lis_test_result_quantitative
                        # 旧的空位放N/A
                        singlerData.Lis_test_result_quantitative = 'N/A'

                # 方法50解决病理诊断编码
                if theoFilter.method50(singlerData.Pathology_diagnosis_code):
                    singlerData.Pathology_diagnosis_code = 'N/A'

                # 方法51
                result51 = theoFilter.method51(singlerData.Discharge_department_name)
                # 赋值
                singlerData.Discharge_department_name = result51

                # 方法52
                result52 = theoFilter.method52(singlerData.Discharge_department_name)
                # 赋值
                singlerData.Discharge_department_name = result52

                # 方法53
                result53 = theoFilter.method53(singlerData.Discharge_department_name)
                # 赋值
                singlerData.Discharge_department_name = result53

                # 方法54
                result54 = theoFilter.method54(singlerData.Discharge_department_name)
                # 赋值
                singlerData.Discharge_department_name = result54

                # 方法55
                result55 = theoFilter.method55(singlerData.Discharge_department_name)
                # 赋值
                singlerData.Discharge_department_name = result55

                # 方法56
                result56 = theoFilter.method56(singlerData.Discharge_department_name)
                # 赋值
                singlerData.Discharge_department_name = result56

                # 方法57
                result57 = theoFilter.method57(singlerData.Discharge_department_name)
                # 赋值
                singlerData.Discharge_department_name = result57

                # 方法58
                result58 = theoFilter.method58(singlerData.Discharge_department_name)
                # 赋值
                singlerData.Discharge_department_name = result58

                # 方法59
                result59 = theoFilter.method59(singlerData.Discharge_department_name)
                # 赋值
                singlerData.Discharge_department_name = result59

                # 方法60
                result60 = theoFilter.method60(singlerData.Discharge_department_name)
                # 赋值
                singlerData.Discharge_department_name = result60

                # 方法61
                result61 = theoFilter.method61(singlerData.Discharge_department_name)
                # 赋值
                singlerData.Discharge_department_name = result61

                # 方法62
                result62 = theoFilter.method62(singlerData.Discharge_department_name)
                # 赋值
                singlerData.Discharge_department_name = result62

                # 方法63
                result63 = theoFilter.method63(singlerData.Discharge_department_name)
                # 赋值
                singlerData.Discharge_department_name = result63

                # 方法64
                result64 = theoFilter.method64(singlerData.Discharge_department_name)
                # 赋值
                singlerData.Discharge_department_name = result64

                # 方法65
                result65 = theoFilter.method65(singlerData.Discharge_department_name)
                # 赋值
                singlerData.Discharge_department_name = result65

                # 方法66
                result66 = theoFilter.method66(singlerData.Discharge_department_name)
                # 赋值
                singlerData.Discharge_department_name = result66

                # 一定要flush()，否则会有语句丢失
                session.flush()

            self.cTime+=1

        # 最后提交
        session.commit()
        # 关闭Session:
        session.close()


@clock
def testTime():
    print('主线程开始')
    # 总记录数
    tAllNum=10000
    # 开的线程个数
    tThreadNum=1
    # 每次循环在数据库检查的条数
    tRecordNum=1000
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


