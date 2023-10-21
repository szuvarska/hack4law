import pandas as pd

def filterdata(df):
    df = df[df["courtType"] == "COMMON"]
    # judgeType = SENTENCE or REASONS
    df = df[df["judgmentType"] == "SENTENCE"]
    return df

data = pd.read_csv("../Data/clean_output1.csv", sep=";")
filtered_data = filterdata(data)


import re
def uzasadnienie(text):
    #print(text)
    start = re.search("UZASADNIENIE", text)
    end = re.search("sąd\s\w+\szważyć", text)
    if start and end:
        return text[start.end():end.start()]
    else:
        return text


filtered_data["textContent"] = filtered_data["textContent"].astype(str)
#new column with uzasadnienie


filtered_data["uzasadnienie"] = filtered_data["textContent"].apply(uzasadnienie)


#print( len(filtered_data["textContent"]))
#print((filtered_data["uzasadnienie"]))


def check():
    for i in range ( len(filtered_data["textContent"])):
            print(filtered_data["textContent"].iloc[i])
            print("#######################################################")

            print( uzasadnienie((str) (filtered_data["textContent"].iloc[i])))
            print("\n \n \n \n")
            print("#######################################################")
            print("#######################################################")
        #print(data["textContent"].iloc[10])

check()