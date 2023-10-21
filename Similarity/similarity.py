import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


df = pd.read_csv('Data/clean_output1.csv', sep = ";")
df_id = df['id']
df_text = df['textContent']

# Inicjalizacja obiektu TF-IDF Vectorizer
tfidf_vectorizer = TfidfVectorizer()

# Fit i transformacja tekstu do reprezentacji TF-IDF
tfidf_matrix = tfidf_vectorizer.fit_transform(df_text)

# Konwersja rzadkiej macierzy TF-IDF do ramki danych
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out())

# Wybierz pierwszy wiersz jako punkt odniesienia
new_data = tfidf_df.iloc[0].values.reshape(1, -1)


# Wybierz resztę wierszy jako punkty docelowe
target_vectors = tfidf_df.iloc[1:]

# Dodawanie nowych danych (od sędziego)
# new_data = tfidf_vectorizer.transform(new_df)


def calculateSimilarity(new_data:np.ndarray, base_df:pd.DataFrame):
    """
    This functions will have documentation later

    Args:
        base_df (pd.DataFrame): _description_
        new_data (pd.Series): _description_

    Returns:
        _type_: _description_
    """

    # Oblicz podobieństwo kosinusowe
    cosine_similarities = cosine_similarity(new_data, base_df)

    # Konwertuj wynik do ramki danych
    similarity_df = pd.DataFrame({'Cosine Similarity': cosine_similarities[0]}, index=df_id.iloc[1:])
    return similarity_df


# Wyświetlenie wyniku
print(calculateSimilarity(new_data,target_vectors).sort_values(by = 'Cosine Similarity'))
