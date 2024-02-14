import pygame as pg
from animacoes import carregar_frames, calc_distancia, Animacao
from personagem import Personagem, Arma, inicializa_capitao

# Variáveis iniciais
pg.init()
altura, largura = (600, 800)
tela = pg.display.set_mode((1200, altura))
pg.display.set_caption("Lost Treasure Island")

# Capitão Daleo
capitao, anim_capitao, lista_anim_cap = inicializa_capitao()
anim_capitao.definir_frames(lista_anim_cap[0])

# Música de fundo
pg.mixer.music.load("sounds\8bit Bossa.mp3")
pg.mixer.music.play(-1)

# Loop principal
executando = True
while executando:
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            executando = False
            
    # Lógica da animação
    anim_capitao.atualizar()
    tela.fill((0, 0, 0))
    
    # Desenha o frame atual na tela
    tela.blit(anim_capitao.obter_frame_atual(), (capitao._x, capitao._y))

    pg.display.flip()
    
pg.mixer.music.stop()
pg.quit()