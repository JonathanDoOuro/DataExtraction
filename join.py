import PyPDF2
import time
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTImage, LTTextBoxHorizontal, LTTextBox, LTText, LTFigure



#fonte de dados
fontes = ['enem', 'unicamp']
fonte = fontes[0]
path = 'data/input/2022_PV_impresso_D1_CD1.pdf'

if fonte == 'enem':
    nQuestao = 95
elif fonte == 'unicamp':
    nQuestao = 72

#dicionario com info de cada questão
tem_imagem = dict()

pages = extract_pages(path)


#transforma o pdf em uma lista de elementos
allElements = []
tempo_inicial = time.time()
print("teste")
for page in pages:
    for element in page:
        allElements.append(element)
tempo_final = time.time()
print(f"tempo: {tempo_final - tempo_inicial} segundos")

elementos = allElements

for i in range(1, nQuestao):
    start = f'QUESTÃO {i}'
    end = f'QUESTÃO {i+1}'
    for j in range(len(elementos)):
        #verifica se tem um elemento indicando a questão "start"
        if (isinstance(elementos[j], LTTextBoxHorizontal) and (start in elementos[j].get_text())):
            #verifica se o restante dos elementos tem uma imagem antes da questão "end"
            for k in range(j+1, len(elementos)):
                if(isinstance(elementos[k], LTTextBoxHorizontal) and (end in elementos[k].get_text())):
                    tem_imagem[start] = False
                    break
                elif (isinstance(elementos[k], LTFigure)):
                    tem_imagem[start] = True
                    break

naotem = 0
for k, v in tem_imagem.items():
    if v == False:
        naotem +=1

print(naotem)
