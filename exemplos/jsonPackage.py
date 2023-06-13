import re

import re

def filtrar_texto(texto):
    # Expressão regular para encontrar a expressão matemática
    pattern = re.compile(r'\\{0,2}\n{0,}\{\\displaystyle.*?\n{0,}\}')

    # Substitui a expressão matemática encontrada por uma string vazia
    texto_filtrado = re.sub(pattern, '', texto)

    return texto_filtrado

texto = """Podemos sentir o efeito da entropia ao esticarmos um elástico, 
por exemplo. A borracha é formada por longas cadeias de polímeros com 
ligações cruzadas – que lembram ziguezagues. Quando o elástico está 
relaxado essas cadeias estão parcialmente enroladas e ordenadas aleatoriamente, 
devido a esse alto grau de desordem das moléculas o estado possui um valor de 
entropia também alto. Ao esticarmos o elástico desenrolamos essas moléculas e 
as alinhamos, como o alinhamento diminui a desordem isso significa dizer que a
derivada \n\n\n\nd\nS\n\n/\n\nd\nx\n\n\n{\\displaystyle dS/dx}\n\n se torna 
negativa e consequentemente a força exercida pelos polímeros se torna positiva. 
Essa força se deve a tendência das moléculas de voltar ao estado menos ordenado 
(com uma maior entropia).\n"""

texto_filtrado = filtrar_texto(texto)
print(texto_filtrado)