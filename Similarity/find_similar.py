import pprint
import pandas as pd

from pathlib import Path

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.schema import Document


# Potrzebne pakiety to: 'langchain[chromadb], sentence-transformer i chromadb


def return_df_with_similarities(query:str, data_path = 'Data/decisions_with_uzasadnienie.csv' ):

    model_name = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    model_kwargs = {"device": "cpu"}
    embeddings = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs)

    chroma_db_filepath = Path("./chroma_db")

    df = pd.read_csv(data_path, sep = ";")

    if chroma_db_filepath.exists():
        db = Chroma(embedding_function=embeddings, persist_directory=str(chroma_db_filepath))
    else:
        documents = df.apply(lambda row: Document(page_content = row['uzasadnienie']
                                                , metadata = {'source' : row['id']}), axis=1)

        text_splitter = CharacterTextSplitter(chunk_size=3000 , chunk_overlap=300)
        docs = text_splitter.split_documents(documents)
        db = Chroma.from_documents(docs, embeddings, persist_directory=str(chroma_db_filepath))

    sim = db.similarity_search_with_score(
        query, k=5
        
    )

    results = [(score, doc.metadata["source"], doc.page_content) for (doc, score) in sim]
    results.sort(key=lambda x: x[0])

    pprint.pprint(results)
    
    df_results = pd.DataFrame(results, columns = ['similarity', 'id', 'uzasadnienie'])
    df_results['id'] = df_results['id'].astype('str')
    df['id'] = df['id'].astype('str')
    df = df[[col for col in df.columns if col!="uzasadnienie"]]
    merged = df_results.merge(df, on='id', how='inner')

    return merged