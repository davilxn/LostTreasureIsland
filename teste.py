from utils import inicializa_criaturas, inicializa_grafo
from grafo import Grafo
grafo = Grafo()
inicializa_grafo(grafo, "pontos.json")
for vertice in grafo.vertices:
    print(grafo.vertices[vertice].objeto)