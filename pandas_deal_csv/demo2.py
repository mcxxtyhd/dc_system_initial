import pandas as pd
from sqlalchemy import create_engine

chunks = pd.read_csv('formativetableprimarykey_fourthtry.csv',iterator = True)

engine = create_engine('mssql+pymssql://sa:123@localhost:1434/testPythonDatabase?charset=utf8')

target_chunk=chunks.get_chunk(10000)

target_chunk.to_sql(name='cleaningdata', con=engine, if_exists='append', index=False)
#
print(target_chunk)

# for single in chunks:
#     print (single)