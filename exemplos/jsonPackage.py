import re

def filtrar_texto(texto):
    # Expressão regular para encontrar a expressão matemática
    pattern = r'\\{0,2}\n*\{\\displaystyle.*?\n*\}'

    # Substitui a expressão matemática encontrada por uma string vazia
    texto_filtrado = re.sub(pattern, '', texto)

    # Remove espaços e quebras de linha desnecessários
    texto_filtrado = re.sub(r'\s+', ' ', texto_filtrado).strip()

    return texto_filtrado.replace("\n", "")

texto = """Sejam V e W espaços vetoriais sobre um corpo K , sendo V de dimensão finita, e seja T uma transformação linear de V em W . Então dim ⁡ ( V ) = dim ⁡ ( ker ⁡ ( T ) ) + dim ⁡ ( Im ⁡ ( T ) ) . (T)).} Vai ser visto como se pode demonstrar esse facto. Seja n = dim ⁡ ( ker ⁡ ( T ) ) e seja { v 1 , v 2 ,,v_{2},} … , v n }\\}} uma base de ker ⁡ ( T ) . Como ker ⁡ ( T ) é um subespaço de V , pode-se completar essa base até obtermos uma base de V . Sejam então w 1 , w 2 ,,w_{2},} … , w m} ∈ V tais que { v 1 , v 2 ,,v_{2},} … , v n , w 1 , w 2 ,,w_{1},w_{2},} … , w m }\\}} seja uma base de V ; em particular, dim ⁡ ( V ) = n + m . Vai-se provar que { T ( w 1 ) ,),} … , T ( w m ) })\\}} é uma base de Im ( T ) , de onde resultará que dim ⁡ ( Im ⁡ ( T ) ) = m = ( m + n ) − n = dim ⁡ ( V ) − dim ⁡ ( ker ⁡ ( T ) ) . (T))=m=(m+n)-n=\\dim(V)-\\dim(\\ker(T)).} Se w ∈ Im ( T ) , então w = T ( v ) para algum v ∈ V e v pode ser escrito sob a forma v = α 1 v 1 + ⋯ α n v n + β 1 w 1 + ⋯ + β m w m ,v_{1}+\\cdots \\alpha _{n}v_{n}+\\beta _{1}w_{1}+\\cdots +\\beta _{m}w_{m},} pelo que T ( v ) = β 1 T ( w 1 ) + ⋯ + β m T ( w m ) ,T(w_{1})+\\cdots +\\beta _{m}T(w_{m}),} visto que v 1 , v 2 , … , v n,v_{2},\\ldots ,v_{n}} ∈ ker ⁡ ( T ) . Isto prova que { T ( w 1 ) , … , T ( w m ) }),\\ldots ,T(w_{m})\\}} gera Im ⁡ ( T ) . (T).} Por outro lado, os vetores T ( w 1 ) , T ( w 2 ) , … , T ( w m )),T(w_{2}),\\ldots ,T(w_{m})} são linearmente independentes, pois se α 1 , α 2 , … , α m,\\alpha _{2},\\ldots ,\\alpha _{m}} ∈ K forem tais que α 1 T ( w 1 ) + α 2 T ( w 2 ) + ⋯ + α m T ( w m ) = 0 ,T(w_{1})+\\alpha _{2}T(w_{2})+\\cdots +\\alpha _{m}T(w_{m})=0,} então T ( α 1 w 1 + α 2 w 2 + ⋯ + α m w m ) = 0 ⇒ α 1 w 1 + α 2 w 2 + ⋯ + α m w m ∈ ker ⁡ ( T ) ,\\alpha _{1}w_{1}+\\alpha _{2}w_{2}+\\cdots +\\alpha _{m}w_{m}{\\bigr )}=0\\Rightarrow \\alpha _{1}w_{1}+\\alpha _{2}w_{2}+\\cdots +\\alpha _{m}w_{m}\\in \\ker(T),} de onde resulta que α 1 w 1 + α 2 w 2 + … + α m w mw_{1}+\\alpha _{2}w_{2}+\\ldots +\\alpha _{m}w_{m}} é uma combinação linear dos vetores v 1 , v 2 , … , v n ,,v_{2},\\ldots ,v_{n},} o que é só é possível se α 1 = α 2 = … = α m = 0 ,=\\alpha _{2}=\\ldots =\\alpha _{m}=0,} pois o conjunto { v 1 , v 2 , … , v n , w 1 , w 2 , … , w m },v_{2},\\ldots ,v_{n},w_{1},w_{2},\\ldots ,w_{m}\\}} é uma base e, portanto, linearmente independente."""

def possui_muitos_simbolos(texto, limite_proporcao=0.1):
    # Remove espaços em branco para contar apenas caracteres
    texto = texto.replace(" ", "")

    # Conta a quantidade total de caracteres
    total_caracteres = len(texto)

    # Encontra os caracteres não alfabéticos
    caracteres_nao_alfabeticos = re.findall(r'[^a-zA-Z]', texto)

    # Conta a quantidade de caracteres não alfabéticos
    total_nao_alfabeticos = len(caracteres_nao_alfabeticos)

    # Calcula a proporção de caracteres não alfabéticos
    proporcao_nao_alfabeticos = total_nao_alfabeticos / total_caracteres

    # Verifica se a proporção ultrapassa o limite estabelecido
    if proporcao_nao_alfabeticos > limite_proporcao:
        return True
    else:
        return False

def contar_palavras(texto):
    palavras = re.findall(r'\b[a-zA-Z]{5,}\b', texto)  # Encontra palavras formadas por letras com mais de 4 letras
    return len(palavras)

# Exemplo de uso

texto_filtrado = filtrar_texto(texto)
print(texto_filtrado)

numero_palavras = contar_palavras(texto_filtrado)
print(numero_palavras)

print(possui_muitos_simbolos(texto))