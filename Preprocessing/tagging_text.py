from transformers import pipeline
import pandas as pd
from getuzasadnienie import get_uzasadnienie

data = pd.read_csv("../Data/with_uzasadnienie.csv", sep=";")
#one tag = one row new line seprated
tags = pd.read_csv("../Data/tagi.csv", sep=";")
tags = tags["tag"].tolist()

classifier = pipeline("zero-shot-classification", model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")
# sequence_to_classify = "Angela Merkel ist eine Politikerin in Deutschland und Vorsitzende der CDU"
# candidate_labels = ["politics", "economy", "entertainment", "environment"]
# for ecery row in data do this and add new column with tags and score save to csv file
# new blank columns
data["tags"] = ""
data["score"] = ""


for i in range(len(data["uzasadnienie"])):
    output = classifier(data["uzasadnienie"].iloc[i], tags, multi_label=True)
    data["tags"].iloc[i] = output["labels"]
    data["score"].iloc[i] = output["scores"]
    #save to csv
    data.to_csv("../Data/with_tags.csv", sep=";", index=False)
    print(data.iloc[i])
    print("#######################################################")


