import requests
import random
from bs4 import BeautifulSoup

# Lista de palavras-chave para pesquisa de páginas de biologia
keywords = ["brasil colonia", "escravidao no brasil"]

# URL da API do MediaWiki
api_url = "https://pt.wikipedia.org/w/api.php"

# Número máximo de páginas para cada palavra-chave
max_pages_per_keyword = 15

# Itera sobre as palavras-chave
for keyword in keywords:
    print("Palavra-chave:", keyword)

    # Parâmetros da consulta de pesquisa
    search_params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": keyword,
        "srlimit": max_pages_per_keyword
    }

    # Faz a requisição de pesquisa à API
    search_response = requests.get(api_url, params=search_params)
    search_data = search_response.json()

    # Obtém a lista de títulos das páginas
    page_titles = [result["title"] for result in search_data["query"]["search"]]

    # Seleciona aleatoriamente títulos das páginas
    random_page_titles = random.sample(page_titles, min(max_pages_per_keyword, len(page_titles)))

    # Itera sobre os títulos das páginas selecionadas
    for title in random_page_titles:
        # Parâmetros da consulta para obter o texto completo da página
        page_params = {
            "action": "parse",
            "format": "json",
            "prop": "text",
            "page": title
        }

        # Faz a requisição à API para obter o texto completo da página
        page_response = requests.get(api_url, params=page_params)
        page_data = page_response.json()

        # Obtém o conteúdo HTML da página
        page_html = page_data["parse"]["text"]["*"]

        # Faz o parsing do conteúdo HTML usando a biblioteca BeautifulSoup
        soup = BeautifulSoup(page_html, "html.parser")

        # Encontra a div do texto principal da página
        main_content_div = soup.find("div", class_="mw-parser-output")

        # Filtra as seções indesejadas e obtém somente o texto principal
        filtered_text = ""
        for element in main_content_div:
            if element.name == "p":  # Filtra apenas parágrafos
                filtered_text += element.get_text()

        with open(f'{keyword}/{title}.txt', "w") as file:
            print(filtered_text, file=file)
            print("\n---\n")