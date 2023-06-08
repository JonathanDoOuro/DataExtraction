import time
import requests
import random
import pickle
from bs4 import BeautifulSoup

# Lista de palavras-chave
portugues = [
    "Língua como fenômeno sociocultural, histórico e geopolítico",
    "Práticas de linguagem",
    "Produção e negociação de sentidos entre os interlocutores",
    "Recursos linguísticos",
    "Variação linguística",
    "Elementos lexicais",
    "Elementos semânticos",
    "Elementos gramaticais",
    "Construção de sentidos e uso crítico da língua",
    "Intertextualidade",
    "Relações lógico-discursivas",
    "Funcionamento social da língua",
    "Circulação dos discursos",
    "Usos linguísticos na norma culta",
    "Elementos sintáticos",
    "Estrutura do vocábulo",
    "Classes morfológicas",
    "Elementos de fonologia",
    "Recursos fonético-fonológicos"
]

literatura = [
    "Literaturas de língua portuguesa",
    "Fruição estética",
    "Manifestações artísticas em contextos diferentes",
    "Romances",
    "Contos",
    "Crônicas",
    "Prosa literária",
    "Representação do sentimento na prosa",
    "Elaboração estética do cotidiano na prosa",
    "Persuasão na prosa",
    "Linguagem poética",
    "Formas convencionais da poesia",
    "Poesia lírica",
    "Análise de poemas",
    "Recursos formais da poesia",
    "Verso de poema",
    "Estrofe de poema",
    "Metro de poesia",
    "Ritmo de poema",
    "Sonoridade de poema",
    "Expressão poética",
    "Figuras de linguagem",
    "Texto teatral",
    "Teatro",
    "Sobrevivendo no inferno Racionais",
    "O Espelho de Machado de Assis",
    "O marinheiro de Fernando Pessoa",
    "A falência de Júlia Lopes de Almeida"
    "Sermões de Padre Antonio Vieira",
    "O Ateneu de Raul Pompéia"
    ]

matematica = [
    "Conjuntos numéricos",
    "subconjuntos",
    "União, interseção de conjuntos",
    "Números naturais",
    "Números inteiros",
    "Sistema de numeração",
    "Números reais",
    "progressão aritmética",
    "progressão geométrica",
    "Funções lineares",
    "Funções quadráticas",
    "Funções matematicas",
    "Equações e inequações com funções",
    "Polinômios",
    "princípios de contagem",
    "arranjos de contagem", "combinações de contagem", "permutações", 
    "espaço amostral", "probabilidade da união",
    "probabilidade da interseção de eventos", "probabilidade condicional", 
    "binômio de Newton",
    "matrizes", "determinante de matriz" ,"sistemas lineares",
    "Geometria plana",
    "Geometria espacial",
    "Trigonometria",
    "Geometria analítica",
    "Logaritmos",
    "funções exponenciais"
    ]

sociologia = [
    "homem como ser social", 
    "grupos sociais", 
    "sociabilidade", 
    "etnias", 
    "classes sociais", 
    "gênero", "geração", 
    "dimensões demográficas", 
    "dimensões urbanas", "dimensões produtivas", 
    "população mundial", 
    "urbanização", 
    "circuitos da produção", "comércio internacional", 
    "globalização financeira e produtiva", "geografia das redes", 
    "transformações no mundo do trabalho", 
    "dimensão cultural", "movimentos sociais", 
    "direitos humanos", "violências no mundo contemporâneo"]

geografia = [
    "Espaço geográfico",
    "Território",
    "Meio urbano",
    "Redes técnicas",
    "Fronteiras",
    "Linguagem cartográfica",
    "Geotecnologias",
    "Coordenadas geográficas",
    "Movimentos da órbita terrestre",
    "Fusos horários",
    "Princípios da cartografia sistemática",
    "Projeções cartográficas",
    "Escalas cartográficas",
    "Hidrosfera",
    "Atmosfera",
    "Criosfera",
    "Dinâmicas atmosféricas",
    "Zonalidade climática",
    "Elementos do clima",
    "Aquecimento global",
    "Bacias hidrográficas",
    "Oceanos e mares",
    "Organização político-territorial",
    "Globalização e regionalização mundial",
    "Geopolítica e geoeconomia",
    "Conflitos territoriais",
    "Matrizes energéticas",
    "Organização político-territorial do Brasil",
    "Formação territorial do Brasil",
    "Políticas territoriais",
    "Estado e governo",
    "Economia e território",
    "Industrialização",
    "Agropecuária",
    "Mercado de trabalho",
    "Redes de energia e transportes",
    "Urbanização",
    "Metropolização",
    "Segregação socioespacial",
    "Movimentos sociais"
]

historia = [
    "Grécia",
    "Roma",
    "Medievo",
    "Império Bizantino",
    "Mundo árabe",
    "Feudalismo",
    "Capitalismo",
    "Renascimento",
    "Estado Moderno",
    "Monarquias confessionais",
    "Absolutismo",
    "Mercantilismo",
    "Expansão marítima europeia",
    "Impérios coloniais",
    "Conquista e colonização das Américas",
    "Iluminismo",
    "Crise do Antigo Regime",
    "Liberalismo",
    "Revoluções burguesas",
    "Consolidação do Estado burguês",
    "Nacionalismo",
    "Industrialização",
    "Urbanização",
    "Doutrinas socialistas",
    "Abolicionismo",
    "Escravismo",
    "Migrações",
    "Imperialismo europeu",
    "Partilha colonial",
    "Brasil no século XIX",
    "Escravidão",
    "Revolução Mexicana",
    "Revolução Russa",
    "Revolução Chinesa",
    "Revolução Cubana",
    "Crise do liberalismo",
    "Fascismos",
    "Regimes totalitários",
    "Guerras mundiais",
    "Populismos na América Latina",
    "Descolonização",
    "Ditadura civil-militar no Brasil",
    "Memórias",
    "Cultura de massas",
    "Redemocratizações na América Latina",
    "Fim dos regimes comunistas",
    "Primavera árabe",
    "Globalização",
    "Multiculturalismo"
]

filosofia = [
    "surgimento da filosofia", "conceito de medievo", "ocidente medieval", "império bizantino", 
    "mundo árabe", "Islamismo", "crise do feudalismo", "capitalismo", "Renascimento", "Reformas", 
    "Estado Moderno", "monarquias confessionais", "absolutismo", "mercantilismo", "expansão marítima europeia", 
    "descobrimentos", "iluminismo", "pensamento filosófico no século XIX", 
    "transformações sociais e culturais no século XXI"]

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

fisica = [
    "Grandezas físicas",
    "Cinemática",
    "Leis de Newton",
    "Equilíbrio",
    "Lei da gravitação",
    "Quantidade de movimento",
    "Trabalho e energia",
    "Termodinâmica",
    "Óptica",
    "Ondas",
    "Eletricidade e magnetismo",
    "Mecânica dos fluídos",
    "Campos elétricos e magnéticos",
    "Eletrostática",
    "Corrente elétrica",
    "Circuitos elétricos",
    "Leis de Kirchhoff",
    "Forças magnéticas",
    "Indução eletromagnética",
    "Óptica geométrica",
    "Óptica ondulatória",
    "Lentes e espelhos",
    "Interferência e difração",
    "Fenômenos térmicos",
    "Leis da termodinâmica",
    "Calorimetria",
    "Ondas sonoras",
    "Ondas eletromagnéticas",
    "Física nuclear",
    "Física de partículas"
]

quimica = [
    "Propriedades da matéria",
    "Gases",
    "Líquidos e sólidos",
    "Estrutura atômica",
    "Ligações químicas",
    "Transformações químicas",
    "Estequiometria",
    "Cinética química",
    "Equilíbrio químico",
    "Ácidos e bases",
    "Química orgânica",
    "Recursos naturais",
    "Tabela periódica",
    "Reações químicas",
    "Equações químicas",
    "Funções inorgânicas",
    "Solubilidade",
    "pH e pOH",
    "Equilíbrio ácido-base",
    "Oxidação e redução",
    "Termoquímica",
    "Catalisadores",
    "Estequiometria avançada",
    "Polímeros",
    "Química ambiental",
    "Química forense",
    "Química farmacêutica",
    "Radioatividade",
    "Espectroscopia",
    "Química analítica"
]

sample_test = ["homem como ser social", 
    "grupos sociais",
    "demografia"]

keywords = portugues + literatura + matematica + sociologia + geografia + historia + filosofia + biologia + fisica + quimica

train_dataset = []

test_dataset = []

# URL da API do MediaWiki
api_url = "https://pt.wikipedia.org/w/api.php"

# Número máximo de páginas para cada palavra-chave
max_pages_per_keyword = 4

# Itera sobre as palavras-chave
for keyword in keywords:
    inicio = time.time()
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

    i = 0
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
                if(i != 3):
                    train_dataset.append((element.get_text(), title))
                elif (i == 3):
                    test_dataset.append((element.get_text(), title))
        i+=1
    fim = time.time()  # Captura o tempo de término
    tempo_execucao = fim - inicio
    texto_pagina = [linha for linha in filtered_text.split("\n") if linha.strip()]
    print("Tempo de execução:", tempo_execucao, "segundos")


with open("train_dataset.pickle", "wb") as arquivo:
    pickle.dump(train_dataset, arquivo)

with open("test_dataset.pickle", "wb") as arquivo:
    pickle.dump(test_dataset, arquivo)


        with open(f'{keyword}/{title}.txt', "w") as file:
            print(filtered_text, file=file)
            print("\n---\n")