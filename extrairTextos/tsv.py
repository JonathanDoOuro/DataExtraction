import csv
import json
import random
import nltk
import re
from nltk.stem import WordNetLemmatizer
import string
import spacy

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

with open("extrairTextos/DataSetGeral/biologia_train_dataset.json", "r") as file:
    docs = json.load(file)

textos, titulos, keywords = zip(*docs)

def preprocess_text(textos):
    # Carrega o modelo do SpaCy para o idioma português
    nlp = spacy.load("pt_core_news_sm")
    
    # Lista para armazenar os textos processados
    textos_processados = []
    
    # Processa cada texto
    for texto in textos:
        # Aplica o pipeline do SpaCy para lematização e remoção de stop words
        doc = nlp(texto)
        
        # Lematização das palavras e remoção de stop words
        palavras_lematizadas = [token.lemma_ for token in doc if not token.is_stop]
        
        # Reconstroi o texto a partir das palavras lematizadas
        texto_processado = ' '.join(palavras_lematizadas)
        
        # Adiciona o texto processado à lista de textos processados
        textos_processados.append(texto_processado)
    
    return textos_processados

porcentagem_train = 0.8
porcentagem_test = 0.1
porcentagem_val = 0.1

# Dados para as colunas
coluna1 = preprocess_text(textos)
# Criar a lista coluna2
total_elementos = len(coluna1)
num_train = int(total_elementos * porcentagem_train)
num_test = int(total_elementos * porcentagem_test)
num_val = total_elementos - num_train - num_test
coluna2 = ["train"] * num_train + ["test"] * num_test + ["val"] * num_val
random.shuffle(coluna2)

coluna3 = titulos

# Caminho para o arquivo de saída
caminho_arquivo = 'extrairTextos/DataSetOctis/corpus.tsv'

# Abre o arquivo em modo de escrita
with open(caminho_arquivo, 'w', newline='', encoding='utf-8') as arquivo_tsv:
    writer = csv.writer(arquivo_tsv, delimiter='\t')

    # Escreve os dados em cada linha
    for i in range(len(coluna1)):
        writer.writerow([coluna1[i], coluna2[i], coluna3[i]])

# Baixa a lista de stop words (se ainda não foi baixada)


stopwords_personalizadas = ["e/ou"]

# Carrega a lista de stop words em português
stopwords = nltk.corpus.stopwords.words('portuguese')
stopwords.extend(stopwords_personalizadas)


# Expressão regular para filtrar apenas palavras
regex = re.compile(r'\b[a-zA-Z]+\b')

# Lista para armazenar as palavras do vocabulário
vocabulario = []
lemmatizer = WordNetLemmatizer()
# Itera sobre os textos
for texto in textos:
    # Tokeniza o texto em palavras
    palavras = nltk.word_tokenize(texto.lower())

    # Filtra as palavras que não são stop words nem números
    palavras_filtradas = [palavra for palavra in palavras if palavra not in stopwords and not palavra.isdigit()]

    # Aplica a expressão regular para filtrar apenas palavras
    palavras_filtradas = [palavra for palavra in palavras_filtradas if regex.match(palavra)]

    palavras_lematizadas = [lemmatizer.lemmatize(palavra) for palavra in palavras_filtradas]

    # Adiciona as palavras filtradas ao vocabulário
    vocabulario.extend(palavras_filtradas)

# Remove duplicatas do vocabulário
vocabulario = list(set(vocabulario))

# Caminho para o arquivo de saída
caminho_arquivo = 'extrairTextos/DataSetOctis/vocabulary.txt'

# Abre o arquivo em modo de escrita
with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
    # Escreve uma palavra por linha
    for palavra in vocabulario:
        arquivo.write(palavra + '\n')