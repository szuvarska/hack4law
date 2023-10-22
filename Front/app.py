
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
                        ui.output_ui("dajDivOrze0"),
                        ui.input_switch('czytajmore0', "Czytaj więcej"),

                        ui.output_ui("dajDivOrze1"),
                        ui.input_switch('czytajmore1', "Czytaj więcej"),

                        ui.output_ui("dajDivOrze2"),
                        ui.input_switch('czytajmore2', "Czytaj więcej"),

                        ui.output_ui("dajDivOrze3"),
                        ui.input_switch('czytajmore3', "Czytaj więcej"),

                        ui.output_ui("dajDivOrze4"),
                        ui.input_switch('czytajmore4', "Czytaj więcej"),

                        ui.output_ui("dajDivOrze5"),
                        ui.input_switch('czytajmore5', "Czytaj więcej"),

                        ui.output_ui("dajDivOrze6"),
                        ui.input_switch('czytajmore6', "Czytaj więcej"),

                        ui.output_ui("dajDivOrze7"),
                        ui.input_switch('czytajmore7', "Czytaj więcej"),

                        ui.output_ui("dajDivOrze8"),
                        ui.input_switch('czytajmore8', "Czytaj więcej"),

                        ui.output_ui("dajDivOrze9"),
                        ui.input_switch('czytajmore9', "Czytaj więcej"),
                        

                        ui.include_css("www/my-styles.css"),

          
                        
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

    def dajOrzeczenie(df, i = 1, limit = 1000, tru = True):

        try:
            df['id'][i]
        except:
            return None


        LISTA_GIGA_DUZA = []
        
        
        sygn1 = df['courtCases'][i]
        sedzia1 = ", ".join(df['judges'][i])
        data1 = df['judgmentDate'][i]
        tekst_orze = df['textContent'][i]
        if tru==False:
            tekst_orze = tekst_orze[:limit] + "..."
        else:
            tekst_orze = tekst_orze


        sygn = div(sygn1, id='elem', class_='sygnatura')
        sedzia = div("Skład sędziowski: " + sedzia1, id='elem', class_='sedzia')
        data = div("Data: " + data1, id='elem', class_='data')
        orzeczenie_tekst = div(tekst_orze, id='elem', class_='orzeczenie_tekst')

        idk = (sygn, sedzia, data, orzeczenie_tekst)
        orze_1 = div(idk, id="single_orz", class_='orzeczenie')
        LISTA_GIGA_DUZA.append(orze_1)

        duzy_div_orz = div(LISTA_GIGA_DUZA, id='duzy_div_orz', class_='lista')

        return duzy_div_orz
    
    

    @output
    @render.ui
    def value0():
        return input.czytajmore0()

    @output
    @render.ui
    def value1():
        return input.czytajmore1()

    @output
    @render.ui
    def value2():
        return input.czytajmore2()

    @output
    @render.ui
    def value3():
        return input.czytajmore3()

    @output
    @render.ui
    def value4():
        return input.czytajmore4()

    @output
    @render.ui
    def value5():
        return input.czytajmore5()

    @output
    @render.ui
    def value6():
        return input.czytajmore6()

    @output
    @render.ui
    def value7():
        return input.czytajmore7()

    @output
    @render.ui
    def value8():
        return input.czytajmore8()

    @output
    @render.ui
    def value9():
        return input.czytajmore9()
        


    @output
    @render.ui
    def dajDivOrze0():
        return dajOrzeczenie(df, 0, 1000, input.czytajmore0())

    @output
    @render.ui
    def dajDivOrze1():
        return dajOrzeczenie(df, 1, 1000, input.czytajmore1())

    @output
    @render.ui
    def dajDivOrze2():
        return dajOrzeczenie(df, 2, 1000, input.czytajmore2())

    @output
    @render.ui
    def dajDivOrze3():
        return dajOrzeczenie(df, 3, 1000, input.czytajmore3())

    @output
    @render.ui
    def dajDivOrze4():
        return dajOrzeczenie(df, 4, 1000, input.czytajmore4())

    @output
    @render.ui
    def dajDivOrze5():
        return dajOrzeczenie(df, 5, 1000, input.czytajmore5())

    @output
    @render.ui
    def dajDivOrze6():
        return dajOrzeczenie(df, 6, 1000, input.czytajmore6())

    @output
    @render.ui
    def dajDivOrze7():
        return dajOrzeczenie(df, 7, 1000, input.czytajmore7())

    @output
    @render.ui
    def dajDivOrze8():
        return dajOrzeczenie(df, 8, 1000, input.czytajmore8())

    @output
    @render.ui
    def dajDivOrze9():
        return dajOrzeczenie(df, 9, 1000, input.czytajmore9())
    

app = App(app_ui, server)
app.run(port=8080)