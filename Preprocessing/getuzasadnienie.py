import pandas as pd
import re

data = pd.read_csv("../Data/clean_output1.csv", sep=";")
def filterdata(df):
    df = df[df["courtType"] == "COMMON"]
    # judgeType = SENTENCE or REASONS
    df = df[df["judgmentType"] == "SENTENCE"]
    return df


def uzasadnienie(text):
    #print(text)
    start = re.search("UZASADNIENIE", text)
    end = re.search("sąd\s\w+\szważyć", text)
    if start and end:
        return text[start.end():end.start()]
    else:
        return text


def get_uzasadnienie(df):
    df = filterdata(df)
    df["textContent"] = df["textContent"].astype(str)
    df["uzasadnienie"] = df["textContent"].apply(uzasadnienie)
    return df

def check():
    for i in range ( len(filtered_data["textContent"])):
            print(filtered_data["textContent"].iloc[i])
            print("#######################################################")

            print( uzasadnienie((str) (filtered_data["textContent"].iloc[i])))
            print("\n \n \n \n")
            print("#######################################################")
            print("#######################################################")
        #print(data["textContent"].iloc[10])

#saving to csv
with_uzasadnienie = get_uzasadnienie(data)
with_uzasadnienie.to_csv("../Data/with_uzasadnienie.csv", sep=";", index=False)

#check()