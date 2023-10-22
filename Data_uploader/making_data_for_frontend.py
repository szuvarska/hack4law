import pandas as pd

file_path1 = '../Data/with_uzasadnienie2.csv'
df1 = pd.read_csv(file_path1, sep=";")
df1= df1[["id","uzasadnienie", "judges","courtCases","judgmentDate"]]
file_path2 = '../Data/output_with_decisions2.csv'
df2 = pd.read_csv(file_path2, sep=";")
df2 = df2[["id","textContent"]]
df = pd.merge(df1, df2, on='id', how='inner')
df.drop(df.index[-850:], inplace=True)

df.to_csv("../Data/output_for_frontend.csv", sep=";", index=False)
