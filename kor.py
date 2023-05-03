import re

questao = """
UESTÃO 08 
As Brigadas Internacionais foram unidades de 
combatentes formadas por voluntários de 53 nacionalidades dispostos a lutar em defesa da República espanhola. Estima-se que cerca de 60 mil cidadãos de várias partes do mundo – incluindo 40 brasileiros – tenham se incorporado a essas unidades. Apesar de coordenadas pelos comunistas, as Brigadas contaram com membros socialistas, liberais e de outras correntes político-ideológicas.
SOUZA, I. I. A Guerra Civil Europeia. História Viva, n. 70, 2009 (fragmento).
A Guerra Civil Espanhola expressou as disputas em curso na Europa na década de 1930. A perspectiva política comum que promoveu a mobilização descrita foi o(a)A crítica ao stalinismo.
B combate ao fascismo.
C rejeição ao federalismo.
D apoio ao corporativismo.
E adesão ao anarquismo.
"""


print(questao)

bruto = re.split(r"[A]\s.+?\.\n[B]", questao, maxsplit=1)
aux = re.search(r"[A]\s.+?\.\n[B]", questao)
print(aux.group(0))