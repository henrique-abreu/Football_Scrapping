from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time
import os


def tratar_dados_dentro_dict(lista_final):

    #Necessário juntar os dados das rondas pois, no site existe rondas com o mesmo número espalhadas pela página.
    #Seria ideal juntar, para estar todos os jogos dentro da mesma ronda/jornada
    #FAZER!!!!!!!!!!

    pass

def trabalhar_string(ficheiro):

    #Variaveis para armazenar valores
    lista_final = []
    lista_lines = []
    dictionary_final = {}
    ronda = ''
    data = []
    equipa = []
    resultado = []

    #Abrir o ficheiro e meter cada linha do HTML na lista "lista_lines"
    with open(ficheiro, "r") as file:
        for line in file.readlines():
            lista_lines.append(line)

    #Percorrer a lista "lista_lines" e, quando encontrar uma específica
    #linha (classes referentes às rondas, data, equipas e resultado)
    #guardar os valores nas variáveis, e depois guardar numa nova lista, o dictionary já com a informação ideal.
    for index, item in enumerate(lista_lines):
        if "event__round event__round--static" in item and ronda == '':
            ronda = lista_lines[index + 1]
        elif "event__time" in item:
            data.append(lista_lines[index + 1].strip())
        elif "event__participant event__participant--home" in item:
            equipa.append(lista_lines[index + 1].strip() + ' vs ' + lista_lines[index + 5].strip())
        elif "event__scores" in item:
            resultado.append(lista_lines[index + 2].strip() + lista_lines[index + 4].strip() + lista_lines[index + 6].strip())
        elif "event__round event__round--static" in item and ronda != '':
            dictionary_final["Ronda_Numero"] = ronda.strip()
            dictionary_final["Data"] = data
            dictionary_final["Equipa"] = equipa
            dictionary_final["Resultado"] = resultado
            lista_final.append(dictionary_final)
            ronda = lista_lines[index + 1]
            data = []
            equipa = []
            resultado = []
            dictionary_final = {}
        elif index + 1 == len(lista_lines):
            dictionary_final["Ronda_Numero"] = ronda.strip()
            dictionary_final["Data"] = data
            dictionary_final["Equipa"] = equipa
            dictionary_final["Resultado"] = resultado
            lista_final.append(dictionary_final)
            ronda = ''
            data = []
            equipa = []
            resultado = []
            dictionary_final = {}

    #Testar Resultados#######################################################################
    print(lista_final[2]["Ronda_Numero"])
    print(lista_final[2]["Data"][3])
    print(lista_final[2]["Equipa"][3])
    print(lista_final[2]["Resultado"][3])
    ##########################################################################################

    #tratar_dados_dentro_dict(lista_final)
    pass

def guardar_ficheiro(html_string):

    #Guardar o código em HTML num novo ficheiro na pasta "folder_path"
    folder_path = "html_files/"
    ficheiro_completo_path = folder_path + "html_string.html"

    #Caso já existam ficheiros nessa pasta, elimina tudo
    for ficheiro in os.listdir(folder_path):
        if len(os.listdir(folder_path)) > 0:
            os.remove(folder_path + ficheiro)

    #escreve o ficheiro e guarda na pasta
    file = open(ficheiro_completo_path, "w")
    file.write(html_string.prettify())
    file.close()

    #enviar para outra função o ficheiro
    trabalhar_string(ficheiro_completo_path)
    pass

def give_link(link, number_times_show_button_appears):

    #Driver
    chrome_browser = webdriver.Chrome('./chromedriver.exe')
    chrome_browser.maximize_window()

    #Ir para o Link
    chrome_browser.get(link)

    #Aceitar as cookies do site //// FAZER! É preciso esperar que as cookies façam load, senão dá erro! Ainda não está feito
    cookies = chrome_browser.find_element_by_id('onetrust-accept-btn-handler').click()

    #Continuar a clicar no botão enquanto enquanto i menor que 3, porque sabemos que na página são 3 cliques no botão
    #Falta aqui um try para se não houver mais vezes o botão "Show more matches" para clicar, para passar
    #para a próxima linha. FALTA!!!!!!!!
    #Clicar no botão "Show more", dependendo do número que mandamos inicialmente para a função.
    i = 0
    while int(i) < int(number_times_show_button_appears):
        show_button1 = chrome_browser.find_element_by_xpath('//*[@id="live-table"]/div[1]/div/div/a').click()
        time.sleep(3)
        i += 1

    #Guardar o código HTML, desde a classe que tem toda a informação
    jogos = chrome_browser.find_element_by_xpath('//*[@id="live-table"]/div').get_attribute('outerHTML')
    chrome_browser.quit()
    html_string = BeautifulSoup('<html><head><title></title></head><body>' + str(jogos) + '</body></html>','html.parser')

    #Não consegui fazer parse. Ele em vez de tratar o html linha a linha, ele interpreta aquilo como uma string total.
    #Então decide guardar num ficheiro (serve de intermediário), para depois já puder trabalhar linha a linha.
    #Enviar o código HTML para ser guardado num ficheiro.
    guardar_ficheiro(html_string)
    pass

if __name__=="__main__":
    give_link("https://www.flashscore.com/football/england/premier-league-2020-2021/results/", 3)