from random import randint, choice
from animacoes import Animacao

class PlantaMedicinal:
    def __init__(self, nome, descricao, vertice=None, pontos_vida=25):
        self.nome = nome
        self.descricao = descricao
        self.vertice = vertice
        self.pontos_vida = pontos_vida
    
class Arma:
    def __init__(self, nome, descricao, pontos_ataque, imagem, usos_maximos=1000,vertice=None):
        self.nome = nome
        self.imagem = imagem
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
    def __init__(self, grafo, vertice=None, pontos_vida=100, pontos_ataque=20):
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
    
    def atacar(self, alvo):
        dano_total = randint(int(0.3*self.pontos_ataque), self.pontos_ataque) 
        alvo.receber_dano(dano_total)
        
        return dano_total

    def receber_dano(self, quantidade):
        self.pontos_vida -= quantidade
        if self.pontos_vida < 0:
            self.pontos_vida = 0
    
    def mover(self):
        if self.pontos_vida == 0:
            self.pontos_vida = 100
        vertice_antigo = self.vertice
        vertices_proibidos = [vertice_antigo, 0, 31]
        for vertice in self.grafo.vertices:
            if any(event == "checkpoint" for event in self.grafo.vertices[vertice].evento):
                vertices_proibidos.append(vertice)
                
        vertices_disponiveis = [v for v in self.grafo.vertices if v not in vertices_proibidos]
        vertice_novo = choice(vertices_disponiveis)
        
        # Remove o monstro do vértice atual
        self.grafo.vertices[vertice_antigo].objeto.remove(self)
        self.grafo.vertices[vertice_antigo].evento.remove("monstro")
        
        # Adiciona o monstro no novo vértice
        self.vertice = vertice_novo
        self.grafo.vertices[self.vertice].objeto.append(self)
        
        if isinstance(self.grafo.vertices[self.vertice].evento, str):
            self.grafo.vertices[self.vertice].evento = [self.grafo.vertices[self.vertice].evento]
        self.grafo.vertices[self.vertice].evento.append("monstro")
        
        self.verifica_rinha()
        
    def verifica_rinha(self):
        lista_monstros = []
        for obj in self.grafo.vertices[self.vertice].objeto:
            if isinstance(obj, Criatura) and obj != self:
                lista_monstros.append(obj)
        
        if len(lista_monstros) > 0:
            lista_monstros.append(self)
            self.rinha_criatura(lista_monstros)
    
    def rinha_criatura(self, lista_monstros):
        forte, fraco = None, None
        for monstro in lista_monstros:
            if forte == None and fraco == None:
                forte, fraco = monstro, monstro
            if monstro.pontos_ataque > forte.pontos_ataque:
                forte = monstro
            if monstro.pontos_ataque < fraco.pontos_ataque:
                fraco = monstro
        
        forte.receber_dano(fraco.pontos_ataque)
        if forte.pontos_vida <= 0:
            forte.pontos_vida = 0
            forte.mover()
        
        fraco.receber_dano(100)
        fraco.mover()
        for monstro in lista_monstros:
            if monstro != forte and monstro != fraco:
                monstro.receber_dano(forte.pontos_ataque)
                monstro.mover()
        
class Personagem:
    def __init__(self, grafo, pontos_vida=100, pontos_ataque=10):
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
        self.menor_vida = 100
        self.pontos_vida_maximos = pontos_vida
        self.vidas_restantes = 3
        self.tesouro = 0
        self.pontos_ataque = pontos_ataque
        self.maior_ataque = self.pontos_ataque
        self.arma = None  
        
        # Auxiliares
        self.estado = 0
        self.em_batalha = False
        self.arma_nova = False
        self.planta = False
        self.animacao = Animacao()
        self.lista_anim = []
    
    def mover(self):
        self.ind_caminho += 1
        self.vertice = self.caminho[self.ind_caminho]
        self.arma.vertice = self.vertice
        
        if not self.tesouro:
            self.menor_vida = self.pontos_vida
            self.maior_ataque = self.pontos_ataque
            
        self.transporta_tesouro()
        
        # Os montros devem se mover, também
        for vertice in self.grafo.vertices:
            for obj in self.grafo.vertices[vertice].objeto:
                if isinstance(obj, Criatura):
                    obj.mover()
        
    def estado_atual(self):
        print(f"\nVida: {self.pontos_vida}")
        if self.arma != None:
            print(f"Ataque: {self.arma.pontos_ataque}")
            print(f"Usos restantes da arma: {self.arma.usos_restantes}")
        else:
            print(f"Ataque: {self.pontos_ataque}")
        print(f"Checkpoint atual: {self.checkpoint_atual}")
        print(f"Vidas restantes: {self.vidas_restantes}")
        print(f"Tesouro: {self.tesouro}%")
        print(f"Caminho: {self.caminho}\n")
    
    def transporta_tesouro(self):
        if self.tesouro:                    
            self.tesouro = self.menor_vida - self.maior_ataque
            if self.tesouro < 0:
                self.tesouro = 0
    
    def atacar(self, alvo):
        dano_total = randint(int(0.3*self.pontos_ataque), self.pontos_ataque)
        alvo.receber_dano(dano_total)
        
        if self.arma.verificar_quebrada():
            self.desequipar_arma()
            
        return dano_total

    def receber_dano(self, quantidade):
        self.pontos_vida -= quantidade
        if self.pontos_vida <= 0:
            self.pontos_vida = 0
        
        if self.tesouro:
            if self.pontos_vida > 0 and self.pontos_vida < self.menor_vida:
                self.menor_vida = self.pontos_vida  
             
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
        if self.tesouro:
            if self.pontos_ataque > self.maior_ataque:
                self.maior_ataque = self.pontos_ataque
        if self.tesouro != 0:
            self.transporta_tesouro()

    def desequipar_arma(self):
        self.arma = None
        arma_inicial = Arma("Lâmina do explorador", "Lâmina modesta e forte, aço leve e punho de couro. Boa para novatos.", 20, imagem="images\GUI\Lâmina do Explorador.png", vertice=self.vertice)
        self.equipar_arma(arma_inicial)
        
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
        exit()
        
    def interacao_vertice(self):
        if any(event == "checkpoint" for event in self.grafo.vertices[self.vertice].evento):
            print("Você alcançou um checkpoint. Descanse, aprecie a vista e prepare-se.")
            self.checkpoint_atual = self.vertice
        
        if any(event == "areiaMovedica" or event == "florestaPerigosa" for event in self.grafo.vertices[self.vertice].evento):
            dano = randint(1, 10)
            print(f"Você encontrou um perigo. Perdeu {dano} pontos de vida. Tome cuidado!")
        
        if any(event == "arma" for event in self.grafo.vertices[self.vertice].evento):
            arma = [obj for obj in self.grafo.vertices[self.vertice].objeto if isinstance(obj, Arma)]
            print(f"Que sorte! Você encontrou: {arma[0].nome}.")
            print(f"{arma[0].descricao}")
            self.arma_nova = True
        
        if any(event == "plantaMedicinal" for event in self.grafo.vertices[self.vertice].evento):
            self.planta = True
            planta_med = [obj for obj in self.grafo.vertices[self.vertice].objeto if isinstance(obj, PlantaMedicinal)]
            print(f"Que sorte! Você encontrou: {planta_med[0].nome}.")
            print(f"{planta_med[0].descricao}")
            if self.pontos_vida < 100:
                self.pontos_vida += planta_med[0].pontos_vida
                if self.pontos_vida > 100:
                    self.pontos_vida = 100
                print("Você utilizou utilizou como remédio para fazer um curativo e sua vida foi regenerada!")
            else:
                print("No entanto, não lhe não lhe servirá de nada, pois você já está bem de vida. Sombra e água fresca.")
                
        if any(event == "monstro" for event in self.grafo.vertices[self.vertice].evento):
            print("Você encontrou um montro sedendo por sangue e destruição!")
            self.em_batalha = True
        
        if self.vertice == 31 and self.caminho[-1] == 31:
            self.caminho = self.grafo.dfs(31,0)
            self.ind_caminho = 0
            self.vertice = self.caminho[0]
            self.tesouro = self.pontos_vida - self.arma.pontos_ataque
            print("Parabéns, você encontrou o tesouro! Poderá desfrutar da sua conquista, mas antes, volte para o navio.")
        
        if self.vertice == 0 and self.caminho[-1] == 0:
            if self.tesouro:
                print("Você conseguiu. Conquistou o grande tesouro tão desejado por todos os aventureiros. Boa viagem de volta pra casa, e jamais cometa a estupidez de retornar a esta ilha.")
            else:
                print("Você foi ao inferno e, embora não tenha conseguido o tesouro, sobreviveu. Agradeça aos céus, volte pra casa somente com as histórias, e jamais retorne.")
            self.fim_de_jogo()
        
        self.estado_atual()
        
    
