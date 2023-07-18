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

        for page in doc:
            # Dividir a página verticalmente
            width = page.rect.width
            height = page.rect.height
            mid_x = width / 2

            # Extrair o texto da metade esquerda
            left_rect = fitz.Rect(page.rect.tl, (mid_x, page.rect.br.y))
            left_text = page.get_textbox(left_rect)

            # Extrair o texto da metade direita
            right_rect = fitz.Rect((mid_x, page.rect.tl.y), page.rect.br)
            right_text = page.get_textbox(right_rect)

            # Adicionar o texto extraído ao resultado
            texto += left_text + right_text

        return texto
    
    def _extrair_gabarito(self, texto):
        #padrao = r'(\d+)\n\s*([A-Z])\n'
        padrao = r'(\d+)?\s*\n\s*([A-Z])\s*\n'
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
