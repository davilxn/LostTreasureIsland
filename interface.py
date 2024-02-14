import pygame as pg

class Interface:
    def __init__(self, largura, altura):
        pg.init()
        self.largura = largura
        self.altura = altura
        self.tela = pg.display.set_mode((largura, altura))
        pg.display.set_caption("Lost Treasure Island")

    def desenhar_elemento(self, imagem, posicao):
        self.tela.blit(imagem, posicao)

    def exibir_mensagem(self, mensagem, posicao, tamanho_fonte=30, cor=(255, 255, 255)):
        fonte = pg.font.Font(None, tamanho_fonte)
        texto = fonte.render(mensagem, True, cor)
        self.tela.blit(texto, posicao)

    def aguardar_evento(self):
        # Aguarda eventos do jogador e retorna o primeiro evento obtido
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                pg.quit()
                exit()
            return evento

    def atualizar_tela(self):
        pg.display.flip()

    def limpar_tela(self):
        self.tela.fill((0, 0, 0))