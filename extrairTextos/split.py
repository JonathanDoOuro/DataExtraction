def extrair_palavras(vetor_strings):
    palavras = []

    for string in vetor_strings:
        palavras.extend(string.split())

    return palavras

x = [
    "biomas brasil território deserto ocupação",
    "luz estações jornada trabalho tempo",
    "'pensamento autonomo' impotência acomodação dificuldades",
    "produção agrícola critica agrotóxicos plantações",
    "ideologia idade media revoltas camponesas",
    "sociedade organização indígenas portugueses língua"]

print(extrair_palavras(x))
