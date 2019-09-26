import pandas as pd

def foo(row):


a = [1,2,3]
b = [2,3,4]
c = [3,3,2]

df = pd.DataFrame({"a":a,"b":b,"c":c})

df.assign(abc=df.apply(foo,axis=1))

#print(df)