import time
import requests
import random
import re
import json
import pickle
from bs4 import BeautifulSoup

biologia = [
    "Biologia celular",
    "Genética",
    "Evolução biológica",
    "Ecologia",
    "Anatomia",
    "Fisiologia",
    "Reprodução",
    "Saúde",
    "Microbiologia",
    "Biodiversidade",
    "Classificação dos seres vivos",
    "Organismos unicelulares",
    "Organismos multicelulares",
    "Metabolismo",
    "Sistemas corporais",
    "Adaptações evolutivas",
    "Cadeias alimentares",
    "Ecossistemas",
    "Biomas",
    "Ciclos biogeoquímicos",
    "Conservação ambiental",
    "Interações simbióticas",
    "Biologia molecular",
    "Expressão gênica",
    "Biologia do desenvolvimento",
    "Biologia humana",
    "Neurociência",
    "Imunologia",
    "Genética populacional",
    "Engenharia genética"
]

def filtrar_texto(texto):
    # Expressão regular para encontrar a expressão matemática
    pattern = r'\\{0,2}\n*\{\\displaystyle.*?\n*\}'

    # Substitui a expressão matemática encontrada por uma string vazia
    texto_filtrado = re.sub(pattern, '', texto)

    # Remove espaços e quebras de linha desnecessários
    texto_filtrado = re.sub(r'\s+', ' ', texto_filtrado).strip()

    return texto_filtrado.replace("\n", "")

def contar_palavras(texto):
    palavras = re.findall(r'\b[a-zA-Z]{5,}\b', texto)  # Encontra palavras formadas por letras com mais de 4 letras
    return len(palavras)

def possui_muitos_simbolos(texto, limite_proporcao=0.1):
    # Remove espaços em branco para contar apenas caracteres
    texto = texto.replace(" ", "")

    # Conta a quantidade total de caracteres
    total_caracteres = len(texto)

    # Encontra os caracteres não alfabéticos
    caracteres_nao_alfabeticos = re.findall(r'[^a-zA-Z]', texto)

    # Conta a quantidade de caracteres não alfabéticos
    total_nao_alfabeticos = len(caracteres_nao_alfabeticos)

    # Calcula a proporção de caracteres não alfabéticos
    proporcao_nao_alfabeticos = total_nao_alfabeticos / total_caracteres

    # Verifica se a proporção ultrapassa o limite estabelecido
    if proporcao_nao_alfabeticos > limite_proporcao:
        return True
    else:
        return False
    
def searchPages(keywords, max_pages_per_keyword, api_url):
    pageTitles = []
    for keyword in keywords:
        print("Palavra-chave:", keyword)

        # Parâmetros da consulta de pesquisa
        search_params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": keyword,
            "srlimit": max_pages_per_keyword,
        }

        # Faz a requisição de pesquisa à API
        search_response = requests.get(api_url, params=search_params)
        search_data = search_response.json()
        # Obtém a lista de títulos das páginas
        page_titles = [result["title"] for result in search_data["query"]["search"]]

        # Seleciona aleatoriamente títulos das páginas
        random_page_titles = random.sample(page_titles, min(max_pages_per_keyword, len(page_titles)))
        print("         titulos associados: ", random_page_titles)
        pageTitles.append(random_page_titles)
    return pageTitles

def getTextFromPage(titles_per_page, api_url):
    train_dataset = []
    for page in titles_per_page:
        for title in page:
            print("       Titulo:", title)
            page_params = {
                "action": "parse",
                "format": "json",
                "prop": "text",
                "page": title
            }

            page_response = requests.get(api_url, params=page_params)
            page_data = page_response.json()
            print(page_data["parse"]["pageid"], page_data["parse"]["title"])
            page_html = page_data["parse"]["text"]["*"]

            soup = BeautifulSoup(page_html, "html.parser")

            main_content_div = soup.find("div", class_="mw-parser-output")
            for element in main_content_div:
                if element.name == "p":
                    if(contar_palavras(element.get_text()) >= 15 and (not possui_muitos_simbolos(element.get_text()))):
                        train_dataset.append((filtrar_texto(element.get_text()), title))
    return train_dataset

def obter_categorias_por_id(id_pagina):
    url_base = "https://pt.wikipedia.org/w/api.php"

    # Parâmetros da requisição
    params = {
        "action": "query",
        "format": "json",
        "pageids": id_pagina,
        "prop": "categories"
    }

    # Fazendo a requisição à API da Wikipedia
    response = requests.get(url_base, params=params)
    data = response.json()

    # Verificando se o ID da página é válido
    if "-1" in data["query"]["pages"]:
        print("ID de página inválido.")
        return

    # Obtendo as categorias da página
    page = data["query"]["pages"][id_pagina]
    categories = page.get("categories")

    # Exibindo as categorias
    if categories:
        print(f"Categorias da página com ID {id_pagina}:")
        for category in categories:
            print(category["title"])
    else:
        print(f"A página com ID {id_pagina} não possui categorias.")

def main():
    bio2 = [ "Biologia celular",
    "Anatomia"]
    api_url = "https://pt.wikipedia.org/w/api.php"
    max_pages_per_keyword = 6
    # titles_per_page = searchPages(bio2, max_pages_per_keyword, api_url)
    # getTextFromPage(titles_per_page, api_url)
    obter_categorias_por_id("259880")


if __name__ == "__main__":
    main()