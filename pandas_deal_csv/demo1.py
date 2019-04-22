import pandas as pd


path = 'formativetableprimarykey_fourthtry.csv'

f = open(path)

data = pd.read_csv(path, sep=',',engine = 'python',iterator=True)
loop = True
chunkSize = 10000
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

n=0
for single in chunks:
    print(single)
    n+=1
    print('this is '+str(n))
