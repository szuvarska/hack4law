import pandas as pd
import json
import re
df = pd.read_csv("clean_output1.csv", sep=';')
pd.options.mode.chained_assignment = None
# print(df)

# print(df['judges'])

def get_judges(df):
    pattern = r"'name': '(.*?)',"
    for i in range (df.shape[0]):
        
        df['judges'][i] = re.findall(pattern, df['judges'][i])

    return df

def get_caseNumber(df):
    pattern = r"'caseNumber': '(.*?)'"
    for i in range (df.shape[0]):
        df['courtCases'][i] = re.findall(pattern, df['courtCases'][i])
    return df




df_r = get_judges(df)
df_r = get_caseNumber(df_r)

# imiona = [osoba['name'] for osoba in df['judges']]


