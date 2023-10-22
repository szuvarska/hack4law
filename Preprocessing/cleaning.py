import re
import string

import pandas as pd
import spacy
from bs4 import BeautifulSoup


def remove_html_tags(document):
    print("html")
    # Remove HTML tags
    document = BeautifulSoup(document, 'html.parser').get_text()

    # Remove single letters
    # document = ' '.join([word for word in document.split() if len(word) > 1])

    return document


def remove_punctuation(document):
    translator = str.maketrans('', '', string.punctuation)
    return document.translate(translator)


def lemmatize_document_with_pos_and_punctuation(document, nlp):
    doc = nlp(remove_punctuation(document))
    lemmatized_tokens = [token.lemma_ if token.pos_ not in {"SPACE"} else token.text for token in doc]
    return ' '.join(lemmatized_tokens)


def remove_stopwords(doc, nlp):
    return ' '.join([token.text for token in nlp(doc) if not token.is_stop])


def remove_white_spaces(document):
    # Remove newlines and extra white spaces, but keep spaces
    document = re.sub(r'\s+', ' ', document)

    # Remove spaces between numbers and the section sign (§)
    document = re.sub(r'(\d) (\§) (\d)', r'\1\2\3', document)
    return document


def clean_document(document):
    # Load the Polish model
    nlp = spacy.load("pl_core_news_sm")

    # We want to treat "kpc" as a stop word too
    nlp.Defaults.stop_words.add("kpc")
    # Remove HTML tags
    document = remove_html_tags(document)

    # Lemmatize the document
    document = lemmatize_document_with_pos_and_punctuation(document, nlp)

    # Remove stop words
    document = remove_stopwords(document, nlp)

    # Remove white spaces
    document = remove_white_spaces(document)

    return document


def clean_data():
    file_path = '../Data/output4.csv'

    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path, sep=";")
    df = df.drop(df.columns[0], axis=1)

    df = df[df["courtType"] == "COMMON"]  # only common courts

    df = df[df["judgmentType"] == "SENTENCE"]  # only sentences

    # Print the pretty printed string
    # print(textwrap.fill(df["textContent"].iloc[0], width=60))

    df = df.dropna(subset=['textContent'])

    df["textContent"] = df["textContent"].apply(clean_document)

    # Save clean data to csv
    df.to_csv("../Data/clean_output.csv", sep=";", index=False)

if __name__ == '__main__':
    clean_data()
