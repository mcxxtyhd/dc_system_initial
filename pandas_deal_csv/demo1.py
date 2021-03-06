import pandas as pd
from sqlalchemy import create_engine

from decorator.timekill import clock

path = 'formativetableprimarykey_fourthtry.csv'

f = open(path)

data = pd.read_csv(path, sep=',',engine = 'python',iterator=True)
loop = True
chunkSize = 2000
chunks = []
index=0
while loop:
    try:
        print(index)
        chunk = data.get_chunk(chunkSize)
        chunks.append(chunk)
        index+=1

    except StopIteration:
        loop = False
        print("Iteration is stopped.")
print('开始合并')


engine = create_engine('mssql+pymssql://sa:123@localhost:1434/testPythonDatabase?charset=utf8')

@clock
def testmethod():
    for single in chunks:

        single.to_sql(name='cleaningdata', con=engine, if_exists='append', index=False)

testmethod()