import json
import re
import fitz
import os

class GabaritoExtractor:
    def __init__(self, outputPath):
        self.outputPath = outputPath

    def setInputPath(self, inputPath):
        self.inputPath = inputPath

    def extrair_texto_do_pdf(self, arquivo):
        doc = fitz.open(f'{self.inputPath}/{arquivo}')  # open document
        texto = ''
        for page in doc:  #iterate the document pages
            text = page.get_text(sort=False)  # get plain text (is in UTF-8)
            texto += text
        return texto
    
    def extrair_gabarito(self, texto):
        padrao = r'(\d+)\n([A-Z])\n'
        matches = re.findall(padrao, texto)
        
        gabarito = {}
        for match in matches:
            numero = int(match[0])
            resposta = match[1]
            gabarito[numero] = resposta
        
        return gabarito

def salvarTxt(nome, outputpath, string):
    with open(f'{outputpath}/{nome}.txt', "w") as file: 
        file.write(string)

def salvarDicionario(nome, outputpath, dict):
    with open(f'{outputpath}/{nome}.json', "w") as file: 
        x = json.dumps(dict)
        file.write(x)

def main():
    inputPath= "gabarito/input"
    outputPath = "gabarito/output"

    extrator = GabaritoExtractor(outputPath=outputPath)
    extrator.setInputPath(inputPath=inputPath)

    listaGabaritos = os.listdir(inputPath)

    texto = extrator.extrair_texto_do_pdf(listaGabaritos[1])

    gabarito = extrator.extrair_gabarito(texto)

    salvarDicionario("gabaritoTeste", outputPath, gabarito)

if __name__ == "__main__":
    main()