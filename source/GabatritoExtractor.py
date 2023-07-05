import json
import re
import fitz
import os

class GabaritoExtractor:
    def __init__(self, outputPath, inputPath):
        self.outputPath = outputPath
        self.inputPath = inputPath

    def extrair_texto_do_pdf(self, arquivo):
        doc = fitz.open(f'{self.inputPath}/{arquivo}')  # open document
        texto = ''
        for page in doc:  #iterate the document pages
            text = page.get_text(sort=False)  # get plain text (is in UTF-8)
            texto += text
        return texto
    
    def _extrair_gabarito(self, texto):
        padrao = r'(\d+)\n([A-Z])\n'
        matches = re.findall(padrao, texto)
        
        gabarito = {}
        for match in matches:
            numero = int(match[0])
            resposta = match[1]
            gabarito[numero] = resposta
        
        return gabarito
    
    def gabarito(self, arquivo):
        texto = self.extrair_texto_do_pdf(arquivo)
        gabarito = self._extrair_gabarito(texto)
        self.salvarDicionario(arquivo, gabarito)
        return gabarito

    def salvarDicionario(self, nome, dict):
        with open(f'{self.outputPath}/{nome}.json', "w") as file: 
            x = json.dumps(dict)
            file.write(x)

# def main():
#     inputPath= "gabarito/input"
#     outputPath = "gabarito/output"

#     extrator = GabaritoExtractor(outputPath=outputPath)
#     extrator.setInputPath(inputPath=inputPath)

#     listaGabaritos = os.listdir(inputPath)

#     texto = extrator.extrair_texto_do_pdf(listaGabaritos[1])

#     gabarito = extrator.extrair_gabarito(texto)

#     extrator.salvarDicionario("gabaritoTeste", outputPath, gabarito)

# if __name__ == "__main__":
#     main()