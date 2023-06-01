import requests
import random

# Palavra-chave para pesquisa de páginas de biologia
keyword = "matemática"

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

# Obtém o texto de cada página selecionada
for title in random_page_titles:
    # Parâmetros da consulta para obter o texto da página
    page_params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "exintro": True,
        "explaintext": True,
        "titles": title
    }

    # Faz a requisição à API para obter o texto da página
    page_response = requests.get(api_url, params=page_params)
    page_data = page_response.json()

    # Obtém o texto da página
    page_id = list(page_data["query"]["pages"].keys())[0]
    page_text = page_data["query"]["pages"][page_id]["extract"]

    # Imprime o título e o texto da página
    with open(f'{title}.txt', "w") as file:
        print("Texto: ", page_text, file=file)
        print("\n---\n")