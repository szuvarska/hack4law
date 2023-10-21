import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv('Data/clean_output1.csv', sep = ";")
print(df['textContent'].iloc[0])

# Inicjalizacja obiektu TF-IDF Vectorizer
tfidf_vectorizer = TfidfVectorizer()

# Fit i transformacja tekstu do reprezentacji TF-IDF
tfidf_matrix = tfidf_vectorizer.fit_transform(df['textContent'])

# Konwersja rzadkiej macierzy TF-IDF do ramki danych
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out())

# Wyświetlenie utworzonej ramki danych
print(tfidf_df.head(2))

# Wybierz pierwszy wiersz jako punkt odniesienia
query_vector = tfidf_df.iloc[0].values.reshape(1, -1)

# Wybierz resztę wierszy jako punkty docelowe
target_vectors = tfidf_df.iloc[1:]

# Oblicz podobieństwo kosinusowe
cosine_similarities = cosine_similarity(query_vector, target_vectors)

# Konwertuj wynik do ramki danych
similarity_df = pd.DataFrame({'Cosine Similarity': cosine_similarities[0]}, index=df.index[1:])

# Wyświetlenie wyniku
print(similarity_df.sort_values(by = 'Cosine Similarity'))


def addSimilarity(new_data:pd.Series, base_df:pd.DataFrame):
    """
    This functions will have documentation later

    Args:
        base_df (pd.DataFrame): _description_
        new_data (pd.Series): _description_

    Returns:
        _type_: _description_
    """    
    pass
