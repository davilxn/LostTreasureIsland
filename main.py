import pygame as pg
from animacoes import carregar_frames, Animacao

# Variáveis iniciais
pg.init()
altura, largura = (600, 800)
tela = pg.display.set_mode((largura, altura))
pg.display.set_caption("Lost Treasure Island")

# Capitão Daleo
frames_capitao = carregar_frames("images\Run-6frm.png", 6)
anim_capitao = Animacao(frames_capitao, 10)

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
    
    # Limpa a tela
    tela.fill((0, 0, 0))
    
    # Desenha o frame atual na tela
    tela.blit(anim_capitao.obter_frame_atual(), (100, 100))

    pg.display.flip()
    
pg.mixer.music.stop()
pg.quit()