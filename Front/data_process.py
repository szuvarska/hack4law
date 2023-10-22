import pandas as pd
import re
pd.options.mode.chained_assignment = None
#from Similarity import find_similar as fs

df = pd.read_csv("Front/clean_output1.csv",sep = ';')
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

df = get_caseNumber(get_judges(df))
