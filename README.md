# DataExtraction

## Resumo

A contribuição principal desse trabalho é um conjunto de dados de questões e um modelo de tópicos, ambos fundamentais no treinamento e no ambiente de produção de um modelo gerador de questões.

Esses dados alimentam modelos generativos de textos utilizados no projeto *Quizzing*, uma plataforma onde professores e alunos podem gerar quizzes através de prompts para uma inteligência artificial que gera quizzes baseados nas instruções do usuário. O projeto *Quizzing* é idealizado por Julio Cesar dos Reis, professor Associado do instituto de computação da UNICAMP. 

## Dataset de questões

Para obter o *dataset*, utilizamos bibliotecas de extração de texto como *pyMupdf* e uma técnica de processamento de linguagem natural conhecida como modelagem de tópicos. Primeiro, extraímos o texto bruto das provas de vestibular; em seguida, realizamos um processamento para separar e estruturar as questões em um formato adequado para o modelo gerador de questões consumir.

Para ter acesso as questões acesse `data/ouptput/Finais`

```
{
    "numero_da_questão": 91,
    "enunciado": "  Disponível em: www.seton.com. Acesso em: 28 fev. 2012. Placas como a da gravura são usadas para orientar os usuários de um espaço urbano. Essa placa, especificamente, tem a função de avisar que somente",
    "alternativas": {
        "A": "as despesas feitas com estacionamento são deduzidas.",
        "B": "os donos de carro entram no estacionamento do parque.",
        "C": "o proprietário autoriza a validação do estacionamento.",
        "D": "os rebocadores precisam de permissão para entrar no local.",
        "E": "os veículos autorizados podem estacionar naquela área. "
    },
    "resposta": "E",
    "topicos": [
        "urbanismo", "urbanas", "urbanos", "urbanizacao", "urbano", "cidades"
    ],
    "metadados": {
        "vestibular": "enem",
        "ano_prova": 2013,
        "quantidade_alternativas": 5,
        "codigo_prova": "_PV_reaplicacao_PPL_D2_CD6"
    }
}
 ```

## Modelagem de tópicos

Durante o treinamento dos modelos generativos, além das questões, é necessário um conteúdo fonte sobre cada questão. Para isso, desenvolvemos um modelo de extração de tópicos que identifica o tema de cada questão, fornecendo metadados relevantes para o modelo gerador de questões buscar textos relacionados no momento do treinamento. 

Para obter o modelo de tópicos, foram analisados os resultados de duas técnicas de modelagem e busca semântica (*Bertopic* e *Top2Vec*) em um conjunto de dados de questões de vestibulares com rótulos de tópicos. O modelo escolhido foi o *Top2Vec* pois ele apresentou a maior pontuação de similaridade entre o tópico previsto e o tópico esperado, usando como medida a média de similaridade do cosseno entre o embedding do resultado predito e o rótulo.
