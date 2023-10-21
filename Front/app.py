
from typing import List

from shiny import App, Inputs, Outputs, Session, reactive, ui, render
from shiny.types import NavSetArg
from htmltools import TagList, div
import shiny.experimental
import re
from data_process import df_r as df

style="border: 0px solid #999;"


hell = ui.a('Hej', href = "https://shiny.posit.co/py/api/ui.panel_main.html")


Title = div("Znalezione podobne orzeczenia", id = 'tytul', class_='tytul')

LISTA_GIGA_DUZA = []

for i in range(10):

    sygn1 = df['courtCases'][i]
    sedzia1 = ", ".join(df['judges'][i])
    data1 = df['judgmentDate'][i]
    tekst_orze = df['textContent'][i]
    sygn = div(sygn1, id='elem', class_='sygnatura')
    sedzia = div("Skład sędziowski: " + sedzia1, id='elem', class_='sedzia')
    data = div("Data: " + data1, id='elem', class_='data')
    orzeczenie_tekst = div(tekst_orze, id='elem', class_='orzeczenie_tekst')

    idk = (sygn, sedzia, data, orzeczenie_tekst)
    orze_1 = div(idk, id="single_orz", class_='orzeczenie')
    LISTA_GIGA_DUZA.append(orze_1)

duzy_div_orz = div(LISTA_GIGA_DUZA, id='duzy_div_orz', class_='lista')

app_ui = ui.page_navbar(
    ui.nav('Znajdź podobne',
           ui.layout_sidebar(
                ui.panel_sidebar(
                    ui.input_selectize("txt_kw", "Podaj słowa kluczowe:",
                                        ["Dziedziczenie i dziedziczy", "Incydenty drogowe", "Kary pieniężne", "Kradzieże", "Konflikty korporacyjne", "Konflikty z polisami", "Kwestie związane z opieką nad dziećmi", "Naprawienie krzywdy", "Naruszenia kontraktów", "Naruszenia przepisów ochrony środowiska", "Naruszenia przepisów podatkowych", "Naruszenia umów wynajmu", "Opłaty za wykroczenia", "Ochrona zdrowotna", "Podział majątku po rozwodzie", "Podział majątku po zmarłych", "Podziały spadku", "Polisy ubezpieczeniowe", "Przywracanie równowagi", "Przywracanie sprawiedliwości", "Problemy z nieruchomościami", "Rekompensata", "Rozlew substancji niebezpiecznych", "Rozliczenia handlowe", "Rozliczenia ubezpieczeniowe", "Rozwody i separacje", "Rozwód i podział majątku", "Szkody w budownictwie", "Szkody w budownictwie", "Spory biznesowe", "Spory dzierżawcze", "Spory korporacyjne", "Spory o nieruchomości", "Spory o prawa rodzicielskie", "Spory o spadek", "Spory dotyczące gruntów", "Spustoszenia", "Straty materialne", "Urazy ciała", "Unieważnienie testamentu", "Uszkodzenia ekosystemów", "Uszkodzenia mienia", "Uszkodzenia zdrowia", "Uszkodzenia środowiska naturalnego", "Ustalanie wysokości alimentów", "Wyrównanie szkody", "Wykroczenia finansowe", "Zanieczyszczenia przyrodnicze", "Zniszczenia rzeczy"],
                                        multiple=True),
                    ui.input_text_area("txtfull", "Podaj stan faktyczny:", ),
                ),
                ui.panel_main(
                        Title,
                        duzy_div_orz,
                        ui.include_css("www/my-styles.css"),
                        ui.output_text_verbatim("txt_kw"),
                        ui.output_text_verbatim("txtfull")
                        )
           )
        ),
    title='Przeanalizuj mnie'
)


def server(input: Inputs, output: Outputs, session: Session):
    
    @output
    @render.text
    def txt_kw():
        return input.txt_kw()

    @output
    @render.text
    def txtfull():
        return input.txtfull()

app = App(app_ui, server)
app.run(port=8080)