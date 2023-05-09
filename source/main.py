import random
from DataExtractor import DataExtractor
import os
import re
from integration import BancoMongo

def simpleMetaData(arquivo):
    '''
        Extrai os metadados com base no nome do arquivo.
        No momento trata os casos do enem e unicamp.
    '''
    anoBruto = re.findall('\d+', arquivo)
    if anoBruto:
        ano = int(anoBruto[0])
    vestibular = re.match(r'\D*', arquivo).group()
    codigo = re.search(r'\d+(.*)', arquivo).group(1)
    codigo = codigo.replace(".pdf", "")

    numeroQuestoes = 0
    qtdAlternativas = 0

    if (vestibular == "unicamp"):
        qtdAlternativas = 4
        if (ano >= 2021):
            numeroQuestoes = 72
        else:
            numeroQuestoes = 90
    elif (vestibular == "enem"):
        qtdAlternativas = 5
        pattern = r'_D(\d+)'
        match = re.search(pattern, codigo)
        if match:
            dia = match.group(0)
            if (dia == "_D1"):
                numeroQuestoes = 90
            elif (dia == "_D2"):
                numeroQuestoes = 180

    return {"data_prova": ano, 
            "vestibular": vestibular, 
            "codigo": codigo, 
            "qtd_alternativas": qtdAlternativas, 
            "qtd_questoes": numeroQuestoes
            }

def extrairDados(pasta_input, extratorQuestoes: DataExtractor, outputPath):
    for arquivo in pasta_input:
        print("extraindo: ", arquivo)
        metaData = simpleMetaData(arquivo)
        extratorQuestoes.setMetaData(vestibular=metaData["vestibular"],
                                        ano=metaData["data_prova"],
                                        qtd_alternativas=metaData["qtd_alternativas"],
                                        codigo=metaData["codigo"],
                                        qtd_questoes=metaData["qtd_questoes"])
        #extrai o texto completo do pdf e retorna uma string
        texto = extratorQuestoes.extrair_texto_do_pdf(arquivo)
        #salva o texto extraido
        with open(f'{outputPath}/{arquivo}.txt', 'w') as file:
            print(texto, file=file)
        #processa o texto e extrai cada questão separadamente
        questoes = extratorQuestoes.questoes(texto=texto, salvar=False)
        #salva as questões em um arquivo json
        with open(f'{outputPath}/{arquivo}.json', 'w') as file:
            print(questoes, file=file)

def main():
    #paths
    inputPath = "data/input"
    outputPath = "data/output"

    #banco de questoes
    bancoMongo = BancoMongo("mongodb://root:example@localhost:27017")
    bancoMongo.setDb("ProjetoQuiz")
    bancoMongo.setCollection("questoes")

    #extrator de questoes
    extratorQuestoes = DataExtractor(outputPath=outputPath)
    extratorQuestoes.setInputPath(inputPath=inputPath)
    extratorQuestoes.setBancoDados(bancoMongo)

    #pasta de arquivos do input
    pasta_input = os.listdir(inputPath)

    #extrair pdf e salva em uma pasta o texto completo e as questões
    extrairDados(pasta_input=pasta_input, extratorQuestoes=extratorQuestoes, outputPath=outputPath)

if __name__ == "__main__":
    main()