import pygame as pg

class Tela:
    def __init__(self, largura, altura, titulo):
        pg.init()
        self.largura = largura
        self.altura = altura
        self.tela = pg.display.set_mode((largura, altura))
        pg.display.set_caption(titulo)
        self.imagem_fundo = None 

    def definir_imagem_fundo(self, caminho_imagem):
        imagem = pg.image.load(caminho_imagem)
        imagem_redimensionada = pg.transform.scale(imagem, (self.largura, self.altura))
        self.imagem_fundo = imagem_redimensionada

    def desenhar_elemento(self, imagem, posicao):
        self.tela.blit(imagem, posicao)

    def exibir_mensagem(self, mensagem, posicao, tamanho_fonte=30, cor=(255, 255, 255), largura_maxima=800):
        fonte = pg.font.Font(None, tamanho_fonte)
        
        palavras = mensagem.split(' ')
        linhas = []
        linha_atual = ''
        
        for palavra in palavras:
            texto_teste = linha_atual + ' ' + palavra if linha_atual else palavra
            largura_texto, _ = fonte.size(texto_teste)
            
            if largura_maxima is not None and largura_texto > largura_maxima:
                linhas.append(linha_atual)
                linha_atual = palavra
            else:
                linha_atual = texto_teste
        
        linhas.append(linha_atual)
        
        altura_texto = fonte.get_height()
        
        for i, linha in enumerate(linhas):
            texto_renderizado = fonte.render(linha, True, cor)
            largura_texto, _ = fonte.size(linha)
            
            pos_x = posicao[0]
            pos_y = posicao[1] + i * altura_texto
            
            self.tela.blit(texto_renderizado, (pos_x, pos_y))
    
    def desenhar_botao(self, texto, posicao, tamanho=(150, 50), cor_fundo=(0, 0, 255), cor_texto=(255, 255, 255)):
        pg.draw.rect(self.tela, cor_fundo, (posicao[0], posicao[1], tamanho[0], tamanho[1]))
        fonte = pg.font.Font(None, 30)
        texto_renderizado = fonte.render(texto, True, cor_texto)
        self.tela.blit(texto_renderizado, (posicao[0] + 10, posicao[1] + 10))

    def aguardar_clique_botao(self):
        botao_clicado = None
        while botao_clicado is None:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    pg.quit()
                    exit()
                elif evento.type == pg.MOUSEBUTTONDOWN:
                    posicao_mouse = pg.mouse.get_pos()
                    if 50 <= posicao_mouse[0] <= 200 and 400 <= posicao_mouse[1] <= 450:
                        botao_clicado = "Lutar"
                    elif 250 <= posicao_mouse[0] <= 400 and 400 <= posicao_mouse[1] <= 450:
                        botao_clicado = "Fugir"
        return botao_clicado

    def atualizar_tela(self):
        pg.display.flip()

    def limpar_tela(self):
        self.tela.fill((0, 0, 0))



