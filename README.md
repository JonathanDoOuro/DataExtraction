# DataExtraction

## Resumo

Provas objetivas e dissertativas são comuns no ensino brasileiro, todavia, vem sendo questionada a eficácia desses métodos no aprendizado dos alunos, bem como levantadas possíveis soluções para melhorar o aproveitamento dos estudos. Uma solução proposta é a utilização de quizzes em sala de aula, de modo que o ensino se torne mais iterativo e ativo.

Neste contexto, surge o projeto chamado *Quizzing*, que é uma plataforma onde professores e alunos podem gerar quizzes através de prompts para uma inteligência artificial que gera quizzes baseados nas instruções do usuário.

Essa inteligência artificial é um conjunto de modelos generativos de textos, os quais precisam ser treinados com questões existentes de alta qualidade para então gerar quizzes corretos, sendo esse ponto o foco deste projeto. Nosso objetivo é produzir um *dataset* de questões de vestibulares que será utilizado para refinar o modelo gerador de texto, de modo que ele seja capaz de gerar quizzes inéditos.

Para obter o *dataset*, utilizamos bibliotecas de extração de texto como *pyMupdf* e uma técnica de processamento de linguagem natural conhecida como modelagem de tópicos. Primeiro, extraímos o texto bruto das provas de vestibular; em seguida, realizamos um processamento para separar e estruturar as questões em um formato adequado para o modelo gerador de questões consumir.

No treinamento dos modelos generativos, é preciso além das questões, um conteúdo fonte sobre a questão. Tendo isso em mente, construímos um modelo de extração de tópicos e utilizamos ele para identificar o tópico de cada questão extraída, visando fornecer metadados relevantes para o modelo gerador de questões procurar textos relacionados com a questão no momento do treinamento.

Para obter o modelo de tópicos, analisamos os resultados de duas técnicas de modelagem de tópicos e busca semântica em um conjunto de dados que contém questões de vestibulares rotuladas com tópicos esperados. O modelo escolhido foi o que apresenta a maior pontuação de similaridade entre o tópico previsto e o tópico esperado, onde a pontuação é a média de similaridade do cosseno entre o *embedding* do resultado predito e o rótulo.

A contribuição principal desse estudo é um conjunto de dados de questões e um modelo de tópicos, ambos fundamentais no treinamento e no ambiente de produção de um modelo gerador de questões.
