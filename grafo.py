import random

class Pilha:
    def __init__(self):
        self.itens = []

    def empilhar(self, item):
        self.itens.append(item)

    def desempilhar(self):
        if not self.esta_vazia():
            return self.itens.pop()
        else:
            return None

    def topo(self):
        if not self.esta_vazia():
            return self.itens[-1]
        else:
            return None

    def esta_vazia(self):
        return len(self.itens) == 0

    def tamanho(self):
        return len(self.itens)
    
    def obter_elementos(self):
        return list(self.itens)
    
class Grafo:
    def __init__(self):
        self.vertices = {}

    def adicionar_vertice(self, vertice):
        self.vertices[vertice.id] = vertice

    def adicionar_aresta(self, vertice1, vertice2):
        vertice1.adicionar_vizinho(vertice2)
        vertice2.adicionar_vizinho(vertice1)

    def obter_vertice(self, vertice_id):
        return self.vertices.get(vertice_id)
    
    def dfs(self, inicio_id, fim_id):
        pilha = Pilha()
        caminho = []
        inicio = self.obter_vertice(inicio_id)
        fim = self.obter_vertice(fim_id)
        inicio.marca = 1
        self.visita(pilha, caminho, fim, inicio)
        caminho_id = []
        for vertice in caminho[0]:
            caminho_id.append(vertice.id)
        return caminho_id

    def visita(self, pilha, caminho, fim, vertice):
        pilha.empilhar(vertice)
        vizinhos_embaralhados = random.sample(vertice.vizinhos, len(vertice.vizinhos))
        for vizinho in vizinhos_embaralhados:
            if vizinho.marca == 0:
                vizinho.marca = 1
                if vizinho.id == fim.id:
                    pilha.empilhar(fim)
                    caminho.append(pilha.obter_elementos())
                    break
                else:
                    self.visita(pilha, caminho, fim, vizinho)
        pilha.desempilhar()
    
    def encontra_caminho(self):
        caminho = set()
        caminho.add(0)
        iter = 0
        i = 0
        while iter <= 150:
            vizinhos = [vizinho.id for vizinho in self.vertices[i].vizinhos]
            vizinho_sorteado = random.choice(vizinhos)
            while vizinho_sorteado in caminho:
                vizinho_sorteado = random.choice(vizinhos)  
            caminho.add(vizinho_sorteado)
            if vizinho_sorteado == 31:
                break
            i = vizinho_sorteado
            iter += 1

        return list(caminho)
        

class Vertice:
    def __init__(self, vertice_id, x, y, marca=0, evento=None, grafo=None):
        self.grafo = grafo
        self.id = vertice_id
        self.marca = 0
        self.evento = evento
        self.descricao = ''
        self.vizinhos = []
        self.x = x
        self.y = y
    
    def adicionar_vizinho(self, vertice):
        self.vizinhos.append(vertice)



