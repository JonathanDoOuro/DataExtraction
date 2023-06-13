from bertopic import BERTopic
import torch

model_path = "exemplos/supervised_model"
model = torch.load(model_path, map_location=torch.device('cpu'))

texto = """A cultura do Brasil é uma síntese da influência dos vários povos e etnias que formaram o povo brasileiro. Não existe uma cultura brasileira perfeitamente homogênea, e sim um mosaico de diferentes vertentes culturais que formam, juntas, a cultura do Brasil.
"""

topic, _ = model.transform(texto)

print(topic)