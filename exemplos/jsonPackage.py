import json


with open("data/output/enem2012_PV_reaplicacao_PPL_D2_CD6.pdf.json", "r") as file:
    docs = json.load(file)

print(len(docs))
 
iteravelStrings = list()

for i in range(len(docs)):
    iteravelStrings.append(docs[i])
    print(i)
    print(docs[i]["texto"])