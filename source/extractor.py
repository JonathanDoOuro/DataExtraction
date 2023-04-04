import PyPDF2 as pd
import re

### Function to Extract Text From PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path,"rb") as f:
        reader = pd.PdfReader(f)
        results = []
        for i in range(0,len(reader.pages)): # prev read.getNumPages()
            selected_page = reader.pages[i]
            text = selected_page.extract_text()
            results.append(text)
        return ' '.join(results) # convert list to a single doc
        

def splitQuestions(text):
    for i in range(1, 72):
        ls = [int(x) for x in str(i+1)]
        li = [int(x) for x in str(i)]

        if (i >= 10):
            pattern = f'(?s)((?<=QUESTÃO {i})|(?<=QUESTÃO {li[0]} {li[1]})).*?((?=QUESTÃO {i+1})|(?=QUESTÃO {ls[0]} {ls[1]}))'
        else:
            pattern = f'(?s)(?<=QUESTÃO {i}).*?(?=QUESTÃO {i+1})'

        rawQuestion = re.search(pattern, text)
        
        if (rawQuestion != None):
            question = rawQuestion.group(0)
            with open(f'data/output/question{i}.txt', 'w') as file:
                print(question, file=file)

def destructQuestion(question):
    '''
    Estrutura do json:
    {
    'Texto guia': 'some text',
    'fonte': '(comphania das letras.. 2019)',
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
    pass

if __name__ == '__main__':
    path = "./data/input/f12022Q_X.pdf"
    #extrair o texto completo e salvar ele
    """text = extract_text_from_pdf(path)
    with open(f'data/output/completeText.txt', 'w') as file:
        print(text, file=file)

    #separa as questões e salva em arquivos diferentes
    splitQuestions(text)"""

    with open('data/output/question10.txt') as arquivo:
        string = arquivo.read()

    destructQuestion(string)


















