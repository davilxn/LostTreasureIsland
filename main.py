from grafo import Grafo
from interface import Tela
from random import choice
import pygame as pg
from utils import inicializa_grafo, mover_em_linha_reta, inicializa_capitao, turno_de_batalha

# As telas
tela_principal = Tela(1200, 700, "LostTreasureIsland")
tela_principal.definir_imagem_fundo("images\PNG map.jpg")

tela_luta = None

# O grafo
grafo = Grafo()
inicializa_grafo(grafo,"./pontos.json")

# Capitão Daleo
capitao  = inicializa_capitao(grafo)
capitao.animacao.definir_frames(capitao.lista_anim[capitao.estado], capitao.estado, capitao.estado)

# Música de fundo
pg.mixer.music.load("sounds\8bit Bossa.mp3")
pg.mixer.music.play(-1)

# Variáveis de controle
executando = True
turno_batalha = 0
batalha, checkpoint, tesouro = False, False, False
decisao_jogador = None

# Loop principal
while executando:
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            executando = False
        
        elif evento.type == pg.MOUSEBUTTONDOWN:
            capitao.mover()
            capitao.interacao_vertice()
            
    if capitao.em_batalha and not batalha:
        mensagem = "Você encontrou um monstro sedento por sangue e destruição! O que deseja fazer?"
        tela_principal.exibir_mensagem(mensagem, (200, 350))
        tela_principal.desenhar_botao("Lutar", (50, 400))
        tela_principal.desenhar_botao("Fugir", (250, 400))
        tela_principal.atualizar_tela()

        decisao_jogador = tela_principal.aguardar_clique_botao()
        
        if decisao_jogador == "Lutar":
            batalha = True
            if tela_luta is None:
                tela_luta = Tela(600, 300, "Fight")
                fundos = ["images\Battleground1.png", "images\Battleground3.png", "images\Battleground4.png"]
                fundo_escolhido = choice(fundos)
                tela_luta.definir_imagem_fundo(fundo_escolhido)
                
        elif decisao_jogador == "Fugir":
            # Com o capitão
            batalha = False
            dano = capitao.grafo.vertices[capitao.vertice].objeto.pontos_ataque
            capitao.receber_dano(dano)
            capitao.em_batalha = False
            
            # Com a tela
            tela_principal.limpar_tela()
            tela_principal.desenhar_elemento(tela_principal.imagem_fundo, (0,0))
            mensagem = f"Você fugiu da criatura, mas antes que conseguisse, foi atingido com um golpe raspão. Perdeu {dano} pontos de vida."
            tela_principal.exibir_mensagem(mensagem, (200, 350))
            tela_principal.atualizar_tela()
            pg.time.delay(5000)
            
        decisao_jogador = None

    if batalha: 
        monstro = capitao.grafo.vertices[capitao.vertice].objeto
        monstro_estado_anterior = monstro.estado
        capitao_estado_anterior = capitao.estado
        monstro.estado = 0
        capitao.estado = 0
        
        capitao.animacao.atualizar()
        monstro.animacao.atualizar()
        
        # Definir frames após a atualização
        capitao.animacao.definir_frames(capitao.lista_anim[capitao.estado], capitao.estado, capitao_estado_anterior)
        monstro.animacao.definir_frames(monstro.lista_anim[monstro.estado], monstro.estado, monstro_estado_anterior)
        
        tela_luta.desenhar_elemento(tela_luta.imagem_fundo, (0, 0))
        tela_luta.desenhar_elemento(capitao.animacao.obter_frame_atual(), (75, 100))
        tela_luta.desenhar_elemento(monstro.animacao.obter_frame_atual(), (monstro.x_luta, monstro.y_luta))

        tela_luta.atualizar_tela()
    
    else: # Lógica Capitão correndo no mapa
        capitao.animacao.atualizar()
        estado_anterior = capitao.estado

        destino = (capitao.grafo.vertices[capitao.vertice].x-123, capitao.grafo.vertices[capitao.vertice].y-123)
        mover_em_linha_reta(capitao, destino)

        capitao.animacao.definir_frames(capitao.lista_anim[capitao.estado], capitao.estado, estado_anterior)

        tela_principal.desenhar_elemento(tela_principal.imagem_fundo, (0,0))
        tela_principal.desenhar_elemento(capitao.animacao.obter_frame_atual(), (capitao.x, capitao.y))

        tela_principal.atualizar_tela()
    
pg.mixer.music.stop()
pg.quit()

### Área de comentários e observações
# Dar nomes diferentes para os perigos que existirem.
# Criar lógicas dos itens. Talvez uma classe Item, pai de Armas. Itens pelo mapa. Coletar e usar itens.
# Dar descrições para todos os itens e todos os monstros. Ver também o negócio das cartinhas com itens e monstros.

# Mostrar informações do personagem na tela. Leozim
# Mostrar informações dos itens na tela, quando o personagem chegar no vértice. Leozim
# Mais de uma coisa no mesmo vértice. Leozim

# Arrumar a tela de luta. Turnos de luta. Davizito
# Criar a lógica dos monstros e das batalhas. Modificar a construção do grafo pra ter vértices de monstros e mais variedade nos perigos. Davizito
# Criar vários objetos do tipo Arma e PlantaMedicinal e espalhar pelos grafos. Como adicionar itens dentro de um vértice.