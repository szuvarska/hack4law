import pandas as pd
import re
df = pd.read_csv("clean_output2.csv", sep=';')
pd.options.mode.chained_assignment = None

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