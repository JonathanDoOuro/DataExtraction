import PyPDF2
import time
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTImage, LTTextBoxHorizontal, LTTextBox, LTText, LTFigure

pages = extract_pages('data/input/2022_PV_impresso_D1_CD1.pdf')

start = 'QUESTÃO 09'
end = 'QUESTÃO 10'

tem_imagem = False
tempo_inicial = time.time()
for i, page in enumerate(pages):
    #transforma a pagina em uma lista
    pagina = list(page)
    #itera sobre os elementos da pagina
    for j in range(len(pagina)):
        #verifica se tem um elemento indicando a questão "start"
        if (isinstance(pagina[j], LTTextBoxHorizontal) and (start in pagina[j].get_text())):
            #verifica se o restante da pagina tem uma imagem antes da questão "end"
            for k in range(j+1, len(pagina)):
                if(isinstance(pagina[k], LTTextBoxHorizontal) and (end in pagina[k].get_text())):
                    tem_imagem = False
                    break
                elif (isinstance(pagina[k], LTFigure)):
                    tem_imagem = True
                    break
tempo_final = time.time()

print(f"{tempo_final - tempo_inicial} segundos")