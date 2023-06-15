import re
import string
import spacy

def preprocess_text(textos):
    # Carrega o modelo do SpaCy para o idioma português
    pontuacao = set(string.punctuation)
    nlp = spacy.load("pt_core_news_sm")
    x = []
    for texto in textos:
        doc = nlp(texto.lower())
        for token in doc:
            if not any(char in pontuacao for char in str(token)):
                x.append(token)
                print(token)
    return x

textos = ["A teoria 4 celular é um 43243 dos conhecimentos fundamentais da biologia. Agora universalmente aceita, a teoria celular afirma que todos os seres vivos são compostos por células, a unidade estrutural e organizacional básica de todos os organismos e que todas as células vêm de células pré-existentes.",
        "A descoberta da célula só foi possível graças à invenção do microscópio. Durante o século I d.C., os romanos produziam vidro e testavam diferentes tipos de vidro transparente, descobrindo que certas lentes postas sob um objeto faziam-no parecer maior.[3] As lentes foram popularizadas apenas por volta do ano 1280, na Itália, com a invenção dos óculos, o que provavelmente levou ao uso mais amplo de microscópios simples. Na época, começaram também as primeiras experiências de combinação de lentes para aplicação em instrumentos de ampliação de imagens, resultando na criação do primeiro microscópio composto (duas ou mais lentes).[4]"]
    
coluna1 = preprocess_text(textos)

print(coluna1[1])