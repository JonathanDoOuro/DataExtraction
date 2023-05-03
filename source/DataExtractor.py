import PyPDF2 as pd
import  json
import re
from pdfminer.high_level import extract_pages
from pdfminer.high_level import extract_text
from pdfminer.layout import LTImage, LTTextBoxHorizontal, LTTextBox, LTText, LTFigure

class DataExtractor:
    def __init__(self, outputPath):
        self.outputPath = outputPath

    def setInputPath(self, inputPath):
        self.inputPath = inputPath

    def setMetaData(self, vestibular, ano, qtd_alternativas, codigo, qtd_questoes):
        self.vestibular = vestibular
        self.ano = ano
        self.quantidade_alternativas = qtd_alternativas
        self.codigo = codigo
        self.quantidade_questoes = qtd_questoes

    def extrair_texto_do_pdf(self, arquivo):
        """
        input: recebe o nome do arquivo
        output: devolve uma string com todo o texto
        """
        #text = extract_text(f'{self.inputPath}/{arquivo}')
        with open(f'{self.inputPath}/{arquivo}','rb') as file:
            reader = pd.PdfReader(f'{self.inputPath}/{arquivo}')
            #le e extrai o texto completo
            results = []
            for i in range(0,len(reader.pages)):
                selected_page = reader.pages[i]
                text = selected_page.extract_text()
                results.append(text)
            return ' '.join(results) # converte a lista em um unico documento
        #print(text)
        #return text
    
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

    def listaNumeros(self, separador):
        out = []
        for x in separador.split():
            if(x.isdigit()):
                out.append(int(x))
        out.sort()
        return out

    def dividirQuestoesEnem(self, texto):
        listaQuestoes = []
        if (self.quantidade_questoes > 90):
            inicio = 91
        else:
            inicio = 1
        for i in range(inicio, self.quantidade_questoes):
            if (i < 10):
                pattern = f'(?s)((?<=Questão 0{i})|(?<=QUESTÃO 0{i}))(.*?)((?=Questão 0{i+1})|(?=QUESTÃO 0{i+1}))'
            elif (i > 10):
                pattern = f'(?s)((?<=Questão {i})|(?<=QUESTÃO {i}))(.*?)((?=Questão {i+1})|(?=QUESTÃO {i+1}))'
            questaoBruta = re.search(pattern, texto)
            if (questaoBruta != None):
                questao = questaoBruta.group(0)
                listaQuestoes.append(questao)

        return listaQuestoes

    def desestruturarQuestaoEnem(self, questao, index):
        bruto = re.split(r"\n[A-Z]\s", questao, maxsplit=1)
        if(len(bruto) >= 2):
            main_text = bruto[0]
            choices = bruto[1] 
            dicionario = dict()
            dicionario['numero_da_questão'] = index
            dicionario["texto"] = main_text
            dicionario["alternativas"] = choices
        else:
            dicionario = dict()
            dicionario['numero_da_questão'] = index
        #dicionario["alternativas"] = alternatives
        return dicionario

    def dividirQuestoesUnicamp(self, texto):
        """
        Retorna uma lista de questões, cada questão está em uma string
        """
        listaFrasesComuns = [r"USE OS TEXTOS I e II PARA RESPONDER ÀS QUESTÕES \d+(?:,\s*\d+)*(?:\s*E\s*\d+)?",
                            r"USE O TEXTO A SEGUIR PARA RESPONDER ÀS QUESTÕES \d+(?:,\s*\d+)*(?:\s*E\s*\d+)?",
                            r"Texto para as questões \d+(?:,\s*\d+)*(?:\s*e\s*\d+)?",
                            r"TEXTO PARA AS QUESTÕES \d+(?:,\s*\d+)*(?:\s*E\s*\d+)?",
                            r"Para as questões \d+(?:,\s*\d+)*(?:\s*e\s*\d+)?",
                            r"Leia o texto a seguir para responder às questões \d+(?:,\s*\d+)*(?:\s*e\s*\d+)?",
                            r"Leia os textos a seguir para responder às questões \d+(?:,\s*\d+)*(?:\s*e\s*\d+)?",
                            r"Texto comum para questões \d+(?:,\s*\d+)*(?:\s*e\s*\d+)?",
                            r"Leia os textos 1 e 2, a seguir, para responder às questões \d+(?:,\s*\d+)*(?:\s*e\s*\d+)?"]    

        listaQuestoes = []
        textoExtra = ""
        addTextoExtra = []
        for i in range(1, self.quantidade_questoes):
            ls = [int(x) for x in str(i+1)]
            li = [int(x) for x in str(i)]

            if (i >= 10):
                pattern = f'(?s)((?<=QUESTÃO {i})|(?<=QUESTÃO {li[0]} {li[1]})).*?((?=QUESTÃO {i+1})|(?=QUESTÃO {ls[0]} {ls[1]}))'
            else:
                pattern = f'(?s)((?<=QUESTÃO {i})|(?<=QUESTÃO  {i})).*?((?=QUESTÃO {i+1})|(?=QUESTÃO  {i+1}))'

            questaoBruta = re.search(pattern, texto)
            if (questaoBruta != None):
                #texto da questao
                questao = questaoBruta.group(0)
                for frase in listaFrasesComuns:
                        pattern2 = re.compile(frase)
                        output = re.search(pattern2, questao)
                        #se achou um "leia o texto a seguir"
                        if output != None:
                            #string do tipo "texto comum bla bla"
                            separador = output.group(0)
                            if (i == 1):    
                                print(frase)
                                print(separador)
                            #separa a questao em duas parte: 0: questão+alternativas; 1: texto extra
                            vetor = questao.split(separador)
                            #se a questão necessita de texto extra
                            """if(i in addTextoExtra):
                                vetor[0] = textoExtra + vetor[0]
                                addTextoExtra.remove(i)"""
                            #listaQuestoes.append(vetor[0])
                            questao = vetor[0]
                            textoExtra = vetor[1]
                            addTextoExtra.extend(self.listaNumeros(separador))                            
                if(i in addTextoExtra):
                    questao = textoExtra + questao
                    listaQuestoes.append(questao)
                else:
                    listaQuestoes.append(questao)
        return listaQuestoes
    
    def desestruturarQuestaoUnicamp(self, questao):
        #primeira etapa: separar o texto das perguntas
        pattern = r"\s*a\)\s*"
        split_text = re.split(pattern, questao, maxsplit=1)
        texto = split_text[0]
        if(len(split_text) > 1):
            perguntas = split_text[1]
            perguntas = 'a) ' + perguntas
            #salvar questão em um dicionario
            dicionario = dict()
            dicionario["texto"] = texto
            dicionario["alternativas"] = perguntas
            #metadados da questao
            dicionario["metadados"] = dict()
            dicionario["metadados"]["vestibular"] = self.vestibular
            dicionario["metadados"]["ano_prova"] = self.ano
            dicionario["metadados"]['quantidade_alternativas'] = self.quantidade_alternativas
            dicionario["metadados"]['codigo_prova'] = self.codigo
            return dicionario
        else:
            return dict()

    def questoesJson(self, texto):
        if(self.vestibular == "unicamp"):
            questoes = self.dividirQuestoesUnicamp(texto=texto)
            listaQuestoes = []
            for questao in questoes:
                listaQuestoes.append(self.desestruturarQuestaoUnicamp(questao))
            jsonLista = json.dumps(listaQuestoes, ensure_ascii=False)#.encode('utf-8').decode('unicode_escape')
        elif (self.vestibular == "enem"):
            questoes = self.dividirQuestoesEnem(texto=texto)
            listaQuestoes = []
            for questao in questoes:
                listaQuestoes.append(self.desestruturarQuestaoEnem(questao, questoes.index(questao)))
            jsonLista = json.dumps(listaQuestoes, ensure_ascii=False)
        return jsonLista