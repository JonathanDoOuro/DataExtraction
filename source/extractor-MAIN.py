import PyPDF2 as pd
import re
import time
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTImage, LTTextBoxHorizontal, LTTextBox, LTText, LTFigure

#retorna quais questões tem imagem
def verificarImagens(path, fonte):
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
        for j in range(0, len(elementos)):
            #verifica se tem um elemento indicando a questão "start"
            if (isinstance(elementos[j], LTTextBoxHorizontal) and (start in elementos[j].get_text())):
                #verifica se o restante dos elementos tem uma imagem antes da questão "end"
                for k in range(j+1, len(elementos)):
                    if(isinstance(elementos[k], LTTextBoxHorizontal) and (end in elementos[k].get_text())):
                        tem_imagem[i] = False
                        break
                    elif (isinstance(elementos[k], LTFigure)):
                        tem_imagem[i] = True
                        break
    return tem_imagem

#extrai o texto do pdf como string
def extract_text_from_pdf(pdf_path):
    with open(pdf_path,"rb") as f:
        reader = pd.PdfReader(f)
        results = []
        for i in range(0,len(reader.pages)): # prev read.getNumPages()
            selected_page = reader.pages[i]
            text = selected_page.extract_text()
            results.append(text)
        return ' '.join(results) # convert list to a single doc

#separa cada questão em um arquivo de texto        
def splitQuestions(text, consultaImagem):
    for i in range(1, 72):
        if(consultaImagem[i] != True):
            ls = [int(x) for x in str(i+1)]
            li = [int(x) for x in str(i)]

            if (i >= 10):
                pattern = f'(?s)((?<=QUESTÃO {i})|(?<=QUESTÃO {li[0]} {li[1]})).*?((?=QUESTÃO {i+1})|(?=QUESTÃO {ls[0]} {ls[1]}))'
            else:
                pattern = f'(?s)(?<=QUESTÃO {i}).*?(?=QUESTÃO {i+1})'

            rawQuestion = re.search(pattern, text)
            
            if (rawQuestion != None):
                question = rawQuestion.group(0)
                with open(f'data/output/text/question{i}.txt', 'w') as file:
                    print(question, file=file)

def destructQuestion(question):
    '''
    Estrutura do json:
    {
    'Texto guia': 'some text',
    'pergunta':'De acordo com o texto o autor...',
    'alternativas': {
        'a': 'ele quis dizer x',
        'b': 'ele quis dizer y'
    },
    'resposta': 'a'
    }
    
    '''
    pattern = r'\([^\(\)]+, [^\.]+\. [^:]+: [^\,]+, [0-9]{4}\.  p\. [0-9]+\.\)'
    
    split_text = re.split(pattern, question, maxsplit=1)
    before_pattern = split_text[0]

    print(before_pattern)
    print(split_text[1])

if __name__ == '__main__':
    path = "./data/input/f12022Q_X.pdf"
    #extrair o texto completo e salvar ele
    text = extract_text_from_pdf(path)
    with open(f'data/output/completeText.txt', 'w') as file:
        print(text, file=file)

    consultaImagem = verificarImagens(path, 'unicamp')
    #separa as questões e salva em arquivos diferentes
    splitQuestions(text, consultaImagem)



















