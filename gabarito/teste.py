from GabatritoExtractor import GabaritoExtractor

name = "enem2015_PV_reaplicacao_PPL_D1_CD9.pdf"
extrator = GabaritoExtractor("gabarito", "data/input/gabaritos/")

texto = extrator.extrair_texto_do_pdf(name)

dictq = extrator._extrair_gabarito(texto)

with open("gabarito/textoAnalise.txt", "w") as file:
    file.write(texto)

print(texto)
print(dictq)