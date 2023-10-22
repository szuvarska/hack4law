
from typing import List, Optional

from shiny import App, Inputs, Outputs, Session, reactive, ui, render
from shiny.types import NavSetArg
from htmltools import Tag, TagList, div
import shiny.experimental
import re
import json
import pandas as pd

from pathlib import Path

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.schema import Document


# Potrzebne pakiety to: 'langchain[chromadb], sentence-transformer i chromadb

def return_df_with_similarities(query:str, tags = ['Kary pieniężne', 'Wyrównanie szkody'], data_path = 'Data/output_for_frontend_2.csv' ):

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
        query, k=len(df)
        
    )

    results = [(score, doc.metadata["source"], doc.page_content) for (doc, score) in sim]
    results.sort(key=lambda x: x[0])

    # pprint.pprint(results)
    
    df_results = pd.DataFrame(results, columns = ['similarity', 'id', 'uzasadnienie'])
    df_results['id'] = df_results['id'].astype('str')
    df['id'] = df['id'].astype('str')
    df = df[[col for col in df.columns if col!="uzasadnienie"]]
    merged = df_results.merge(df, on='id', how='inner')

    condition = merged['tags'].apply(lambda row_tags: all(tag in row_tags for tag in tags))
    filtered_merged = merged.loc[condition]
    filtered_merged = filtered_merged.sort_values(by=['similarity'], ascending=True).iloc[:10, :]
    return filtered_merged.reset_index(drop=True)

style="border: 0px solid #999;"


hell = ui.a('Hej', href = "https://shiny.posit.co/py/api/ui.panel_main.html")

Title = div("Znalezione podobne orzeczenia", id = 'tytul', class_='tytul')

# df = None
# df = return_df_with_similarities('Zakład Ubezpieczeń')

app_ui = ui.page_navbar(
    ui.nav('Znajdź podobne',
           ui.layout_sidebar(
                ui.panel_sidebar(
                    ui.input_selectize("txt_kw", "Podaj słowa kluczowe:",
                                        ["Dziedziczenie i dziedziczy", "Incydenty drogowe", "Kary pieniężne", "Kradzieże", "Konflikty korporacyjne", "Konflikty z polisami", "Kwestie związane z opieką nad dziećmi", "Naprawienie krzywdy", "Naruszenia kontraktów", "Naruszenia przepisów ochrony środowiska", "Naruszenia przepisów podatkowych", "Naruszenia umów wynajmu", "Opłaty za wykroczenia", "Ochrona zdrowotna", "Podział majątku po rozwodzie", "Podział majątku po zmarłych", "Podziały spadku", "Polisy ubezpieczeniowe", "Przywracanie równowagi", "Przywracanie sprawiedliwości", "Problemy z nieruchomościami", "Rekompensata", "Rozlew substancji niebezpiecznych", "Rozliczenia handlowe", "Rozliczenia ubezpieczeniowe", "Rozwody i separacje", "Rozwód i podział majątku", "Szkody w budownictwie", "Szkody w budownictwie", "Spory biznesowe", "Spory dzierżawcze", "Spory korporacyjne", "Spory o nieruchomości", "Spory o prawa rodzicielskie", "Spory o spadek", "Spory dotyczące gruntów", "Spustoszenia", "Straty materialne", "Urazy ciała", "Unieważnienie testamentu", "Uszkodzenia ekosystemów", "Uszkodzenia mienia", "Uszkodzenia zdrowia", "Uszkodzenia środowiska naturalnego", "Ustalanie wysokości alimentów", "Wyrównanie szkody", "Wykroczenia finansowe", "Zanieczyszczenia przyrodnicze", "Zniszczenia rzeczy"],
                                        multiple=True),
                    ui.input_text_area("txtfull", "Podaj stan faktyczny:", ),
                    ui.input_action_button('go', 'Szukaj'),
                    ui.output_data_frame('data_f'),
                ),
                ui.panel_main(
                        Title,
                        ui.output_ui("decision"),
                        ui.input_action_button('more', 'Więcej'),

                        # ui.output_ui("dajDivOrze1"),
                        # ui.input_switch('czytajmore1', "Czytaj więcej"),

                        # ui.output_ui("dajDivOrze2"),
                        # ui.input_switch('czytajmore2', "Czytaj więcej"),

                        # ui.output_ui("dajDivOrze3"),
                        # ui.input_switch('czytajmore3', "Czytaj więcej"),

                        # ui.output_ui("dajDivOrze4"),
                        # ui.input_switch('czytajmore4', "Czytaj więcej"),

                        # ui.output_ui("dajDivOrze5"),
                        # ui.input_switch('czytajmore5', "Czytaj więcej"),

                        # ui.output_ui("dajDivOrze6"),
                        # ui.input_switch('czytajmore6', "Czytaj więcej"),

                        # ui.output_ui("dajDivOrze7"),
                        # ui.input_switch('czytajmore7', "Czytaj więcej"),

                        # ui.output_ui("dajDivOrze8"),
                        # ui.input_switch('czytajmore8', "Czytaj więcej"),

                        # ui.output_ui("dajDivOrze9"),
                        # ui.input_switch('czytajmore9', "Czytaj więcej"),
                        

                        ui.include_css("Front/www/my-styles.css"),

          
                        
                        )
           )
        ),
    title='Przeanalizuj mnie'
)

def get_one_casenumber(json_string):
    pattern = r"'caseNumber': '(.*?)'"
    return re.search(pattern, json_string).group(1)



def server(input: Inputs, output: Outputs, session: Session):
    
    global_df = reactive.Value(pd.DataFrame())
    global_number = reactive.Value(0)
    global_list = reactive.Value(tuple())

    @output
    @render.text
    def txt_kw():
        return input.txt_kw()

    @output
    @render.text
    def txtfull():
        return input.txtfull()
    
    def getOneDecision(df, i = 0, limit = 1000, tru = True) -> Optional[Tag]:
        try:
            df['id'][i]
        except:
            return None

        sygn1 = df['courtCases'][i]
        caseNumber = get_one_casenumber(sygn1)
        # sedzia1 = ", ".join(df['judges'][i])
        data1 = df['judgmentDate'][i]
        tekst_orze = df['textContent'][i]
        if tru==False:
            tekst_orze = tekst_orze[:limit] + "..."
        else:
            tekst_orze = tekst_orze


        sygn = div(caseNumber, id='elem', class_='sygnatura')
        # sedzia = div("Skład sędziowski: " + sedzia1, id='elem', class_='sedzia')
        data = div("Data: " + data1, id='elem', class_='data')
        orzeczenie_tekst = div(tekst_orze, id='elem', class_='orzeczenie_tekst')

        idk = (sygn, data, orzeczenie_tekst)
        orze_1 = div(idk, id="single_orz", class_='orzeczenie')

        return div([orze_1], id='duzy_div_orz', class_='lista')
    

    # def dajOrzeczenie(df, i = 1, limit = 1000, tru = True):

    #     try:
    #         df['id'][i]
    #     except:
    #         return None



        
        
       
    #     LISTA_GIGA_DUZA.append(orze_1)

    #     duzy_div_orz = div(LISTA_GIGA_DUZA, id='duzy_div_orz', class_='lista')

    #     return duzy_div_orz
    
    @reactive.Effect
    @reactive.event(input.go)
    def value():
        print('co')
        global_df.set(return_df_with_similarities(input.txtfull()))
        print(global_df.get())
        print(global_df)


    # def get_ith_decison(i:int):
    #      if input.txtfull() != "":
    #         return dajOrzeczenie(global_df.get(), i, 1000, input.czytajmore0())
         
    @reactive.Effect
    @reactive.event(input.more)
    def add_more():
        if global_df.get() is not None:
            global_number.set(global_number.get() + 1)

        if global_df.get() is not None:
            print("YEY")
            local_copy = global_list.get()
            new_div = getOneDecision(global_df.get(), global_number.get(), 1000, False)
            if len(local_copy) == 0:
                global_list.set(tuple([new_div]))
            else:
                global_list.set(tuple([*local_copy, new_div]))

            print(len(global_list.get()))

    @output
    @render.ui
    def decision():
        print("heh")
        return div(global_list.get())

    # @output
    # @render.ui
    # def dajDivOrze0():
    #    get_ith_decison(0)

    # @output
    # @render.ui
    # def dajDivOrze1():
    #    get_ith_decison(1)

    # @output
    # @render.ui
    # def dajDivOrze2():
    #    get_ith_decison(2)

    # @output
    # @render.ui
    # def dajDivOrze3():
    #     return dajOrzeczenie(global_df, 3, 1000, input.czytajmore3())

    # @output
    # @render.ui
    # def dajDivOrze4():
    #     return dajOrzeczenie(global_df, 4, 1000, input.czytajmore4())

    # @output
    # @render.ui
    # def dajDivOrze5():
    #     return dajOrzeczenie(global_df, 5, 1000, input.czytajmore5())

    # @output
    # @render.ui
    # def dajDivOrze6():
    #     return dajOrzeczenie(global_df, 6, 1000, input.czytajmore6())

    # @output
    # @render.ui
    # def dajDivOrze7():
    #     return dajOrzeczenie(global_df, 7, 1000, input.czytajmore7())

    # @output
    # @render.ui
    # def dajDivOrze8():
    #     return dajOrzeczenie(global_df, 8, 1000, input.czytajmore8())

    # @output
    # @render.ui
    # def dajDivOrze9():
    #     return dajOrzeczenie(global_df, 9, 1000, input.czytajmore9())
    
########################################


app = App(app_ui, server)
app.run(port=8080)