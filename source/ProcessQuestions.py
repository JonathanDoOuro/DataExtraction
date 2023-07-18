import os
import json
import re

path = 'data/output/provasProcessadas'

def abrir(arquivo):
    with open(path + "/" + arquivo, 'r') as file:
        prova = json.load(file)
    return prova

def processarString(texto):
    texto = re.sub(r"[A-Z]+\s-\s\d+º\sdia\s\|\sCaderno\s\d+\s-\s[A-Z]+\s-\sPágina\s\d+\s\d+", "", texto)

    texto = re.sub(r"\n", " ", texto)

    texto = re.sub(r"\t", " ", texto)

    texto = re.sub(r"(?<=\S)\s{2,}(?=\S)", " ", texto)

    texto = re.sub(r"QUESTÃO.*", "", texto)

    return texto

def aplicar_funcao_no_dicionario(dicionario, funcao):
    novo_dicionario = {}
    for chave, valor in dicionario.items():
        novo_valor = funcao(valor)
        novo_dicionario[chave] = novo_valor
    return novo_dicionario

def salvar(file, path):
    with open(path + "/" + "todasQuestoes2.json", "w") as arquivo:
        zipado = json.dumps(file)
        arquivo.write(zipado)

def main():
    listaArquivos = os.listdir(path)
    arquivos = []
    for x in listaArquivos:
        arquivos.append(abrir(x))
    
    todaQuestoes = []
    
    for prova in arquivos:
        for questao in prova:
            if "texto" in questao.keys():
                questao["texto"] = processarString(questao["texto"])

                questao["alternativas"] = aplicar_funcao_no_dicionario(questao["alternativas"], processarString)
                todaQuestoes.append(questao)

    salvar(todaQuestoes, "data/output")


if __name__ == "__main__":
    main()