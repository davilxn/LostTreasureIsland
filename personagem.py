from random import randint, choice
from animacoes import Animacao

class PlantaMedicial:
    def __init__(self, nome, descricao, vertice, pontos_vida=25):
        self.nome = nome
        self.descricao = descricao
        self.vertice = vertice
        self.pontos_vida = pontos_vida
    
class Arma:
    def __init__(self, nome, descricao, vertice, pontos_ataque, usos_maximos=1000000):
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
    def __init__(self, grafo, vertice=None, pontos_vida=100, pontos_ataque=40):
        self.grafo = grafo
        self.vertice = vertice
        self.pontos_vida = pontos_vida
        self.pontos_vida_maximos = pontos_vida
        self.pontos_ataque = pontos_ataque
        self.estado = 0
        self.x_luta = 0
        self.y_luta = 0
        self.animacao = Animacao()
        self.lista_anim = []
    
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
    
    def ressucitar(self):
        vertice_antigo = self.vertice
        vertices_proibidos = [vertice_antigo, 0, 31]
        
        for vertice in self.grafo.vertices:
            if self.grafo.vertices[vertice].evento == 'checkpoint':
                vertices_proibidos.append(vertice)
                
        vertices_disponiveis = [v for v in self.grafo.vertices if v not in vertices_proibidos]
        vertice_novo = choice(vertices_disponiveis)
        self.mover(vertice_novo)

class Personagem:
    def __init__(self, grafo, pontos_vida=100, pontos_ataque=0):
        # Referentes ao grafo
        self.grafo = grafo
        self.caminho = self.grafo.dfs(0,31)
        self.ind_caminho = 0
        self.vertice = self.caminho[0]
        self.checkpoint_atual = 0
        self.x = self.grafo.vertices[self.vertice].x - 123
        self.y = self.grafo.vertices[self.vertice].y - 123
        
        # Referentes ao Capitão
        self.pontos_vida = pontos_vida
        self.pontos_vida_maximos = pontos_vida
        self.vidas_restantes = 3
        self.tesouro = 0
        self.pontos_ataque = pontos_ataque
        self.arma = None  
        
        # Auxiliares
        self.estado = 0
        self.em_batalha = False
        self.animacao = Animacao()
        self.lista_anim = []
    
    def mover(self):
        self.ind_caminho += 1
        self.vertice = self.caminho[self.ind_caminho]
        self.arma.vertice = self.vertice
        self.transporta_tesouro()
        
    def estado_atual(self):
        print(f"\nVida: {self.pontos_vida}")
        print(f"Ataque: {self.pontos_ataque}")
        print(f"Vidas restantes: {self.vidas_restantes}")
        print(f"Checkpoint atual: {self.checkpoint_atual}")
        print(f"Tesouro: {self.tesouro}%")
        print(f"Caminho: {self.caminho}\n")
    
    def transporta_tesouro(self):
        if self.tesouro:
            if self.vidas_restantes == 3:
                self.tesouro = self.pontos_vida - self.arma.pontos_ataque
            else:
                if self.pontos_vida < self.tesouro:
                    self.tesouro = self.pontos_vida - self.arma.pontos_ataque
    
    def atacar(self, alvo):
        dano_total = randint(0.3*self.pontos_ataque, self.pontos_ataque)
        alvo.receber_dano(dano_total)
        self.arma.uso()
        
        if self.arma.verificar_quebrada():
            self.desequipar_arma()
            
        return dano_total

    def receber_dano(self, quantidade):
        self.pontos_vida -= quantidade
        if self.pontos_vida <= 0:
            self.pontos_vida = 0
            
        if self.tesouro and self.pontos_vida > 0:
            self.transporta_tesouro()
        
    def usar_planta(self, planta):
        self.pontos_vida += planta.pontos_vida
        planta.vertice = None
        if self.pontos_vida > self.pontos_vida_maximos:
            self.pontos_vida = self.pontos_vida_maximos

    def equipar_arma(self, arma):
        self.arma = arma
        self.pontos_ataque = self.arma.pontos_ataque
        if self.tesouro != 0:
            self.transporta_tesouro()

    def desequipar_arma(self):
        self.pontos_ataque = 0
        self.arma = None
        
    def morte(self):
        self.vidas_restantes -= 1
        if self.vidas_restantes == 0:
            self.fim_de_jogo()
        else:
            if self.checkpoint_atual != 0:
                self.pontos_vida = self.pontos_vida_maximos
                self.vertice = self.checkpoint_atual
                self.grafo.vertices[self.vertice].evento = 'none'
                self.checkpoint_atual = 0
            
            else:
                self.pontos_vida = self.pontos_vida_maximos
                self.vertice = self.checkpoint_atual
                self.tesouro = 0
            
            # Recalculando o caminho
            if self.tesouro:
                self.caminho = self.grafo.dfs(self.vertice, 0)
                self.ind_caminho = 0
                self.vertice = self.caminho[0]
            else:
                self.caminho = self.grafo.dfs(self.vertice, 31)
                self.ind_caminho = 0
                self.vertice = self.caminho[0]
    
    def fim_de_jogo(self):
        print("Fim de jogo.")
    
    def interacao_vertice(self):
        if self.grafo.vertices[self.vertice].evento == 'checkpoint':
            print(f"Você alcançou um checkpoint. Descanse, aprecie a vista e prepare-se. {self.vertice}")
            self.checkpoint_atual = self.vertice
        
        elif self.grafo.vertices[self.vertice].evento == "monstro":
            print("Você encontrou um montro sedendo por sangue e destruição!")
            self.em_batalha = True
        
        elif self.vertice == 31 and (not self.tesouro):
            self.caminho = self.grafo.dfs(31,0)
            self.ind_caminho = 0
            self.vertice = self.caminho[0]
            self.tesouro = self.pontos_vida - self.arma.pontos_ataque
            print("Parabéns, você encontrou o tesouro! Poderá desfrutar da sua conquista, mas antes, volte para o navio.")
            
        elif self.tesouro and self.vertice == 0:
            print("Você conseguiu. Conquistou o grande tesouro tão desejado por todos os aventureiros. Boa viagem de volta pra casa, e não cometa a estupidez de retornar a esta ilha.")
        
        self.estado_atual()
        
    
