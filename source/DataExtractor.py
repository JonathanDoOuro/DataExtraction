import PyPDF2 as pd
import json
import re
from dbacess import BancoMongo
import fitz
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal, LTFigure


class DataExtractor:
    def __init__(self, outputPath):
        self.outputPath = outputPath

    def setInputPath(self, inputPath):
        self.inputPath = inputPath

    def setBancoDados(self, banco: BancoMongo):
        self.banco = banco

    def setMetaData(self, vestibular, ano, qtd_alternativas, codigo, qtd_questoes):
        self.vestibular = vestibular
        self.ano = ano
        self.quantidade_alternativas = qtd_alternativas
        self.codigo = codigo
        self.quantidade_questoes = qtd_questoes

    def extrair_texto_do_pdf(self, arquivo):
        doc = fitz.open(f'{self.inputPath}/{arquivo}')  # open document
        texto = ''
        for page in doc:  #iterate the document pages
            text = page.get_text(sort=False)  # get plain text (is in UTF-8)
            texto += text
        return texto
    
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
        listaQuestoes = dict()
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
                listaQuestoes[i] = questao

        return listaQuestoes

    def desestruturarAlternativas(self, alternativas):
        if(self.vestibular == "unicamp"):
            escolhas = dict()
            escolhas["A"] = alternativas[0]
            escolhas["B"] = alternativas[1]
            escolhas["C"] = alternativas[2]
            escolhas["D"] = alternativas[3]
        elif(self.vestibular == "enem"):
            escolhas = dict()
            escolhas["A"] = alternativas[0]
            escolhas["B"] = alternativas[1]
            escolhas["C"] = alternativas[2]
            escolhas["D"] = alternativas[3]
            escolhas["E"] = alternativas[4]
        return escolhas
    
    def desestruturarQuestaoEnem(self, questao, index, resposta):
        #retira info desnecessaria
        questao = questao.split("*")[0]
        #separa o texto das alternativas
        padraoQuestao = re.compile(r'(.+)\nA (.+)\nB (.+)\nC (.+)\nD (.+)\nE (.+)', re.DOTALL)
        questaoDividida = re.findall(padraoQuestao, questao)
        if (questaoDividida):
            texto = questaoDividida[0][0]
            perguntas = list(questaoDividida[0][1:])
            #salva as informações em um dicionario
            dicionario = dict()
            dicionario['numero_da_questão'] = index
            dicionario["enunciado"] = texto
            dicionario["alternativas"] = self.desestruturarAlternativas(perguntas)
            dicionario["resposta"] = resposta
            dicionario["topicos"] = []
            #metadados da questão
            dicionario["metadados"] = dict()
            dicionario["metadados"]["vestibular"] = self.vestibular
            dicionario["metadados"]["ano_prova"] = self.ano
            dicionario["metadados"]['quantidade_alternativas'] = self.quantidade_alternativas
            dicionario["metadados"]['codigo_prova'] = self.codigo
        else:
            dicionario = dict()
            dicionario['numero_da_questão'] = index
            dicionario["erro"] = 'padrão de questão não reconhecido'
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

        listaQuestoes = dict()
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
                            #separa a questao em duas parte: 0: questão+alternativas; 1: texto extra
                            vetor = questao.split(separador)
                            questao = vetor[0]
                            textoExtra = vetor[1]
                            addTextoExtra.extend(self.listaNumeros(separador))                            
                if(i in addTextoExtra):
                    questao = textoExtra + questao
                    listaQuestoes[i] = questao
                else:
                    listaQuestoes[i] = questao
        return listaQuestoes
    
    def desestruturarQuestaoUnicamp(self, questao, index, resposta):
        question_regex = re.compile(r'(.+)\na\) (.+)\nb\) (.+)\nc\) (.+)\nd\) (.+)', re.DOTALL)
        questaoDividida = re.findall(question_regex, questao)
        if (questaoDividida):
            dividida = questaoDividida[0]
            texto = dividida[0]
            perguntas = list(dividida[1:])
            #salva as informações em um dicionario
            dicionario = dict()
            dicionario['numero_da_questão'] = index
            dicionario["texto"] = texto
            dicionario["alternativas"] = self.desestruturarAlternativas(perguntas)
            dicionario["resposta"] = resposta
            dicionario["topicos"] = []
            #metadados da questão
            dicionario["metadados"] = dict()
            dicionario["metadados"]["vestibular"] = self.vestibular
            dicionario["metadados"]["ano_prova"] = self.ano
            dicionario["metadados"]['quantidade_alternativas'] = self.quantidade_alternativas
            dicionario["metadados"]['codigo_prova'] = self.codigo
        else:
            dicionario = dict()
            dicionario['numero_da_questão'] = index
            dicionario["erro"] = 'padrão de questão não reconhecido'
        return dicionario

    def questoes(self, texto, salvar: bool, gabarito: dict):
        if(self.vestibular == "unicamp"):
            questoes = self.dividirQuestoesUnicamp(texto=texto)
            listaQuestoes = []
            if (salvar == True):
                for questao in questoes:
                    questaoDestruturadaUnicamp = self.desestruturarQuestaoUnicamp(questao, questoes.index(questao))
                    listaQuestoes.append(questaoDestruturadaUnicamp)
                    self.banco.saveQuestion(questaoDestruturadaUnicamp)
            else:
                for numero, questao in questoes.items():
                    try:
                        questaoDestruturadaUnicamp = self.desestruturarQuestaoUnicamp(questao, numero, gabarito[numero])
                    except KeyError:
                        questaoDestruturadaUnicamp = self.desestruturarQuestaoUnicamp(questao, numero, "anulada")

                    listaQuestoes.append(questaoDestruturadaUnicamp)
            jsonLista = json.dumps(listaQuestoes, ensure_ascii=False)
        elif (self.vestibular == "enem"):
            questoes = self.dividirQuestoesEnem(texto=texto)
            listaQuestoes = []
            if (salvar == True):
                for questao in questoes:
                    questaoDestruturadaEnem = self.desestruturarQuestaoEnem(questao, questoes.index(questao))
                    listaQuestoes.append(questaoDestruturadaEnem)
                    self.banco.saveQuestion(questaoDestruturadaEnem)
            else:
                for numero, questao in questoes.items():
                    try:    
                        questaoDestruturadaEnem = self.desestruturarQuestaoEnem(questao, numero, gabarito[numero])
                    except KeyError:
                        questaoDestruturadaEnem = self.desestruturarQuestaoEnem(questao, numero, "anulada")
                    listaQuestoes.append(questaoDestruturadaEnem)
                    
            jsonLista = json.dumps(listaQuestoes, ensure_ascii=False)
        return jsonLista