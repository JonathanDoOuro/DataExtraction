import json

lista = []
d1 = {"Texto": "\n \nG\u00caNESIS (INTRO) \nDeus fez o mar, as \u00e1rvore, as crian\u00e7a, o amor \nO homem me deu a favela, o crack, a trairagem As arma, as bebida, as puta Eu? Eu tenho uma B\u00edblia velha, uma pistola autom\u00e1tica Um sentimento de revolta \nEu t\u00f4 tentando sobreviver no inferno \n(Racionais Mc\u2019s, Sobrevivendo no inferno . S\u00e3o Paulo: Companhia das Letras, \n2018, p. 45.) \n \n\u201cG\u00eanesis\u201d \u00e9 a segunda can\u00e7\u00e3o do \u00e1lbum Sobrevivendo no \nInferno . \u00c9 antecedida pela invoca\u00e7\u00e3o de uma outra can\u00e7\u00e3o, \nintitulada \u201cJorge da Capad\u00f3cia\u201d",
      "alternativas": "A) fdsfdsfdsfsdfsd"}
d2 = {"Texto": "textoooooooooooo",
      "alternativas": "A) fdsfdsfdsfsdfsd"}
d3 = {"Texto": "páiś",
      "alternativas": "A) alternância"}

lista.append(d1)
lista.append(d2)
lista.append(d3)

with open("data/output/jsonLiteral.json", "w") as file:
    j = json.dumps(lista, ensure_ascii=False)
    file.write(j)