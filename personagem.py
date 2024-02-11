class Personagem:
    def __init__(self, pontos_vida=100, pontos_ataque=10):
        self.pontos_vida = pontos_vida
        self.pontos_vida_maximos = pontos_vida
        self.pontos_ataque = pontos_ataque
        self.arma = None  # Pode ser uma instância da classe Arma
    
    def atacar(self, alvo):
        if self.arma is not None:
            dano_total = self.pontos_ataque + self.arma.pontos_ataque
            alvo.receber_dano(dano_total)
            return dano_total
        else:
            alvo.receber_dano(self.pontos_ataque)
            return self.pontos_ataque

    def receber_dano(self, quantidade):
        self.pontos_vida -= quantidade
        if self.pontos_vida < 0:
            self.pontos_vida = 0

    def curar(self, quantidade):
        self.pontos_vida += quantidade
        if self.pontos_vida > self.pontos_vida_maximos:
            self.pontos_vida = self.pontos_vida_maximos

    def equipar_arma(self, arma):
        self.arma = arma

    def desequipar_arma(self):
        self.arma = None