import re
import string

import pandas as pd
from bs4 import BeautifulSoup

file_path = '../Data/output4.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path, sep=";")
df = df.drop(df.columns[0], axis=1)

df = df[df["courtType"] == "COMMON"]  # only common courts

df = df[df["judgmentType"] == "SENTENCE"]  # only sentences


def remove_html_tags(document):
    # Remove HTML tags
    document = BeautifulSoup(document, 'html.parser').get_text()

    # Remove single letters
    # document = ' '.join([word for word in document.split() if len(word) > 1])

    return document


# Apply the function to the 'html_documents' column
df['textContent'] = df['textContent'].apply(remove_html_tags)


# print(df["textContent"].iloc[1])

# def extract_decision(document):
#     pattern = r"dnia (.*?)UZASADNIENIE"
#     matches = re.findall(pattern, document, re.DOTALL)
#     extracted_texts = [re.sub(r'^[^\n]*\n', '', match.strip()) for match in matches]
#     extracted_texts = [re.sub(r'\n[^\n]*$', '', match) for match in extracted_texts]
#     extracted_texts = [re.sub(r'\b[IVXLCDM]+\b', '', match) for match in extracted_texts]  # Remove Roman numerals
#     extracted_texts = [re.sub(r'[{}]+'.format(string.punctuation), '', match) for match in extracted_texts]
#     extracted_texts = [re.sub(r'\s+', ' ', match).strip() for match in extracted_texts]
#     return extracted_texts

def extract_decision1(document):
    pattern = r"z dnia (.*?)UZASADNIENIE"
    matches = re.findall(pattern, document, re.DOTALL)
    extracted_texts = [re.sub(r'^[^\n]*\n', '', match.strip()) for match in matches]
    extracted_texts = [re.sub(r'\n[^\n]*$', '', match) for match in extracted_texts]
    extracted_texts = [re.sub(r'\b[IVXLCDM]+\b', '', match) for match in extracted_texts]  # Remove Roman numerals
    extracted_texts = [re.sub(r'[{}]+'.format(string.punctuation), '', match) for match in extracted_texts]
    extracted_texts = [re.sub(r'\s+', ' ', match).strip() for match in extracted_texts]
    extracted_texts = [re.sub(r'^.*?UZPZO\d+\s*', '', match) for match in extracted_texts]  # Remove prefix and space
    extracted_texts = [re.sub(r'^1', '', match.strip()) for match in extracted_texts]  # Remove "1" at the start
    extracted_texts = [match.lstrip() for match in extracted_texts]  # Remove leading space
    extracted_texts = [match.replace("u c h y l a", "uchyla").replace("o d d a l a", "oddala") for match in
                       extracted_texts]  # Replace "u c h y l a" and "o d d a l a"
    extracted_texts = [re.sub(r'Sygn akt [A-Za-z0-9 ]+', '', match).strip() for match in extracted_texts]
    return extracted_texts


def extract_decision2(document):
    pattern = r"z dnia (.*?)UZASADNIENIE"
    matches = re.findall(pattern, document, re.DOTALL)
    extracted_texts = []

    for match in matches:
        # Find the last occurrence of "z dnia" in the match
        last_occurrence = match.rfind("z dnia")
        if last_occurrence != -1:
            extracted_text = match[last_occurrence + 7:].strip()  # Add 7 to skip "z dnia"
            extracted_texts.append(extracted_text)

    extracted_texts = [re.sub(r'^[^\n]*\n', '', match.strip()) for match in extracted_texts]
    extracted_texts = [re.sub(r'\n[^\n]*$', '', match) for match in extracted_texts]
    extracted_texts = [re.sub(r'\b[IVXLCDM]+\b', '', match) for match in extracted_texts]  # Remove Roman numerals
    extracted_texts = [re.sub(r'[{}]+'.format(string.punctuation), '', match) for match in extracted_texts]
    extracted_texts = [re.sub(r'\s+', ' ', match).strip() for match in extracted_texts]
    extracted_texts = [re.sub(r'^.*?UZPZO\d+\s*', '', match) for match in extracted_texts]  # Remove prefix and space
    extracted_texts = [re.sub(r'^1', '', match.strip()) for match in extracted_texts]  # Remove "1" at the start
    extracted_texts = [match.lstrip() for match in extracted_texts]  # Remove leading space
    extracted_texts = [match.replace("u c h y l a", "uchyla").replace("o d d a l a", "oddala") for match in
                       extracted_texts]  # Replace "u c h y l a" and "o d d a l a"
    extracted_texts = [re.sub(r'Sygn akt [A-Za-z0-9 ]+', '', match).strip() for match in extracted_texts]

    return extracted_texts


def extract_decision(document: str):
    pattern = r"z dnia (.*?)UZASADNIENIE"
    end = document.rfind("UZASADNIENIE")
    start = document[:end].rfind("z dnia ")
    extracted_text = document[start:end]
    # Split the text into lines
    lines = extracted_text.splitlines()

    # Remove the first and last lines
    if len(lines) >= 2:
        lines = lines[1:-1]
    extracted_text = "\n".join(lines)

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
    extracted_text = re.sub(r'\s', ' ', extracted_text)

    # Remove extra spaces and spaces at the start and end
    extracted_text = ' '.join(extracted_text.split())
    extracted_text = extracted_text.rsplit('.', 1)[0]
    extracted_text = extracted_text.rstrip('.')
    return extracted_text


df['extractedDecision'] = df['textContent'].apply(extract_decision)
print(df["extractedDecision"].iloc[7])
print(df["extractedDecision"])

df.to_csv("../Data/output_with_decisions.csv", sep=";", index=False)
