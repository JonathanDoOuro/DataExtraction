import csv
import json
import random
import nltk
import re
import string
import spacy
import time

def preprocess_text(textos, nlp_model):
    inicio = time.time()
    print(inicio)
    pontuacao = set(string.punctuation)
    textos_processados = [
        ' '.join(token.lemma_ for token in nlp_model(texto.lower()) if not token.is_stop and not token.is_punct and not token.is_digit and not any(char in pontuacao for char in str(token))) for texto in textos
    ]
    fim = time.time()
    tempo_execucao = fim - inicio
    print("Tempo de execução:", tempo_execucao, "segundos")
    return textos_processados

def particao(n: int):
    porcentagem_train = 0.8
    porcentagem_test = 0.1
    num_train = int(n * porcentagem_train)
    num_test = int(n * porcentagem_test)
    num_val = n - num_train - num_test
    coluna2 = ["train"] * num_train + ["test"] * num_test + ["val"] * num_val
    random.shuffle(coluna2)
    return coluna2

def salvarCorpus(caminho_arquivo, coluna1, coluna2, coluna3):
    with open(caminho_arquivo, 'w', newline='', encoding='utf-8') as arquivo_tsv:
        writer = csv.writer(arquivo_tsv, delimiter='\t')

        # Escreve os dados em cada linha
        for i in range(len(coluna1)):
            writer.writerow([coluna1[i], coluna2[i], coluna3[i]])

def lerDataSet():
    with open("extrairTextos/DataSetGeral/biologia_test_dataset.json", "r") as file:
        docs = json.load(file)

    textos, titulos, keywords = zip(*docs)

    return (textos, titulos, keywords)

def vocabulario(textos: list):
    stopwords_personalizadas = ["e/ou"]
    stopwords = nltk.corpus.stopwords.words('portuguese')
    stopwords.extend(stopwords_personalizadas)
    # Expressão regular para filtrar apenas palavras
    regex = re.compile(r'\b[a-zA-Z]+\b')

    vocabulario = []

    for texto in textos:
        # Tokeniza o texto em palavras
        palavras = nltk.word_tokenize(texto.lower())

        # Filtra as palavras que não são stop words nem números
        palavras_filtradas = [palavra for palavra in palavras if palavra not in stopwords and not palavra.isdigit() and regex.match(palavra)]

        vocabulario.extend(palavras_filtradas)

    return list(set(vocabulario))

def salvarVocabulario(caminho_arquivo, vocabulario: list):
    with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
        for palavra in vocabulario:
            arquivo.write(palavra + '\n')

def main():
    nlp = spacy.load("pt_core_news_md")
    caminho_corpus = 'extrairTextos/DataSetOctis/corpus.tsv'
    dataSet = lerDataSet()
    coluna1 = preprocess_text(dataSet[0], nlp)
    coluna2: list = particao(len(dataSet[0]))
    coluna3 = dataSet[1]
    
    salvarCorpus(caminho_corpus, coluna1, coluna2, coluna3)

    caminho_vocabulario = 'extrairTextos/DataSetOctis/vocabulary.txt'
    vocabulario1 = vocabulario(coluna1)
    salvarVocabulario(caminho_vocabulario, vocabulario1)

if __name__ == "__main__":
    main()