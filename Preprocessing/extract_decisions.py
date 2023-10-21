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

# def extract_decision(document):
#     pattern = r"z dnia (.*?)UZASADNIENIE"
#     matches = re.findall(pattern, document, re.DOTALL)
#     print(matches)
#     extracted_texts = [re.sub(r'^[^\n]*\n', '', match.strip()) for match in matches]
#     extracted_texts = [re.sub(r'\n[^\n]*$', '', match) for match in extracted_texts]
#     extracted_texts = [re.sub(r'\b[IVXLCDM]+\b', '', match) for match in extracted_texts]  # Remove Roman numerals
#     extracted_texts = [re.sub(r'[{}]+'.format(string.punctuation), '', match) for match in extracted_texts]
#     extracted_texts = [re.sub(r'\s+', ' ', match).strip() for match in extracted_texts]
#     extracted_texts = [re.sub(r'^.*?UZPZO\d+\s*', '', match) for match in extracted_texts]  # Remove prefix and space
#     extracted_texts = [re.sub(r'^1', '', match.strip()) for match in extracted_texts]  # Remove "1" at the start
#     extracted_texts = [match.lstrip() for match in extracted_texts]  # Remove leading space
#     extracted_texts = [match.replace("u c h y l a", "uchyla").replace("o d d a l a", "oddala") for match in extracted_texts]  # Replace "u c h y l a" and "o d d a l a"
#     extracted_texts = [re.sub(r'Sygn akt [A-Za-z0-9 ]+', '', match).strip() for match in extracted_texts]
#     return extracted_texts

def extract_decision(document):
    document = document.replace("dnia", "z dnia")
    pattern = r"z dnia (.*?)(UZASADNIENIE|$)"
    matches = re.findall(pattern, document, re.DOTALL)

    # Get the first match
    first_match = None
    for match in matches:
        first_match = match[0].strip()
        break

    # Extract from the first match to the end of the document
    extracted_texts = [first_match] if first_match else ['']

    # Extract from the start to "UZASADNIENIE"
    start_to_uzasadnienie = re.search(r'(.*?)UZASADNIENIE', document, re.DOTALL)
    if start_to_uzasadnienie:
        start_to_uzasadnienie_text = start_to_uzasadnienie.group(1).strip()
        if start_to_uzasadnienie_text:
            extracted_texts.append(start_to_uzasadnienie_text)

    extracted_texts = [re.sub(r'\b[IVXLCDM]+\b', '', match) for match in extracted_texts]  # Remove Roman numerals
    extracted_texts = [re.sub(r'[{}]+'.format(string.punctuation), '', match) for match in extracted_texts]
    extracted_texts = [re.sub(r'\s+', ' ', match).strip() for match in extracted_texts]
    extracted_texts = [re.sub(r'^1', '', match.strip()) for match in extracted_texts]  # Remove "1" at the start
    extracted_texts = [match.lstrip() for match in extracted_texts]  # Remove leading space
    extracted_texts = [match.replace("u c h y l a", "uchyla").replace("o d d a l a", "oddala") for match in
                       extracted_texts]  # Replace "u c h y l a" and "o d d a l a"

    # Remove the suffix (e.g., "Sygn akt ACa 136704")
    extracted_texts = [re.sub(r'Sygn akt [A-Za-z0-9 ]+', '', match).strip() for match in extracted_texts]

    return extracted_texts


df['extractedDecision'] = df['textContent'].apply(extract_decision)

print(df["extractedDecision"].iloc[9])

df.to_csv("../Data/output_with_decisions.csv", sep=";", index=False)