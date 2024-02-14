from animacoes import carregar_frames, Animacao
class Arma:
    def __init__(self, nome, pontos_ataque, usos_maximos=3):
        self.pontos_ataque = pontos_ataque
        self.usos_maximos = usos_maximos
        self.usos_restantes = usos_maximos
        self.vertice = None
        self.util = True

    def uso(self):
        self.usos_restantes -= 1
    
    def verificar_quebrada(self):
        if self.usos_restantes == 0:
            self.util = False
            return True
        return False


class Criatura:
    def __init__(self, vertice, pontos_vida=100, pontos_ataque=10,):
        self.pontos_vida = pontos_vida
        self.pontos_vida_maximos = pontos_vida
        self.pontos_ataque = pontos_ataque
        self.vertice = vertice
        self._x = 100
        self._y = 100
    
    def mover(self):
        # A ser implementada
        pass
    
    def atacar(self, alvo):
        dano_total = self.pontos_ataque # Mudar: O dano é um valor aleatório dos pontos de ataque do atacante
        alvo.receber_dano(dano_total)
        
        return dano_total

    def receber_dano(self, quantidade):
        self.pontos_vida -= quantidade
        if self.pontos_vida < 0:
            self.pontos_vida = 0
        


class Personagem:
    def __init__(self, vertice=1, pontos_vida=100, pontos_ataque=10):
        self.pontos_vida = pontos_vida
        self.pontos_vida_maximos = pontos_vida
        self.pontos_ataque = pontos_ataque
        self.arma = None  
        self.tesouro = 0
        self.vertice = vertice
        self._x = 100
        self._y = 100
    
    def mover(self):
        # A ser implementada
        pass
    
    def transporta_tesouro(self):
        self.tesouro = self.pontos_vida - self.pontos_ataque
    
    def atacar(self, alvo):
        dano_total = self.pontos_ataque # Mudar: O dano é um valor aleatório dos pontos de ataque do atacante
        alvo.receber_dano(dano_total)
        self.arma.uso()
        
        if self.arma.verificar_quebrada():
            self.desequipar_arma()
            
        return dano_total

    def receber_dano(self, quantidade):
        self.pontos_vida -= quantidade
        if self.pontos_vida < 0:
            self.pontos_vida = 0
        
        if self.tesouro != 0:
            self.transporta_tesouro()

    def curar(self, quantidade):
        self.pontos_vida += quantidade
        if self.pontos_vida > self.pontos_vida_maximos:
            self.pontos_vida = self.pontos_vida_maximos

    def equipar_arma(self, arma):
        self.arma = arma
        self.pontos_ataque += self.arma.pontos_ataque
        self.arma.vertice = self.vertice
        if self.tesouro != 0:
            self.transporta_tesouro()

    def desequipar_arma(self):
        self.pontos_ataque -= self.arma.pontos_ataque
        self.arma = None
    
    def reiniciar_apos_checkpoint(self):
        self.pontos_vida = self.pontos_vida_maximos
        self.pontos_ataque = 10

def inicializa_capitao():
    capitao = Personagem()
    arma_inicial = Arma("Lâmina do explorador", 10)
    anim_capitao = Animacao()
    capitao.arma = arma_inicial
    capitao_idle = carregar_frames("images\IDLE.png", 3)
    capitao_caminha = carregar_frames("images\WALK.png", 8)
    capitao_ataca = carregar_frames("images\ATTACK.png", 7)
    capitao_morre = carregar_frames("images\DEATH.png", 10)
    
    
    return capitao, anim_capitao, [capitao_idle, capitao_caminha, capitao_ataca, capitao_morre]
