import json
import re

path = "data/output/provasProcessadas"

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

def salvar(file):
    with open("data/output/" + "dicionarioAvalicao2.json", "w") as arquivo:
        zipado = json.dumps(file)
        arquivo.write(zipado)

def estruturarQuestao(questao):
  retorno = "" 
  if 'texto' in questao:
    retorno += questao["texto"]
    for alternativa, resposta in questao["alternativas"].items():
      retorno = retorno + " " + resposta
  return retorno

def criar_lista_strings_vazias(N):
    lista_strings_vazias = [""] * N
    return lista_strings_vazias

def main():
    prova = abrir("enem2015_PV_impresso_D1_CD1.pdf.json")
    questoes = []
    for questao in prova:
        if "texto" in questao.keys():
            questao["texto"] = processarString(questao["texto"])

            questao["alternativas"] = aplicar_funcao_no_dicionario(questao["alternativas"], processarString)
            questoes.append(estruturarQuestao(questao))
    
    data = dict()
    data["questoes"] = questoes
    data["labels"] = criar_lista_strings_vazias(len(questoes))
    salvar(data)



if __name__ == "__main__":
  main()