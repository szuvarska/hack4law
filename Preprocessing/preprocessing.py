import textwrap

import pandas as pd

# Replace 'your_file.csv' with the path to your CSV file
file_path = '../Data/Out_177.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)
df = df.drop(df.columns[0], axis=1)
# print(df.info())

# Print the pretty printed string
print(textwrap.fill(df["textContent"][0], width=60))