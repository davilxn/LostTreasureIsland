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

    def exibir_mensagem(self, mensagem, posicao, tamanho_fonte=30, cor=(101, 58, 26), largura_maxima=800, red=False):
        if red==True:
            tamanho_fonte = 23
        
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
        if red == True:
            gui_bar = pg.image.load("images\GUI\GUI 3.png")
            gui_bar_redimensionada = pg.transform.scale(gui_bar, (550, 200))
            self.desenhar_elemento(gui_bar_redimensionada, (20,posicao[1]-50))
        else:
            gui_bar = pg.image.load("images\GUI\GUI 3.png")
            self.desenhar_elemento(gui_bar, (20,posicao[1]-50))
        for i, linha in enumerate(linhas):
            texto_renderizado = fonte.render(linha, True, cor)
            largura_texto, _ = fonte.size(linha)
            
            pos_x = posicao[0]
            pos_y = posicao[1] + i * altura_texto
            
            self.tela.blit(texto_renderizado, (pos_x, pos_y))
    
    def desenhar_botao(self, texto, posicao, tamanho=(150, 50), cor_fundo=(228,166,114), cor_texto=(101, 58, 26)):
        pg.draw.rect(self.tela, cor_fundo, (posicao[0] + 60, posicao[1] + 80, tamanho[0], tamanho[1]))
        fonte = pg.font.Font(None, 30)
        texto_renderizado = fonte.render(texto, True, cor_texto)
        self.tela.blit(texto_renderizado, (posicao[0] + 80, posicao[1] + 100))

    def desenhar_vida(self, vida_atual,local_y, local_x, cor_fundo=(101, 58, 26), verde=(0, 255, 0), cor_texto=(101, 58, 26), altura=17, largura=100):
        imagem_fundo = pg.image.load("images\GUI\GUI 6.png")
        self.desenhar_elemento(imagem_fundo, (local_y-8,local_x-8))
        barra_tam = int (largura * (vida_atual/100))
        pg.draw.rect(self.tela, cor_fundo, (local_y, 2*local_x, largura, altura))
        fonte = pg.font.Font(None, 20)
        info = fonte.render('Vida', True,cor_texto)
        pg.draw.rect(self.tela, verde, (local_y, 2*local_x, barra_tam, altura))
        self.tela.blit(info,(local_y,local_x))
    
    def desenhar_ataquepts(self, pts_ataque, local_y, local_x, altura=20, largura=50, cor_fundo=(0, 0, 0), cor_texto=(101, 58, 26)):
        imagem_fundo = pg.image.load("images\GUI\GUI 5.png")
        self.desenhar_elemento(imagem_fundo, (local_y-8,local_x-8))
        pts_ataque_str = str(pts_ataque)
        fonte1 = pg.font.Font(None, 30)
        fonte2 = pg.font.Font(None, 20)
        pts_ataque_renderizado = fonte1.render( pts_ataque_str, True, cor_texto)
        info = fonte2.render('Ataque', True,cor_texto)
        
        self.tela.blit(pts_ataque_renderizado, (local_y, 2*local_x))
        self.tela.blit(info, (local_y, local_x))
    
    def desenhar_arma(self, imagem, usos_restantes, local_y=600, local_x=25, cor_texto=(101, 58, 26)):
        imagem_fundo = pg.image.load("images\GUI\GUI 2.png")
        self.desenhar_elemento(imagem_fundo, (local_y-8,local_x-17))
        imagem_core = pg.image.load(imagem)
        self.desenhar_elemento(imagem_core,(local_y,local_x))
        fonte2 = pg.font.Font(None, 20)
        info = fonte2.render(str(usos_restantes), True,cor_texto)
        self.tela.blit(info, (local_y, local_x-10))


    def desenhar_tesouro(self, por_tesouro, local_y=670, local_x=25, cor_texto=(101, 58, 26)):
        imagem_fundo = pg.image.load("images\GUI\GUI 2.png")
        self.desenhar_elemento(imagem_fundo, (local_y-8,local_x-17))
        imagem_core = pg.image.load("images\GUI\Bau do Tesouro.png")
        self.desenhar_elemento(imagem_core,(local_y,local_x))
        fonte2 = pg.font.Font(None, 20)
        info = fonte2.render(str(por_tesouro), True,cor_texto)
        self.tela.blit(info, (local_y, local_x-10))



    def desenhar_coracao(self, num_core, local_y=750, local_x=20):
        imagem_fundo = pg.image.load("images\GUI\GUI 4.png")
        self.desenhar_elemento(imagem_fundo, (local_y-8,local_x-14))
        i = 0
        while num_core != 0:
            imagem_core = pg.image.load("images\capitao\heart.png")
            imagem_redimensionada = pg.transform.scale(imagem_core, (20, 20))
            self.desenhar_elemento(imagem_redimensionada,(local_y+i,local_x))
            i += 30
            num_core -= 1

    def aguardar_clique_botao(self, pos1, pos2, bot1, bot2):
        botao_clicado = None
        while botao_clicado is None:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    pg.quit()
                    exit()
                elif evento.type == pg.MOUSEBUTTONDOWN:
                    posicao_mouse = pg.mouse.get_pos()
                    if pos1[0] <= posicao_mouse[0] <= pos1[1] and pos1[2] <= posicao_mouse[1] <= pos1[3]:
                        botao_clicado = bot1
                    elif pos2[0] <= posicao_mouse[0] <= pos2[1] and pos2[2] <= posicao_mouse[1] <= pos2[3]:
                        botao_clicado = bot2
        return botao_clicado
    

    def atualizar_tela(self):
        pg.display.flip()

    def limpar_tela(self):
        self.tela.fill((0, 0, 0))



