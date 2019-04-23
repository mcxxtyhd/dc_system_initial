from sqlalchemy import create_engine


import pandas as pd

chunks = pd.read_csv('formativetableprimarykey_fourthtry.csv',iterator = True)
chunk = chunks.get_chunk(5)


engine = create_engine('mssql+pymssql://sa:123@localhost:1434/testPythonDatabase?charset=utf8')


chunk.to_sql(name='cleaningdata', con=engine, if_exists='append', index=False)