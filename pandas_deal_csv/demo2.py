import pandas as pd

chunks = pd.read_csv('test.csv',chunksize=2,iterator = True)

target_chunk=chunks.get_chunk(5)

print(target_chunk)

# for single in chunks:
#     print (single)