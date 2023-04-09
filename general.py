import PyPDF2
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTImage, LTTextBoxHorizontal, LTTextBox, LTText, LTFigure


#pdf = PyPDF2.PdfReader(open('data/input/f12022Q_X.pdf', 'rb'))

pages = extract_pages('data/input/f12022Q_X.pdf')

start = 'QUESTÃO 10'
end = 'QUESTÃO 11'

tem_imagem = False

print(type(pages))
for i, page in enumerate(pages):
    if(i == 4):
       
            #transforma a pagina em uma lista
            pagina = list(page)
            #itera sobre os elementos da pagina
            for j in range(len(pagina)):
                #verifica se tem um elemento indicando a questão "start"
                if (isinstance(pagina[j], LTTextBoxHorizontal) and (start in pagina[j].get_text())):
                    print(pagina[j].get_text())
                    #verifica se o restante tem uma imagem
                    for k in range(j+1, len(pagina)):
                        if(isinstance(pagina[k], LTTextBoxHorizontal) and (end in pagina[k].get_text())):
                            tem_imagem = False
                            break
                        elif (isinstance(pagina[k], LTImage) or isinstance(pagina[k], LTFigure)):
                            tem_imagem = True
                            break

    elif(i > 5):
        break

print(tem_imagem)