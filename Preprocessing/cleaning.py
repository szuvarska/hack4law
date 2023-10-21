import string
import textwrap
import re
import pandas as pd
import spacy
from bs4 import BeautifulSoup

file_path = 'Data/output5.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path, sep=";")
df = df.drop(df.columns[0], axis=1)

df = df[df["courtType"] == "COMMON"]  # only common courts

df = df[df["judgmentType"] == "SENTENCE"]  # only sentences


# Print the pretty printed string
# print(textwrap.fill(df["textContent"].iloc[0], width=60))


# Function to remove HTML tags from a document
def remove_html_tags(document):
    # Remove HTML tags
    document = BeautifulSoup(document, 'html.parser').get_text()

    # Remove single letters
    # document = ' '.join([word for word in document.split() if len(word) > 1])

    return document


# Apply the function to the 'html_documents' column
df['textContent'] = df['textContent'].apply(remove_html_tags)

# Load the Polish model
nlp = spacy.load("pl_core_news_sm")

# We want to treat "kpc" as a stop word too
nlp.Defaults.stop_words.add("kpc")


# Function to remove punctuation from a document
def remove_punctuation(document):
    translator = str.maketrans('', '', string.punctuation)
    return document.translate(translator)


# Function to lemmatize a single document with POS tagging
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

print(df["textContent"].iloc[0])

def remove_white_spaces(document):
    # Remove newlines and extra white spaces, but keep spaces
    document = re.sub(r'\s+', ' ', document)

    # Remove spaces between numbers and the section sign (§)
    document = re.sub(r'(\d) (\§) (\d)', r'\1\2\3', document)
    return document


df['textContent'] = df['textContent'].apply(remove_white_spaces)

# Print the cleaned documents
print(df["textContent"].iloc[0])

# Save clean data to csv
df.to_csv("../Data/clean_output1.csv", sep=";", index=False)
