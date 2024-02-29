from grafo import Grafo
import pygame as pg
from utils import inicializa_grafo, mover_em_linha_reta
from utils import inicializa_capitao


# Variáveis iniciais
pg.init()
largura, altura = (1200, 700)
tela = pg.display.set_mode((largura, altura))
pg.display.set_caption("Lost Treasure Island")
imagem_fundo = pg.image.load("images\PNG map.jpg")


# O grafo
grafo = Grafo()
inicializa_grafo(grafo,"./pontos.json")

# Capitão Daleo
capitao, anim_capitao, lista_anim_cap = inicializa_capitao(grafo)
anim_capitao.definir_frames(lista_anim_cap[capitao.estado])

# Música de fundo
pg.mixer.music.load("sounds\8bit Bossa.mp3")
pg.mixer.music.play(-1)

# Loop principal
executando = True
while executando:
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            executando = False
        
        elif evento.type == pg.MOUSEBUTTONDOWN:
            capitao.mover()
            
    # Lógica da animação do Capitão
    anim_capitao.atualizar()
    estado_anterior = capitao.estado
    
    destino = (capitao.grafo.vertices[capitao.vertice].x-123, capitao.grafo.vertices[capitao.vertice].y-123)
    mover_em_linha_reta(capitao, destino)

    if capitao.estado != estado_anterior:
        anim_capitao.reiniciar_animacao()
        
    anim_capitao.definir_frames(lista_anim_cap[capitao.estado])
    
    # Desenha o frame atual na tela
    tela.blit(imagem_fundo, (0, 0))
    tela.blit(anim_capitao.obter_frame_atual(), (capitao.x, capitao.y))

    
    pg.display.flip()
    
pg.mixer.music.stop()
pg.quit()

### Área de comentários e observações
# OBS. Criar lógicas dos itens. Talvez uma classe Item, pai de Armas. Itens pelo mapa. Coletar e usar itens.
# Criar vários objetos do tipo Arma e PlantaMedicinal e espalhar pelos grafos. Como adicionar itens dentro de um vértice.
