import string
import textwrap

import pandas as pd
import spacy
from bs4 import BeautifulSoup

# Replace 'your_file.csv' with the path to your CSV file
file_path = '../Data/output4.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path, sep=";")
df = df.drop(df.columns[0], axis=1)

df = df[df["courtType"] == "COMMON"]  # only common courts

# Print the pretty printed string
# print(textwrap.fill(df["textContent"].iloc[0], width=60))


# Function to remove HTML tags from a document
def remove_html_tags(html_document):
    soup = BeautifulSoup(html_document, 'html.parser')
    text_without_tags = soup.get_text()
    return text_without_tags


# Apply the function to the 'html_documents' column
df['textContent'] = df['textContent'].apply(remove_html_tags)

# Load the Polish model
nlp = spacy.load("pl_core_news_sm")


# Function to remove punctuation from a document
def remove_punctuation(document):
    translator = str.maketrans('', '', string.punctuation)
    return document.translate(translator)


# Function to lemmatize a single document with POS tagging after removing punctuation
def lemmatize_document_with_pos_and_punctuation(document):
    doc = nlp(remove_punctuation(document))
    lemmatized_tokens = [token.lemma_ if token.pos_ not in {"SPACE"} else token.text for token in doc]
    return ' '.join(lemmatized_tokens)


# Lemmatize all documents in a DataFrame with POS tagging and after removing punctuation
df["textContent"] = df["textContent"].apply(lemmatize_document_with_pos_and_punctuation)

# Function to lemmatize a single document
def remove_stopwords(doc):
    return ' '.join([token.text for token in nlp(doc) if not token.is_stop])


# Apply the function to the 'documents' column
df['textContent'] = df['textContent'].apply(remove_stopwords)

# Print the cleaned documents
print(df["textContent"].iloc[0])

# Save clean data to csv
df.to_csv("../Data/clean_output1.csv", sep=";", index=False)
