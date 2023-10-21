import pandas as pd


#tags without header


tags = pd.read_csv("../Data/tagi.csv", sep=";")
tags = tags["tag"].tolist()
print(tags)