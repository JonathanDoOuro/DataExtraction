import random
from DataExtractor import DataExtractor
import os
import re

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

if __name__ == "__main__":
    #paths:
    inputPath = "data/input"
    outputPath = "data/output"

    extratorQuestoes = DataExtractor(outputPath=outputPath)
    extratorQuestoes.setInputPath(inputPath=inputPath)

    #loop na pasta input
    pasta_input = os.listdir(inputPath)

    random_list = [random.randint(0, len(pasta_input)-1) for _ in range(3)]

    #for i in random_list:
    arquivo = 'enem2013_PV_impresso_D1_CD2.pdf'
    print(arquivo)
    metaData = simpleMetaData(arquivo)
    extratorQuestoes.setMetaData(vestibular=metaData["vestibular"],
                                    ano=metaData["data_prova"],
                                    qtd_alternativas=metaData["qtd_alternativas"],
                                    codigo=metaData["codigo"],
                                    qtd_questoes=metaData["qtd_questoes"])

    #extrai o texto completo do pdf e retorna uma string
    texto = extratorQuestoes.extrair_texto_do_pdf(arquivo)
    #processa o texto e extrai cada questão separadamente
    questoes = extratorQuestoes.questoesJson(texto)
    #TO DO: extrair as respostas e salvar nos metadados da questao
    #       antes de salvar o json
    
    #salva as questões em um arquivo json
    with open(f'{outputPath}/{arquivo}.json', 'w') as file:
        print(questoes, file=file)