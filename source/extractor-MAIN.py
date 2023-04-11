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
    for page in pages:
        for element in page:
            allElements.append(element)

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

def destructTexto(texto):
    patterns = [r"\((?:[A-Z][a-z]+(?: [A-Z][a-z]+)*, ){2}(?:[A-Z][a-z]+(?: [A-Z][a-z]+)*, ){1}\d{4}, p\. \d+\.\)",
                r"\s*\([^)]*\)\s*",
                r"(.*?) \[(.*?)\], (.*?), (.*?), Disponível em (.*?), Acessado em (.*?)\.",
                r'\(Fonte: ([^\)]+)\. Acessado em ([^\)]+)\)'
                ]
    #tentar com varios tipos de citação
    for pattern in patterns:
        result = re.split(pattern, texto)
        if(len(result) == 2):
            newText = result[0]
            comando = result[1]
            print(newText)
            break
    


def destructAlternatives(alternativas):
    pass

def destructQuestion(question):
    #primeira etapa: separar o texto das perguntas
    pattern = r"\s*a\)\s*"
    split_text = re.split(pattern, question, maxsplit=1)
    
    texto = split_text[0]
    perguntas = split_text[1]
    perguntas = 'a) ' + perguntas

    #Segunda etapa: desestruturar o texto em texto e pergunta
    destructTexto(texto)

    #Terceira etapa: desestruturar as alterantivas
    destructAlternatives(perguntas)



if __name__ == '__main__':
    path = "./data/input/f12022Q_X.pdf"
    #extrair o texto completo e salvar ele
    #text = extract_text_from_pdf(path)
    #with open(f'data/output/completeText.txt', 'w') as file:
        #print(text, file=file)

    #dicionatio indicando se uma questão possui imagem
    #consultaImagem = verificarImagens(path, 'unicamp')

    #separa as questões e salva em arquivos diferentes
    #splitQuestions(text, consultaImagem)

    #processa cada questão, serando sua estrutura
    with open("data/output/text/question3.txt", "r") as question:
        string = question.read()
        destructQuestion(string)












