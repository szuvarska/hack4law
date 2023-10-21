import re

import pandas as pd

file_path = '../Data/output_with_decisions2.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path, sep=";")
df = df[["id", "extractedDecision"]]

df = df.dropna(subset=['extractedDecision'])
def extract_money(document):
    pattern = r'(kwotę|kwocie) (.*?) [złotych|zł|złote|złoty|złotych]'
    matches = re.findall(pattern, document)
    amounts = [match[1] for match in matches]
    amounts = [amount.replace(" ", "").replace(".", "").replace(",", ".") for amount in amounts]
    amounts = [re.sub(r'\(.*?\)', '', amount) for amount in amounts]
    numeric_amounts = []
    for amount in amounts:
        try:
            numeric_amount = float(amount)
        except ValueError:
            return pd.NA
        numeric_amounts.append(numeric_amount)
    total_amount = sum(numeric_amounts)
    return total_amount

df["sumOfMoney"]=df["extractedDecision"].apply(extract_money)

print(df)

# Save the DataFrame to CSV
df.to_csv('../Data/decisions_only.csv', sep=';', encoding='utf-8-sig')