import pymysql
import xlrd
from xlutils.copy import copy
import openpyxl

rb = xlrd.open_workbook("C:\\Users\\Administrator\\Desktop\\demo2.xls")    #打开weng.xls文件
wb = copy(rb)                          #利用xlutils.copy下的copy函数复制
ws = wb.get_sheet(0)

# 打开数据库连接
db = pymysql.connect("localhost", "root", "root", "formativedata")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute()  方法执行 SQL 查询
cursor.execute("SELECT * FROM `就诊ID`")
results = cursor.fetchall()

# 给一个默认的游标
n=1
for data in results:
    ws.write(n, 43, data[0])
    n+=1


# 关闭数据库连接
db.close()


#最后，将以上操作保存到指定的Excel文件中
wb.save("C:\\Users\\Administrator\\Desktop\\demo2.xls")