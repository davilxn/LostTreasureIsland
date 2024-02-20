from animacoes import carregar_frames, Animacao
from random import randint, sample, choice
import networkx as nx

class PlantaMedicial:
    def __init__(self, nome, descricao, vertice, pontos_vida=25):
        self.nome = nome
        self.descricao = descricao
        self.vertice = vertice
        self.pontos_vida = pontos_vida
    
class Arma:
    def __init__(self, nome, descricao, vertice, pontos_ataque, usos_maximos=3):
        self.nome = nome
        self.descricao = descricao
        self.pontos_ataque = pontos_ataque
        self.usos_maximos = usos_maximos
        self.usos_restantes = usos_maximos
        self.vertice = vertice
        self.util = True

    def uso(self):
        self.usos_restantes -= 1
    
    def verificar_quebrada(self):
        if self.usos_restantes == 0:
            self.vertice = None
            return True
        return False

class Criatura:
    def __init__(self, grafo, vertice, pontos_vida=100, pontos_ataque=10):
        self.grafo = grafo
        self.vertice = vertice
        self.pontos_vida = pontos_vida
        self.pontos_vida_maximos = pontos_vida
        self.pontos_ataque = pontos_ataque
    
    def mover(self, novo_vertice):
        self.vertice = novo_vertice
    
    def atacar(self, alvo):
        dano_total = randint(0.3*self.pontos_ataque, self.pontos_ataque) 
        alvo.receber_dano(dano_total)
        
        return dano_total

    def receber_dano(self, quantidade):
        self.pontos_vida -= quantidade
        if self.pontos_vida < 0:
            self.pontos_vida = 0
            self.ressucitar()
    
    def ressucitar(self):
        vertice_antigo = self.vertice
        vertices_proibidos = [vertice_antigo, 0, 31]
        
        for vertice in self.grafo.nodes:
            if self.grafo.nodes[self.vertice]['evento'] == 'checkpoint':
                vertices_proibidos.append(vertice)
                
        vertices_disponiveis = [v for v in self.grafo.nodes if v not in vertices_proibidos]
        vertice_novo = choice(vertices_disponiveis)
        self.mover(vertice_novo)

class Personagem:
    def __init__(self, grafo, pontos_vida=100, pontos_ataque=10):
        self.grafo = grafo
        self.caminho = choice(list(nx.all_simple_paths(self.grafo, 0, 31)))
        self.ind_caminho = 0
        self.vertice = self.caminho[0]
        self.checkpoint_atual = 0
        self.pontos_vida = pontos_vida
        self.pontos_vida_maximos = pontos_vida
        self.vidas_restantes = 3
        self.tesouro = 0
        self.pontos_ataque = pontos_ataque
        self.arma = None  
        self.x = 131
        self.y = 300
    
    def mover(self):
        # A ser implementada
        self.ind_caminho += 1
        self.vertice = self.caminho[self.ind_caminho]
        self.alcançar_checkpoint()
        self.arma.vertice = self.vertice
        pass
    
    def transporta_tesouro(self):
        self.tesouro = self.pontos_vida - self.pontos_ataque
    
    def atacar(self, alvo):
        dano_total = randint(0.3*self.pontos_ataque, self.pontos_ataque)
        alvo.receber_dano(dano_total)
        self.arma.uso()
        
        if self.arma.verificar_quebrada():
            self.desequipar_arma()
            
        return dano_total

    def receber_dano(self, quantidade):
        self.pontos_vida -= quantidade
        if self.pontos_vida < 0:
            self.pontos_vida = 0
            self.vidas_restantes -= 1
            if self.vidas_restantes != 0:
                if self.checkpoint_atual != None:
                    self.ressucitar()
                else:
                    self.fim_de_jogo()
            else:
                self.fim_de_jogo()
            
        if self.tesouro != 0:
            self.transporta_tesouro()
        
    def usar_planta(self, planta):
        self.pontos_vida += planta.pontos_vida
        planta.vertice = None
        if self.pontos_vida > self.pontos_vida_maximos:
            self.pontos_vida = self.pontos_vida_maximos

    def equipar_arma(self, arma):
        self.arma = arma
        self.pontos_ataque += self.arma.pontos_ataque
        if self.tesouro != 0:
            self.transporta_tesouro()

    def desequipar_arma(self):
        self.pontos_ataque -= self.arma.pontos_ataque
        self.arma = None
        
    def ressucitar(self):
        self.vidas_restantes -= 1
        if self.vidas_restantes == 0:
            self.fim_de_jogo()
        else:
            self.pontos_vida = self.pontos_vida_maximos
            self.vertice = self.checkpoint_atual
            self.grafo.nodes[self.vertice]['evento'] = 'none'
            self.checkpoint_atual = 0
    
    def fim_de_jogo(self):
        print("Fim de jogo")
        
    
    def alcançar_checkpoint(self):
        if self.grafo.nodes[self.vertice]['evento'] == 'checkpoint':
            self.checkpoint_atual = self.vertice

def inicializa_capitao(grafo):
    capitao = Personagem(grafo=grafo)
    arma_inicial = Arma("Lâmina do explorador", "Lâmina modesta e forte, aço leve e punho de couro. Boa para novatos.", capitao.vertice, 10)
    anim_capitao = Animacao()
    capitao.arma = arma_inicial
    capitao_idle = carregar_frames("images\Idle-5frm.png", 5)
    capitao_caminha = carregar_frames("images\Run-6frm.png", 6)
    capitao_ataca = carregar_frames("images\Atk1-6frm.png", 6)
    capitao_dano = carregar_frames("images\Hit-3frm.png", 3)
    capitao_morre = carregar_frames("images\Death-4frm.png", 4)
    capitao_saca = carregar_frames("images\Gun-Out-6frm.png", 6)
    capitao_guarda = carregar_frames("images\Gun-in-5frm.png", 5)
    
    return capitao, anim_capitao, [capitao_idle, capitao_caminha, capitao_ataca, capitao_dano, capitao_morre, capitao_saca, capitao_guarda]

# OBS
    # self.lista_vertices =  list(self.grafo.nodes()) = list(self.grafo.nodes) que é uma lista dos indices dos vértices
    # Para acessar um vértice a partir de um indice, faz-se self.grafo.nodes[indice] = self.grafo.nodes()[indice]
