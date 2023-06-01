import requests
import random
from bs4 import BeautifulSoup

# Palavra-chave para pesquisa de páginas de biologia
keyword = "genética"

# URL da API do MediaWiki
api_url = "https://pt.wikipedia.org/w/api.php"

# Parâmetros da consulta de pesquisa
search_params = {
    "action": "query",
    "format": "json",
    "list": "search",
    "srsearch": keyword,
    "srlimit": 100  # Número máximo de resultados de pesquisa
}

# Faz a requisição de pesquisa à API
search_response = requests.get(api_url, params=search_params)
search_data = search_response.json()

# Obtém a lista de títulos das páginas de biologia
page_titles = [result["title"] for result in search_data["query"]["search"]]

# Seleciona aleatoriamente 100 títulos das páginas de biologia
random_page_titles = random.sample(page_titles, 100)

# Obtém o texto principal de cada página selecionada
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
    
    with open(f'{title}.txt', "w") as file:
        print(filtered_text, file=file)
        print("\n---\n")