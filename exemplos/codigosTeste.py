import PyPDF2 as pd
import json
import re
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTImage, LTTextBoxHorizontal, LTTextBox, LTText, LTFigure

def extrair_texto_do_pdf(inputPath, arquivo):
        """
        input: recebe o nome do arquivo
        output: devolve uma string com todo o texto
        """
        with open(f'{inputPath}/{arquivo}','rb') as file:
            reader = pd.PdfReader(f'{inputPath}/{arquivo}')
            #extrair metadados (no mommento é stub)
            #le e extrai o texto completo
            results = []
            for i in range(0,len(reader.pages)):
                selected_page = reader.pages[i]
                text = selected_page.extract_text()
                results.append(text)
            return ' '.join(results) # converte a lista em um unico documento
        
def desestruturarQuestao(questao):
        #primeira etapa: separar o texto das perguntas
        pattern = r"\s*a\)\s*"
        split_text = re.split(pattern, questao, maxsplit=1)
        texto = split_text[0]
        perguntas = split_text[1]
        perguntas = 'a) ' + perguntas
        #salvar questão em um dicionario
        dicionario = dict()
        dicionario["texto"] = texto
        dicionario["alternativas"] = perguntas
        #metadados da questao
        """dicionario["metadados"] = dict()
        dicionario["metadados"]["vestibular"] = self.vestibular
        dicionario["metadados"]["anoDaProva"] = self.data
        dicionario["metadados"]['numero_alternativas'] = self.quantidade_alternativas"""
        return dicionario
        
def questoesJson(texto, qtdQuestoes):
    questoes = dividirQuestoes(texto=texto, totalQuestoes=qtdQuestoes)
    listaQuestoes = []
    for questao in questoes:
        try:
            json.dumps(questao).encode('utf-32')
        except UnicodeEncodeError:
            pass
        else:
            listaQuestoes.append(desestruturarQuestao(questao))
      
    jsonLista = json.dumps(listaQuestoes)
    
    return jsonLista

def listaNumeros(separador):
    out = []
    for x in separador.split():
        if(x.isdigit()):
            out.append(int(x))
    out.sort()
    return out
          
def dividirQuestoes(texto, totalQuestoes):
    """
    Retorna uma lista de questões, cada questão está em uma string
    """
    listaFrasesComuns = [r"USE OS TEXTOS I e II PARA RESPONDER ÀS QUESTÕES \d+(?:,\s*\d+)*(?:\s*E\s*\d+)?",
                            r"USE O TEXTO A SEGUIR PARA RESPONDER ÀS QUESTÕES \d+(?:,\s*\d+)*(?:\s*E\s*\d+)?",
                            r"Leia o texto a seguir para responder às questões \d+(?:,\s*\d+)*(?:\s*e\s*\d+)?",
                            r"Leia os textos a seguir para responder às questões \d+(?:,\s*\d+)*(?:\s*e\s*\d+)?",
                            r"Texto comum para questões \d+(?:,\s*\d+)*(?:\s*e\s*\d+)?",
                            r"Leia os textos 1 e 2, a seguir, para responder às questões \d+(?:,\s*\d+)*(?:\s*e\s*\d+)?"]    

    listaQuestoes = []
    textoExtra = ""
    addTextoExtra = []
    for i in range(1, totalQuestoes):
        ls = [int(x) for x in str(i+1)]
        li = [int(x) for x in str(i)]

        if (i >= 10):
            pattern = f'(?s)((?<=QUESTÃO {i})|(?<=QUESTÃO {li[0]} {li[1]})).*?((?=QUESTÃO {i+1})|(?=QUESTÃO {ls[0]} {ls[1]}))'
        else:
            pattern = f'(?s)(?<=QUESTÃO {i}).*?(?=QUESTÃO {i+1})'

        questaoBruta = re.search(pattern, texto)
        if (questaoBruta != None):
            #texto da questao
            questao = questaoBruta.group(0)
            for frase in listaFrasesComuns:
                    pattern2 = re.compile(frase)
                    output = re.search(pattern2, questao)
                    if output != None:
                        separador = output.group(0)
                        vetor = questao.split(separador)
                        if(i in addTextoExtra):
                            vetor[0] = textoExtra + vetor[0]
                        listaQuestoes.append(vetor[0])
                        textoExtra = vetor[1]
                        addTextoExtra.extend(listaNumeros(separador))
                        print(addTextoExtra)
            if(i in addTextoExtra):
                questao = textoExtra + questao
                listaQuestoes.append(questao)
            else:
                listaQuestoes.append(questao)
    return listaQuestoes
        
texto = extrair_texto_do_pdf("/home/jonathan/projetos/DataExtraction/data/input", "f12022Q_X.pdf")

x = questoesJson(texto, 72)
with open("data/output/teste.json", "w") as file:
    print(x, file=file)