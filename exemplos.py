palavrasChave = []
import string
import spacy

def recuperarTextosWikipidia(palavraChave):
    pass

def removerConteudoNaoAlfabetico(texto):
    pass

def maisQue15Palavras(texto):
    pass

def removerStopWordsElematizar(textos, nlp_model):
    pontuacao = set(string.punctuation)
    textos_processados = [
        ' '.join(str(token.lemma_) for token in nlp_model(texto.lower()) if not token.is_stop and not token.is_punct and not token.is_digit and not any(char in pontuacao for char in str(token))) for texto in textos
    ]
    return textos_processados

for palavraChave in palavrasChave:
    textos = recuperarTextosWikipidia(palavraChave)
    textos = removerConteudoNaoAlfabetico(textos)
    textos = list(filter(maisQue15Palavras, textos))
    nlp = spacy.load("pt_core_news_lg")
    textos = removerStopWordsElematizar(textos, nlp)
