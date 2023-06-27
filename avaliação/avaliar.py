questoesTageadas = {"questões": [{"x": "y"}, {"x": "y"}, {"x": "y"}], "labels": [["macaco", "gorila"], ["banana", "maça"]]}


def construirQuestao(questao):
    return questao["x"]

questoes = questoesTageadas["questões"]

for questao in questoes:
    print(questao)

for label in questoesTageadas["labels"]:
    print(label)

