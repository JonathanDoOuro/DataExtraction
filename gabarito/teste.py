import os
import json

path = "gabarito/output/"

arquivos = os.listdir(path)

quantidadeQuestoes = 0
a = 0
b = 0
c = 0
d = 0
e = 0

for arquivo in arquivos:
    with open(path + arquivo) as file:
        gabarito: dict = json.load(file)
    for key in gabarito.values():
        quantidadeQuestoes +=1
        if(key == "A"):
            a +=1
        elif(key == "B"):
            b +=1
        elif(key == "C"):
            c +=1
        elif(key == "D"):
            d +=1
        elif(key == "E"):
            e +=1

print("total de questões: ", quantidadeQuestoes)
print()
print("quantidade de A: ", a)
print("quantidade de B: ", b)
print("quantidade de C: ", c)
print("quantidade de D: ", d)
print("quantidade de E: ", e)
print()
print("proporções: ")
print("A: ", a/quantidadeQuestoes * 100)
print("B: ", b/quantidadeQuestoes * 100)
print("C: ", c/quantidadeQuestoes * 100)
print("D: ", d/quantidadeQuestoes * 100)
print("E: ", e/quantidadeQuestoes * 100)

