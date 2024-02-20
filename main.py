import pygame as pg
from animacoes import carregar_frames, calc_distancia, Animacao
from personagem import Personagem, Arma, inicializa_capitao
import lostTreasureIsland as li 

import networkx as nx

# Variáveis iniciais
pg.init()
largura, altura = (1200, 700)
tela = pg.display.set_mode((largura, altura))
pg.display.set_caption("Lost Treasure Island")
imagem_fundo = pg.image.load("images\PNG map.png")
imagem_fundo = pg.transform.scale(imagem_fundo, (largura, altura))

# O grafo
grafo = li.createisland()
grafo = li.inputInGraph(grafo)

# Capitão Daleo
capitao, anim_capitao, lista_anim_cap = inicializa_capitao(grafo)
anim_capitao.definir_frames(lista_anim_cap[5])

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
    
    # Desenha o frame atual na tela
    tela.blit(imagem_fundo, (0, 0))
    tela.blit(anim_capitao.obter_frame_atual(), (capitao.x, capitao.y))

    pg.display.flip()
    
pg.mixer.music.stop()
pg.quit()
print(grafo.nodes)

### Área de comentários e observações
# OBS. Criar lógicas dos itens. Talvez uma classe Item, pai de Armas. Itens pelo mapa. Coletar e usar itens.
# Mapa tá meio estranho. 31 vértices e começa do vértice 0.
# Falar sobre uso dos vértices para a movimentação do Capitão.
# Organizar os vértices do grafo na tela do PyGame.
# Criar vários objetos do tipo Arma e PlantaMedicinal e espalhar pelos grafos. Como adicionar itens dentro de um vértice.
# O atributo vertice em Personagem é um inteiro. Poderia mudar pra ser um objeto vértice do NetworkX e receber algo tipo vertice.num.
# Falar sobre o inventário