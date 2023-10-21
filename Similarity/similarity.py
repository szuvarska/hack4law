import pandas as pd

df = pd.read_csv('Data/output4.csv', sep = ";")
df = df.loc[df["courtType"]=='COMMON',]
print(df['textContent'])


def addSimilarity(new_data:pd.Series, base_df:pd.DataFrame):
    """
    This functions will have documentation later

    Args:
        base_df (pd.DataFrame): _description_
        new_data (pd.Series): _description_

    Returns:
        _type_: _description_
    """    
    pass
