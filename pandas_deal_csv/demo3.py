import pandas as pd

chunks = pd.read_csv('formativetableprimarykey_fourthtry.csv',iterator = True)
chunk = chunks.get_chunk(5)


#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)


print(chunk)

# print(chunk.columns.values)







