import pandas as pd

df = pd.read_csv('Data/output3.csv', sep = ";")
print(df.loc[df["courtType"]=='COMMON',])