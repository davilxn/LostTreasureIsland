from grafo import Grafo
from interface import Tela
from random import choice
from personagem import Criatura
import pygame as pg
from utils import inicializa_grafo, mover_em_linha_reta, inicializa_capitao

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
batalha, checkpoint, tesouro = False, False, False
decisao_jogador = None
ctrl_anim = 0
turno_capitao, turno_monstro, vez = False, False, False
estado_luta = None
turno = 0

# Loop principal
while executando:
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            executando = False
        
        elif evento.type == pg.MOUSEBUTTONDOWN:
            capitao.mover()
          
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
            
            estado_luta = choice([2,3,4,5])
                
        elif decisao_jogador == "Fugir":
            # Com o capitão
            batalha = False
            monstro = None
            for objeto in capitao.grafo.vertices[capitao.vertice].objeto:
                if isinstance(objeto, Criatura):
                    monstro = objeto
            dano = monstro.pontos_ataque
            capitao.receber_dano(dano)
            if capitao.pontos_vida == 0:
                capitao.morte()
            capitao.em_batalha = False
            
            # Com a tela
            tela_principal.limpar_tela()
            tela_principal.desenhar_elemento(tela_principal.imagem_fundo, (0,0))
            mensagem = f"Você fugiu da criatura, mas antes que conseguisse, foi atingido com um golpe raspão. Perdeu {dano} pontos de vida."
            tela_principal.exibir_mensagem(mensagem, (200, 350))
            tela_principal.atualizar_tela()
            #pg.time.delay(5000)
            
        decisao_jogador = None

    if batalha: 
        monstro = None
        for obj in capitao.grafo.vertices[capitao.vertice].objeto:
            if isinstance(obj, Criatura):
                monstro = obj
                
        fps = 50
        if ctrl_anim < fps*max(capitao.animacao.num_frames, monstro.animacao.num_frames):
            monstro_estado_anterior = monstro.estado
            capitao_estado_anterior = capitao.estado
            monstro.estado = 0
            capitao.estado = 0
            
            capitao.animacao.atualizar()
            monstro.animacao.atualizar()
            
            # Definir frames após a atualização
            capitao.animacao.definir_frames(capitao.lista_anim[capitao.estado], capitao.estado, capitao_estado_anterior)
            monstro.animacao.definir_frames(monstro.lista_anim[monstro.estado], monstro.estado, monstro_estado_anterior)
            
            ctrl_anim += 1
            if ctrl_anim == fps*max(len(capitao.lista_anim[0]), len(monstro.lista_anim[0])):
                turno_capitao = True
                ctrl_anim += 10000000000
                
        else:
            if turno < 3:
                capitao.animacao.atualizar()
                monstro.animacao.atualizar()
                
                # Capitão bate
                if turno_capitao and capitao.pontos_vida != 0 and monstro.pontos_vida != 0:
                    monstro_estado_anterior, capitao_estado_anterior = monstro.estado, capitao.estado
                    monstro.estado, capitao.estado = 0, estado_luta
                    
                    capitao.animacao.definir_frames(capitao.lista_anim[capitao.estado], capitao.estado, capitao_estado_anterior)
                    if capitao.animacao.indice_frame == capitao.animacao.num_frames-1:
                        turno_capitao = False
                        capitao.animacao.definir_frames(capitao.lista_anim[0], 0, capitao.estado)
                        monstro.animacao.definir_frames(monstro.lista_anim[2], 2, monstro.estado)
                
                # Monstro apanha       
                elif not turno_monstro and (not vez) and capitao.pontos_vida != 0 and monstro.pontos_vida != 0:
                    monstro_estado_anterior, capitao_estado_anterior = monstro.estado, capitao.estado
                    monstro.estado, capitao.estado = 2, 0
                    
                    monstro.animacao.definir_frames(monstro.lista_anim[monstro.estado], monstro.estado, monstro_estado_anterior)
                    if monstro.animacao.indice_frame == monstro.animacao.num_frames-1:
                        turno_monstro = True
                        capitao.atacar(monstro)
                        monstro.animacao.definir_frames(monstro.lista_anim[1], 1, monstro.estado) 
                
                # Monstro bate       
                elif turno_monstro and capitao.pontos_vida != 0 and monstro.pontos_vida != 0:
                    monstro_estado_anterior, capitao_estado_anterior = monstro.estado, capitao.estado
                    monstro.estado, capitao.estado = 1, 0
                    
                    monstro.animacao.definir_frames(monstro.lista_anim[monstro.estado], monstro.estado, monstro_estado_anterior)
                    if monstro.animacao.indice_frame == monstro.animacao.num_frames-1:
                        turno_monstro = False
                        vez = True
                        monstro.animacao.definir_frames(monstro.lista_anim[0], 0, monstro.estado)
                        capitao.animacao.definir_frames(capitao.lista_anim[6], 6, capitao.estado)
                    
                # Capitão apanha        
                elif not turno_capitao and capitao.pontos_vida != 0 and monstro.pontos_vida != 0:
                    monstro_estado_anterior, capitao_estado_anterior = monstro.estado, capitao.estado
                    monstro.estado, capitao.estado = 0, 6
                    
                    capitao.animacao.definir_frames(capitao.lista_anim[capitao.estado],capitao.estado, capitao_estado_anterior)
                    if capitao.animacao.indice_frame == capitao.animacao.num_frames-1:
                        turno_capitao, turno_monstro, vez = False, False, False
                        monstro.atacar(capitao)
                        ctrl_anim = 0
                        turno += 1
                
                # Capitão morre
                elif capitao.pontos_vida == 0 and monstro.pontos_vida != 0:
                    monstro_estado_anterior, capitao_estado_anterior = monstro.estado, capitao.estado
                    monstro.estado, capitao.estado = 0, 7
                    
                    capitao.animacao.definir_frames(capitao.lista_anim[capitao.estado],capitao.estado, capitao_estado_anterior)
                    if capitao.animacao.indice_frame == capitao.animacao.num_frames-1:
                        turno_capitao, turno_monstro, vez = False, False, False
                        ctrl_anim = 0
                        capitao.morte()
                        batalha = False
                        capitao.em_batalha = False
                        tela_principal = Tela(1200, 700, "LostTreasureIsland")
                        tela_principal.definir_imagem_fundo("images\PNG map.jpg")
                
                # Monstro morre
                elif monstro.pontos_vida == 0 and capitao.pontos_vida != 0:
                    capitao_estado_anterior, monstro_estado_anterior = capitao.estado, monstro.estado
                    capitao.estado, monstro.estado = 0, 3
                    
                    monstro.animacao.definir_frames(monstro.lista_anim[monstro.estado],monstro.estado, monstro_estado_anterior)
                    if monstro.animacao.indice_frame == monstro.animacao.num_frames-1:
                        turno_monstro, turno_capitao, vez = False, False, False
                        ctrl_anim = 0
                        monstro.mover()
                        batalha = False
                        capitao.em_batalha = False
                        tela_principal = Tela(1200, 700, "LostTreasureIsland")
                        tela_principal.definir_imagem_fundo("images\PNG map.jpg")

            else:
                turno = 0

        print(capitao.pontos_vida, monstro.pontos_vida)
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
        tela_principal.desenhar_vida(capitao.pontos_vida)
        tela_principal.desenhar_ataquepts(capitao.pontos_ataque)
        tela_principal.atualizar_tela()
         
pg.mixer.music.stop()
pg.quit()

### Área de comentários e observações
# Complemento da batalha: Turnos, fuga opcional. Terminar o jogo.
# Criar lógicas dos itens. Talvez uma classe Item, pai de Armas. Itens pelo mapa. Coletar e usar itens. 
# Mostrar os itens e a quantidade de usos da arma.
# Dar descrições para todos os itens e todos os monstros. Ver também o negócio das cartinhas com itens e monstros.

# Mostrar informações dos itens na tela, quando o personagem chegar no vértice. Leozim

# Criar vários objetos do tipo Arma e PlantaMedicinal e espalhar pelos grafos. Como adicionar itens dentro de um vértice.