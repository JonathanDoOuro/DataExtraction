from DataExtractor import DataExtractor
import os

if __name__ == "__main__":
    #paths:
    inputPath = "data/input"
    outputPath = "data/output"

    extrator = DataExtractor(outputPath=outputPath)
    extrator.setInputPath(inputPath=inputPath)

    #loop na pasta input
    pasta_input = os.listdir(inputPath)
    for arquivo in pasta_input:
        texto = extrator.extrair_texto_do_pdf(arquivo)
        questoes = extrator.questoesJson(texto, 72)

        #ecrita do json
        with open(f'{outputPath}/{arquivo}.json', 'w') as file:
           print(questoes, file=file)