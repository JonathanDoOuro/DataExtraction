import json

# with open("data/output/temp.json", "r") as file:
#     temp = json.load(file)

# with open("data/output/dicionarioAvalicao2.json", "r") as file:
#     avaliacao = json.load(file)

# dataBio = dict()
# labelsBio = []
# questoesBio = []
# # dataBio["labels"] = []
# # dataBio["questoes"] = []

# questoes: list = avaliacao["questoes"]
# labels: list = avaliacao["labels"]

# for label in labels:
#     if "---" in label:
#         labelsBio.append(label.replace("---", ""))
#         questoesBio.append(questoes[labels.index(label)])

# dataBio["questoes"] = questoesBio
# dataBio["labels"] = labelsBio

# with open("data/output/avaliacaoBio.json", "w") as file:
#     x = json.dumps(dataBio)
#     file.write(x)


with open("data/output/todasQuestoes2.json", "r") as file:
    todas = json.load(file)    

print(len(todas))