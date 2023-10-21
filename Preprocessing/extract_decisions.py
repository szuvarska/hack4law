import re
import string

import pandas as pd
from bs4 import BeautifulSoup

file_path = '../Data/output5.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path, sep=";")
df = df.drop(df.columns[0], axis=1)

df = df[df["courtType"] == "COMMON"]  # only common courts

df = df[df["judgmentType"] == "SENTENCE"]  # only sentences

df = df.dropna(subset=['textContent'])

def remove_html_tags(document):
    # Remove HTML tags
    document = BeautifulSoup(document, 'html.parser').get_text()

    # Remove single letters
    # document = ' '.join([word for word in document.split() if len(word) > 1])

    return document


# Apply the function to the 'html_documents' column
df['textContent'] = df['textContent'].apply(remove_html_tags)


def extract_decision(document: str):
    end = document.rfind("UZASADNIENIE")
    start = document[:end].rfind("z dnia ")
    extracted_text = document[start:end]
    if len(extracted_text) != 0:
        # Split the text into lines
        lines = extracted_text.splitlines()

        # Remove the first and last lines
        if len(lines) >= 2:
            lines = lines[1:-1]
        extracted_text = "\n".join(lines)
    else:
        start = document[:end].rfind("I.")
        extracted_text = document[start:end]
        if len(extracted_text) == 0:
            start = document[:end].rfind("1.")
            extracted_text = document[start:end]
            if len(extracted_text) == 0:
                extracted_text = document[:end]
                lines = extracted_text.split('\n')
                lines = [item for item in lines if item != ""]
                extracted_lines = lines[-2:-1]
                extracted_text = '\n'.join(extracted_lines)

    # Replace "u c h y l a" with "uchyla" and "o d d a l a" with "oddala"
    extracted_text = extracted_text.replace("u c h y l a", "uchyla").replace("o d d a l a", "oddala")

    # Remove text matching the specified patterns
    patterns_to_remove = [
        r"Sygn\. akt I ACa-\d+",
        r"Sygn\. akt- I ACa \d+",
        r"Sygn\.akt I ACa \d+",
        r"Sygn\. akt I ACa \d+",
        r"Sygn\. akt I Ca \d+",
        r"sygn\. akt I (ACa-\d+|UZP/ZO/\S+)",
        r"/\d{2} I ACz \d\d+/\d\d+",
        r"\)\d{2} I ACz \d\d+\)\d\d+",
        r"\)\d+",
        r"/(\d+|\d+ \d+|\d\d+)"
    ]

    for pattern in patterns_to_remove:
        extracted_text = re.sub(pattern, "", extracted_text)

    # Replace tabs and other white characters with spaces

    extracted_text = re.sub(r'\n', '', extracted_text)
    extracted_text = re.sub(r'\s', ' ', extracted_text)
    extracted_text = re.sub(r'Sygn.', ' ', extracted_text)

    # Remove extra spaces and spaces at the start and end
    extracted_text = ' '.join(extracted_text.split())
    extracted_text = extracted_text.rsplit('.', 1)[0]
    extracted_text = extracted_text.rstrip('.')

    return extracted_text

# print(extract_decision(df["textContent"].iloc[8]))
df['extractedDecision'] = df['textContent'].apply(extract_decision)
print(df["extractedDecision"].iloc[7])
print(df["extractedDecision"])

df.to_csv("../Data/output_with_decisions2.csv", sep=";", index=False)
