import pandas as pd

file_path = '../Data/output4.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path, sep=";")
df = df.drop(df.columns[0], axis=1)

df = df[df["courtType"] == "COMMON"]  # only common courts

df = df[df["judgmentType"] == "SENTENCE"]  # only sentences

pattern = r"z dnia (\d{1,2}\s\w+\s\d{4} r., sygn. akt \w{2} \w{2} \d{3}/\d{2})"