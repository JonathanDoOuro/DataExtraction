import glob
import json
import codecs
import pickle
import random
import os

# folder_path = 'data/output'  # Replace with the actual folder path

# # Get a list of all JSON files in the folder
# json_files = glob.glob(folder_path + '/*.json')

# # Iterate over each JSON file and open it if it's UTF-8 encoded
# for file_path in json_files:
#     with codecs.open(file_path, 'r', encoding='utf-8') as file:
#         json_data = json.load(file)
#         print(json_data[1]["texto"])

# with open('vetorTextos.pickle', 'rb') as file:
#     data = pickle.load(file)

# for x in data:
#     print(x)
#     break

# arquivos = os.listdir("extrairTextos/topicos")

# print(arquivos)

# for arquivo in arquivos:
#     with open(f"extrairTextos/topicos/{arquivo}", "rb") as file:
#         data = pickle.load(file)

#     with open("vizualize.txt", "w") as arquivo2:
#         print(len(data),": " ,data, file=arquivo2)
vetor_triplas = [("a", "b", "c"), ("d", "e", "f")]

vetor_a, vetor_b, vetor_c = zip(*vetor_triplas)
