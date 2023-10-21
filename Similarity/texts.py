# coding=UTF-8

import pprint
import pandas as pd

from pathlib import Path

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.schema import Document

model_name = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
model_kwargs = {"device": "cpu"}
embeddings = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs)

chroma_db_filepath = Path("./chroma_db")
if chroma_db_filepath.exists():
    db = Chroma(embedding_function=embeddings, persist_directory=str(chroma_db_filepath))
else:
    df = pd.read_csv('Data/output_with_decisions.csv', sep = ";")

    documents = df.apply(lambda row: Document(page_content = row['textContent']
                                            , metadata = {'source' : row['id']}), axis=1)

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=300)
    docs = text_splitter.split_documents(documents)
    db = Chroma.from_documents(docs, embeddings, persist_directory=str(chroma_db_filepath))

query = """Powódka K. K. (1) pozwem z dnia 16 czerwca 1994r. wniosła o zobowiązanie pozwanego do usunięcia względnie przestawienia linii wysokiego napięcia 400 KV B. - S. w okolicy działki zabudowanej położonej w J. , ul . (...), stanowiącej własność powódki, ewentualnie o zobowiązanie pozwanego do złożenia oświadczenia woli w przedmiocie nabycia od powódki tejże działki za wynagrodzeniem odpowiadającym wartości tej działki oraz znajdujących się na niej budynków.
W uzasadnieniu powódka podała, iż jest właścicielką działki położonej w J., ul . (...). W 1986r. w odległości około 7 metrów od jej domu wybudowano linię wysokiego napięcia 400 KV której odległość - zgodnie z obowiązującymi przepisami wynosić powinna 33 metry. Mimo zainstalowania specjalnych ekranów - nie są one w pełni skuteczne, wobec czego na działce powódki występuje pole elektryczne o natężeniu szkodliwym dla życia i zdrowia.
Na rozprawie w dniu 26 marca 1997r. powódka sprecyzowała żądanie pozwu domagając się przesunięcia linii wysokiego napięcia lub wykupu przez pozwanych zabudowanej nieruchomości.
W odpowiedzi na pozew pozwany  (...) S.A. w B. wniósł o oddalenie powództwa wobec braku legitymacji biernej, bowiem przedmiotową linię pozwany przekazał w dniu 6 lipca 1993r.  (...) S.A. w K..
Wezwana do udziału w sprawie pozwana -  (...) S.A. (...) w K. wniosło oddalenie powództwa i zasądzenie kosztów.
Pozwana uznała swoją legitymację bierną do występowania w sprawie ale zarzuciła, że usytuowanie linii wysokiego napięcia nie przeszkadza w swobodnym korzystaniu z własności powoda.
Wyrokiem z dnia 9 kwietnia 1997r. Sąd Okręgowy w Katowicach oddalił powództwo. W uzasadnieniu wyroku Sąd wskazał, że oparł się na opinii biegłego dr. inż. M. G., z której jednoznacznie wynika, że wytwarzane przez linię wysokiego napięcia pole elektromagnetyczne w żaden sposób nie uniemożliwia bezpiecznego korzystania z domu powódki. Uznając, że występujące wytwarzanie przez linię emisje nie naruszają możliwości bezpiecznego zamieszkiwania przez powódkę w swym domu - może ona korzystać z nieruchomości zgodnie z jej społeczno-gospodarczym przeznaczeniem. Zdaniem Sądu społeczno - gospodarczym przeznaczeniem linii wysokiego napięcia jest zaspokojenie potrzeb ludności w zakresie energii elektrycznej, przy czym występujące przy przesyłaniu energii niedogodności - jeżeli nie zagrażają życiu i zdrowiu ludzi; nie są nadmierne muszą - być przez nich znoszone.
Apelację od powyższego wyroku wniosła powódka.
Rozpoznając apelację Sąd Apelacyjny w Katowicach wyrokiem z dnia 23 grudnia 1997r. uchylił zaskarżony wyrok i przekazał sprawę do ponownego rozpoznania sądowi pierwszej instancji.
Sąd Apelacyjny podzielił zawarty w apelacji powódki o ile dotyczy ewentualnego naruszenia przez pozwanego prawa własności powódki przez usytuowanie w określonym miejscu linii wysokiego napięcia.
Zwrócił Sąd Apelacyjny uwagę na prawa właściciela w zakresie dysponowania swoją własnością i brak dowodów by pozwany miał jakiekolwiek prawo do nieruchomości powódki, podczas gdy w procesie negatoryjnym na pozwanym spoczywa ciężar udowodnienia, iż naruszenie własności nie było bezprawne. Zdaniem Sądu Apelacyjnego koniecznym są także ustalenia pozwalające na zastosowanie właściwych przepisów prawa materialnego w kontekście przepisów art. 140 k.c. i art. 222 § 2 k.c."""

sim = db.similarity_search_with_score(
    query, k=1
)

# embedding_vector = embeddings.embed_query(query)
# docs_and_scores = db.similarity_search_by_vector(embedding_vector)

results = [(score, doc.metadata["source"], doc.page_content) for (doc, score) in sim]
results.sort(key=lambda x: x[0])

pprint.pprint(results)