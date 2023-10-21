
from typing import List

from shiny import App, Inputs, Outputs, Session, reactive, ui, render
from shiny.types import NavSetArg
from htmltools import TagList, div
import shiny.experimental

style="border: 0px solid #999;"


hell = ui.a('Hej', href = "https://shiny.posit.co/py/api/ui.panel_main.html")


x1 = div(hell, id="foo1", class_="bar")
x2 = div("hello2", id="foo2", class_="bar")

sygn = div("sygn_txt", id='elem', class_='sygnatura')
sedzia = div("sedzia_txt", id='elem', class_='sedzia')
data = div("data_txt", id='elem', class_='data')
sad = div("sad_txt", id='elem', class_='sad')
orzeczenie_tekst = div("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", id='elem', class_='orzeczenie_tekst')


idk = (sygn, sedzia, data, sad, orzeczenie_tekst)

orze_1 = div(idk, id="single_orz", class_='orzeczenie')
orze_2= div(idk, id="single_orz", class_='orzeczenie')
orze_3 = div(idk, id="single_orz", class_='orzeczenie')

lista_orz = (orze_1, orze_2, orze_3)
duzy_div_orz = div(lista_orz, id='duzy_div_orz', class_='lista')

app_ui = ui.page_navbar(
    ui.nav('Orzeczenia',
           ui.layout_sidebar(
                ui.panel_sidebar(
                    ui.input_selectize("txt_kw", "Podaj słowa klucze:",
                                        ["Dziedziczenie i dziedziczy", "Incydenty drogowe", "Kary pieniężne", "Kradzieże", "Konflikty korporacyjne", "Konflikty z polisami", "Kwestie związane z opieką nad dziećmi", "Naprawienie krzywdy", "Naruszenia kontraktów", "Naruszenia przepisów ochrony środowiska", "Naruszenia przepisów podatkowych", "Naruszenia umów wynajmu", "Opłaty za wykroczenia", "Ochrona zdrowotna", "Podział majątku po rozwodzie", "Podział majątku po zmarłych", "Podziały spadku", "Polisy ubezpieczeniowe", "Przywracanie równowagi", "Przywracanie sprawiedliwości", "Problemy z nieruchomościami", "Rekompensata", "Rozlew substancji niebezpiecznych", "Rozliczenia handlowe", "Rozliczenia ubezpieczeniowe", "Rozwody i separacje", "Rozwód i podział majątku", "Szkody w budownictwie", "Szkody w budownictwie", "Spory biznesowe", "Spory dzierżawcze", "Spory korporacyjne", "Spory o nieruchomości", "Spory o prawa rodzicielskie", "Spory o spadek", "Spory dotyczące gruntów", "Spustoszenia", "Straty materialne", "Urazy ciała", "Unieważnienie testamentu", "Uszkodzenia ekosystemów", "Uszkodzenia mienia", "Uszkodzenia zdrowia", "Uszkodzenia środowiska naturalnego", "Ustalanie wysokości alimentów", "Wyrównanie szkody", "Wykroczenia finansowe", "Zanieczyszczenia przyrodnicze", "Zniszczenia rzeczy"],
                                        multiple=True),
                    ui.input_text_area("txtfull", "Podaj pełną treść orzeczenia:",placeholder="Orzeczenie"),
                    
                ),
                ui.panel_main(
                       
                        duzy_div_orz,
                        ui.include_css("www\my-styles.css"),
                        ui.output_text_verbatim("txt_kw")
                        )
           )
        ),
    ui.nav('second opt'),
    title='Danonki'
    
)


def server(input: Inputs, output: Outputs, session: Session):
    @output
    @render.text
    def value():
        return input.caption()
    
    @output
    @render.text
    def txt_kw():
        return input.txt_kw()


app = App(app_ui, server)