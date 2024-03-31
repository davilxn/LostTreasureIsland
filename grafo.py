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
        """
        Inicializa uma instância de Grafo com um dicionário vazio de vértices.
        """
        self.vertices = {}

    def adicionar_vertice(self, vertice):
        """
        Adiciona um vértice ao grafo.

        Args:
            vertice: O vértice a ser adicionado ao grafo.
        """
        self.vertices[vertice.id] = vertice

    def adicionar_aresta(self, vertice1, vertice2):
        """
        Adiciona uma aresta (conexão) entre dois vértices.

        Args:
            vertice1: O primeiro vértice.
            vertice2: O segundo vértice.
        """
        vertice1.adicionar_vizinho(vertice2)
        vertice2.adicionar_vizinho(vertice1)

    def obter_vertice(self, vertice_id):
        """
        Retorna um vértice do grafo, se existir.

        Args:
            vertice_id: O identificador do vértice.

        Returns:
            O vértice correspondente ao identificador, ou None se não existir.
        """
        return self.vertices.get(vertice_id)
    
    def dfs(self, inicio_id, fim_id):
        """
        Executa uma busca em profundidade (DFS) no grafo, de modo a encontrar um caminho qualquer entre o vértice de início e o de fim.

        Args:
            inicio_id: O identificador do vértice de início.
            fim_id: O identificador do vértice de destino.

        Returns:
            Uma lista contendo os vértices no caminho encontrado do vértice de início ao vértice de destino, se existir.
        """
        pilha = Pilha()
        caminho = []
        inicio = self.obter_vertice(inicio_id)
        fim = self.obter_vertice(fim_id)
        inicio.marca = 1
        self.visita(pilha, caminho, fim, inicio)
        caminho_id = []
        for vertice in caminho[0]:
            caminho_id.append(vertice.id)
        for _, vertice in self.vertices.items():
            vertice.marca = 0
        return caminho_id

    def visita(self, pilha, caminho, fim, vertice):
        """
        Função auxiliar para realizar a busca em profundidade (DFS) recursivamente.

        Args:
            pilha: A pilha usada na DFS.
            caminho: Lista para armazenar o caminho encontrado.
            fim: O vértice de destino.
            vertice: O vértice atual sendo visitado.
        """
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

class Vertice:
    def __init__(self, vertice_id, x, y, marca=0, evento=None, grafo=None):
        """
        Inicializa um vértice com um identificador, coordenadas (x, y) e outros atributos opcionais.

        Args:
            vertice_id: O identificador único do vértice.
            x: A coordenada x do vértice na tela do Pygame.
            y: A coordenada y do vértice na tela do Pygame.
            marca: O estado de marcação do vértice (padrão é 0).
            evento: Um evento associado ao vértice (inicialemente opcional).
            grafo: O grafo ao qual o vértice pertence.
        """
        self.grafo = grafo
        self.id = vertice_id
        self.marca = marca
        self.evento = [evento]
        self.objeto = []
        self.descricao = ''
        self.vizinhos = []
        self.x = x
        self.y = y
    
    def adicionar_vizinho(self, vertice):
        """
        Adiciona um vértice vizinho a este vértice.

        Args:
            vertice: O vértice vizinho a ser adicionado.
        """
        self.vizinhos.append(vertice)
    



