import PyPDF2 as pd
import  json
import re
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTImage, LTTextBoxHorizontal, LTTextBox, LTText, LTFigure

class DataExtractor:
    def __init__(self, outputPath):
        self.outputPath = outputPath

    def setInputPath(self, inputPath):
        self.inputPath = inputPath

    def setMetaData(self, vestibular, data, qtd_alternativas):
        self.vestibular = vestibular
        self.data = data
        self.quantidade_alternativas = qtd_alternativas

    def extrair_texto_do_pdf(self, arquivo):
        """
        input: recebe o nome do arquivo
        output: devolve uma string com todo o texto
        """
        with open(f'{self.inputPath}/{arquivo}','rb') as file:
            reader = pd.PdfReader(f'{self.inputPath}/{arquivo}')
            #extrair metadados (no mommento é stub)
            self.setMetaData("Unicamp", "2022", "4")
            #le e extrai o texto completo
            results = []
            for i in range(0,len(reader.pages)):
                selected_page = reader.pages[i]
                text = selected_page.extract_text()
                results.append(text)
            return ' '.join(results) # converte a lista em um unico documento
    
    def verificarImagens(self, nQuestao):
        """Retorna um dicionario que diz se uma questão tem imagem ou não.

        input: path - local do pdf (string); nQuestão - qtd de questões no pdf (int)
        output: dicionario
        """

        #dicionario que informa se uma questão tem imagem
        tem_imagem = dict()
        #paginas do pdf
        pages = extract_pages(self.inputPath)

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

    def dividirQuestoes(self, texto, totalQuestoes):
        """
        Retorna uma lista de questões, cada questão está em uma string
        """
        listaQuestoes = []
        for i in range(1, totalQuestoes):
            ls = [int(x) for x in str(i+1)]
            li = [int(x) for x in str(i)]

            if (i >= 10):
                pattern = f'(?s)((?<=QUESTÃO {i})|(?<=QUESTÃO {li[0]} {li[1]})).*?((?=QUESTÃO {i+1})|(?=QUESTÃO {ls[0]} {ls[1]}))'
            else:
                pattern = f'(?s)(?<=QUESTÃO {i}).*?(?=QUESTÃO {i+1})'

            questaoBruta = re.search(pattern, texto)
            if (questaoBruta != None):
                questao = questaoBruta.group(0)
                listaQuestoes.append(questao)
        return listaQuestoes
    
    def desestruturarQuestao(self, questao):
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
        dicionario["metadados"] = dict()
        dicionario["metadados"]["vestibular"] = self.vestibular
        dicionario["metadados"]["anoDaProva"] = self.data
        dicionario["metadados"]['numero_alternativas'] = self.quantidade_alternativas
        return dicionario
        
    def questoesJson(self, texto, qtdQuestoes):
        questoes = self.dividirQuestoes(texto=texto, totalQuestoes=qtdQuestoes)
        listaQuestoes = []
        for questao in questoes:
            listaQuestoes.append(self.desestruturarQuestao(questao))
        try:    
            jsonLista = json.dumps(listaQuestoes).encode('utf-8').decode('unicode_escape')
        except UnicodeDecodeError:
            pass

        return jsonLista