import pprint
import pandas as pd

from pathlib import Path

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.schema import Document


# Potrzebne pakiety to: 'langchain[chromadb], sentence-transformer, chromadb, sqlite


def return_df_with_similarities(query:str, data_path = 'Data/output_for_frontend_2.csv' ):

    model_name = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    model_kwargs = {"device": "cpu"}
    embeddings = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs)

    chroma_db_filepath = Path("./chroma_db")

    df = pd.read_csv(data_path, sep = ";")

    # print(df)

    if chroma_db_filepath.exists():
        db = Chroma(embedding_function=embeddings, persist_directory=str(chroma_db_filepath))
    else:
        documents = df.apply(lambda row: Document(page_content = row['uzasadnienie']
                                                , metadata = {'source' : row['id']}), axis=1)

        text_splitter = CharacterTextSplitter(chunk_size=3000 , chunk_overlap=300)
        docs = text_splitter.split_documents(documents)
        db = Chroma.from_documents(docs, embeddings, persist_directory=str(chroma_db_filepath))
        print("Chroma - DONE")

    sim = db.similarity_search_with_score(
        query, k=5
        
    )

    results = [(score, doc.metadata["source"], doc.page_content) for (doc, score) in sim]
    results.sort(key=lambda x: x[0])

    # pprint.pprint(results)
    
    df_results = pd.DataFrame(results, columns = ['similarity', 'id', 'uzasadnienie'])
    df_results['id'] = df_results['id'].astype('str')
    df['id'] = df['id'].astype('str')
    df = df[[col for col in df.columns if col!="uzasadnienie"]]
    merged = df_results.merge(df, on='id', how='inner')

    return merged

# query = "Pozwanie spółdzielnia mieszkaniowa T żąda od pozwanej spółki oo T zapłaty kwoty 3 929 327 złotych oraz ustawowych odsetek w wysokości 1 062 003 złotych, tytułem kosztów zarządu nieruchomością wspólną w kwocie 401 272 złotych, z ustawowymi odsetkami od wniesienia pozwu. Pozwana wnosi o oddalenie powództwa, zarzucając brak podstawy do obciążenia kosztami zarządu strony na podstawie zawartej umowy zarządu. Zaskarżony wyrok częściowy końcowego sądu okręgowego w Katowicach zasądził na rzecz pozwanej na sumę 3 646 238 złotych oraz ustawowych odsetek od 1 czerwca 2003 roku w wysokości 338 943 złote, z ustawowymi odsetkami od wniesienia pozwu w kwocie 6 913 złotych, tytułem zwrotu kosztów procesu. Oddala również pozostałą część roszczenia. Rozstrzygnięcie opiera się na następujących ustaleniach i wnioskach stron: spółka oo K, spółka oo zakład usługowo-handlowy R, spółka jawna T oraz współinwestor i współwłaściciel budynku wielomieszkaniowego przy Alei T. Powódka pełniła również funkcję inwestora zastępczego na mocy umowy z 12 grudnia 1998 roku, wspólnie inwestując na podstawie umowy i protokołu zdawczo-odbiorczego z 8 lutego 2002 roku, przekazała pozwanej pięć lokal mieszkalny wraz z przynależnym garażem. W okresie od stycznia 2002 do maja 2003 roku obciążała pozwaną kosztami utrzymania i eksploatacji przekazanych lokali i garażu jako część nieruchomości wspólnej. Akt notarialny z 17 kwietnia 2003 roku pozwolił współwłaścicielom budynku na zawarcie umowy o częściowym zniesieniu współwłasności i ustanowieniu odrębnej własności dla lokali. Na tej podstawie pozwana nabyła odrębną własność części lokali wraz z przynależnościami. Powódka jest uprawniona do dochodzenia roszczeń w zakresie zarządu na podstawie artykułu 1 ustępu 3 ustawy z 15 grudnia 2000 roku o spółdzielniach mieszkaniowych, jako że w chwili wyodrębnienia własności lokalów i garażu, zarząd związał się z wydatkami, które mogła żądać na mocy artykułów 207 i 205 Kodeksu cywilnego oraz § 7 umowy wspólnego inwestowania, a wyodrębnienie własności lokalów i garażu wraz z odpowiednim udziałem w nieruchomości wspólnej stanowi podstawę prawną do dochodzenia roszczeń w zakresie zarządu na mocy artykułu 4 ustępu 4 ww. ustawy o spółdzielniach mieszkaniowych. Na mocy artykułu 27 ustawy o zarządzie powierniczym spółdzielni, wyłączono stosowanie przepisów ustawy o własności lokali w zakresie roszczeń powódki. Okres od 8 lutego 2002 roku, kiedy przekazano lokale i garaż, do momentu zapłaty przez pozwaną, był terminem płatności, który wynika z każdorazowo wyznaczanych przez pozwaną faktur. Wyrok został zaskarżony przez pozwaną, która zarzuca naruszenie prawa materialnego, błędne wykładnie i niewłaściwe zastosowanie artykułów 1 ustępu 3 i 27 ustawy o spółdzielniach mieszkaniowych, a także brak zastosowania artykułu 201 Kodeksu cywilnego. Pozwana twierdzi, że należy się jej odsetki, a roszczenie zostało zasądzone na podstawie prawa. Sąd oparł swoje rozstrzygnięcie na zarzutach wniesionych przez obie strony i oddalił powództwo, zasądzając na rzecz powódki koszty procesu, ewentualnie uchylił wyrok i przekazał sprawę do ponownego rozpoznania."

# print(return_df_with_similarities(query)['uzasadnienie'].iloc[0])