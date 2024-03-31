from grafo import Grafo
from interface import Tela
from random import choice, randint
from personagem import Criatura, Arma, PlantaMedicinal
import pygame as pg
from utils import inicializa_grafo, mover_em_linha_reta, inicializa_capitao

# Definindo função de sobreposição de mensagem
def sobreMens():
    # Limpa e atualiza a tela
        tela_principal.limpar_tela()
        tela_principal.desenhar_elemento(tela_principal.imagem_fundo, (0,0))
        tela_principal.desenhar_elemento(capitao.animacao.obter_frame_atual(), (capitao.x, capitao.y))
        tela_principal.desenhar_vida(capitao.pontos_vida,1028,15)
        tela_principal.desenhar_coracao(capitao.vidas_restantes)
        tela_principal.desenhar_arma(capitao.arma.imagem,capitao.arma.usos_restantes)
        tela_principal.desenhar_expedicao_tempo(capitao.expedicao)
        tela_principal.desenhar_tesouro(capitao.tesouro)
        tela_principal.desenhar_ataquepts(capitao.pontos_ataque,900,15)
        tela_principal.atualizar_tela()

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
estado_luta = choice([2, 3, 4])
turno, turno_anterior = 0, 0

# Loop principal
while executando:
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            executando = False
        
        elif evento.type == pg.MOUSEBUTTONDOWN:
            capitao.mover()
        elif evento.type == pg.KEYDOWN:
            if evento.key == pg.K_SPACE:
                capitao.desequipar_arma()
                print("Você desequipou sua arma atual.")
    
    if capitao.encontrou_tesouro:
        mensagem = f"Parabéns, você encontrou o tesouro! Poderá desfrutar da sua conquista, mas antes, volte para o navio."
        tela_principal.exibir_mensagem(mensagem, (200, 350))
        tela_principal.desenhar_elemento(pg.transform.scale(pg.image.load("images\GUI\Bau do Tesouro.png"),(80,80)), (210,420))
        tela_principal.atualizar_tela()
        pg.time.delay(5000)

        capitao.encontrou_tesouro = False

        sobreMens()

    if capitao.em_checkpoint:
        mensagem = "Você alcançou um checkpoint. Descanse, aprecie a vista e prepare-se."
        tela_principal.exibir_mensagem(mensagem, (200, 350))
        tela_principal.desenhar_elemento(pg.transform.scale(pg.image.load("images\GUI\Sombra e Água Fresca.png"),(80,80)), (210,420))
        tela_principal.atualizar_tela()
        pg.time.delay(3500)

        capitao.em_checkpoint = False

        sobreMens()


    # Capitão achou um perigo
    if capitao.em_perigo != None:
        perigo = capitao.em_perigo
        mensagem = ''
        if perigo == "Areia movediça":
            mensagem += "Você caiu numa área de areia movediça e lutou pra escapar. Cuidado, Indiana Jones. "
        if perigo == "Floresta dos sussuros":
            mensagem += "Você encontrou a Floresta dos Sussurros. Diz a lenda que aqui, o vento carrega vozes que enlouquecem até os mais bravos aventureiros. "
        if perigo == "Vulcão":
            mensagem += "Não sou o bola de fogo, mas o calor tá de matar. Você encontrou um vulcão em erupção, e não conseguiu correr antes de conseguir umas queimaduras. "
        if perigo == "Poço de cobras":
            mensagem += "'Tem uma cobra na minha bota.' Você encontrou um poço de cobras, e foi picado, cowboy. "
        if perigo == "Chuva de cocô dos pombos do Norte":
            mensagem += "Dos perigos desta ilha, o mais mortal: Você foi atingido por cocô do Pombos do Norte. Estes infames destroem tudo o que vêem, sem piedade ou remorso. "
        if perigo == "Pântano do Zé Jacaré":   
            mensagem += "Bem-vindo a um dos Pântanos do Zé Jacaré, um jacaré com coração de lagartixa e muita fome. Você atravessou, mas quase virou petisco. "
            
        dano = randint(1, 10)
        capitao.receber_dano(dano)
        mensagem += f"Você perdeu {dano} pontos de vida."
        tela_principal.exibir_mensagem(mensagem, (200, 350))
        tela_principal.desenhar_elemento(pg.transform.scale(pg.image.load("images\GUI\Perigo.png"),(80,80)), (210,420))
        tela_principal.atualizar_tela()
        pg.time.delay(10000)

        capitao.em_perigo = None

        sobreMens()

    if capitao.em_termino_exploracao != None:
        mensagem = capitao.em_termino_exploracao
        tela_principal.exibir_mensagem(mensagem, (200, 350))
        tela_principal.desenhar_elemento(pg.transform.scale(pg.image.load("images\GUI\jogo termina.png"),(80,80)), (210,420))
        tela_principal.atualizar_tela()
        pg.time.delay(5000)

        capitao.em_termino_exploracao = None

        capitao.fim_de_jogo()

    if capitao.em_morte:
        mensagem = f"Você morreu. Tente novamente, aventureiro."
        tela_principal.exibir_mensagem(mensagem, (200, 350))
        tela_principal.desenhar_elemento(pg.transform.scale(pg.image.load("images\GUI\jogo termina.png"),(80,80)), (210,420))
        tela_principal.atualizar_tela()
        pg.time.delay(5000)

        capitao.em_morte = False

        sobreMens()

    if capitao.arma_nova:
        arma = [obj for obj in capitao.grafo.vertices[capitao.vertice].objeto if isinstance(obj, Arma)]
        mensagem = f"Que sorte! Você encontrou: {arma[0].nome}. {arma[0].descricao}. Deseja trocar de arma ou manter a arma atual?"
        tela_principal.exibir_mensagem(mensagem, (200, 350))
        tela_principal.desenhar_botao("Manter", (50, 400))
        tela_principal.desenhar_botao("Trocar", (250, 400))
        tela_principal.atualizar_tela()

        decisao_jogador = tela_principal.aguardar_clique_botao((50+60, 200+80, 400+80, 450+60), (250+60, 400+80, 400+80, 450+60), "Manter", "Trocar")
        if decisao_jogador == "Trocar":
            capitao.equipar_arma(arma[0])
        if capitao.arma.nome in ["Desesperado", "Justiceiro", "Morte Súbita", "Ressurgente"]:
                estado_luta = 5
        else:
            estado_luta = choice([2,3,4])
            
        capitao.arma_nova = False
        decisao_jogador = None
        
        sobreMens()


    if capitao.planta:
        planta = [obj for obj in capitao.grafo.vertices[capitao.vertice].objeto if isinstance(obj, PlantaMedicinal)]
        mensagem = f"Que sorte! Você encontrou: {planta[0].nome}.\n{planta[0].descricao}"
        if capitao.pontos_vida < 100:
            capitao.pontos_vida += planta[0].pontos_vida
            if capitao.pontos_vida > 100:
                capitao.pontos_vida = 100
                mensagem += "Você utilizou utilizou como remédio para fazer um curativo e sua vida foi regenerada!"
            else:
                mensagem += "No entanto, não lhe não lhe servirá de nada, pois você já está bem de vida. Sombra e água fresca."
        
        tela_principal.exibir_mensagem(mensagem, (200, 350))
        tela_principal.desenhar_elemento(pg.transform.scale(pg.image.load(planta[0].imagem),(80,80)), (210,420))
        tela_principal.atualizar_tela()
        pg.time.delay(5000)

        capitao.planta = False
        
        sobreMens()
        
          
    if capitao.em_batalha and not batalha:
        mensagem = "Você encontrou um monstro sedento por sangue e destruição! O que deseja fazer?"
        tela_principal.exibir_mensagem(mensagem, (200, 350))
        tela_principal.desenhar_botao("Lutar", (50, 400))
        tela_principal.desenhar_botao("Fugir", (250, 400))
        tela_principal.atualizar_tela()

        decisao_jogador = tela_principal.aguardar_clique_botao((50+60, 200+80, 400+80, 450+60), (250+60, 400+80, 400+80, 450+60), "Lutar", "Fugir")
        
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
            capitao.animacao.atualizar()
            monstro.animacao.atualizar()
            turno_anterior = turno
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
                    capitao.arma.uso()
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
                    capitao.arma.uso()
                    tela_principal = Tela(1200, 700, "LostTreasureIsland")
                    tela_principal.definir_imagem_fundo("images\PNG map.jpg")
            
            
            ### Decida se quer continuar lutanto ou fugir
            if turno_anterior != turno:
                mensagem = "Você pode continuar lutando ou fugir para viver e lutar mais um dia."
                tela_luta.exibir_mensagem(mensagem, (50, 140),red=True)
                tela_luta.desenhar_botao("Lutar", (100-60, 165-80))
                tela_luta.desenhar_botao("Fugir", (400-60, 165-80))
                tela_luta.atualizar_tela()

                decisao_jogador = tela_luta.aguardar_clique_botao((100, 350, 165, 215), (400, 550, 165, 215), "Lutar", "Fugir"  )
                
                if decisao_jogador == "Lutar":
                    pass
                        
                elif decisao_jogador == "Fugir":
                    # Com o capitão
                    monstro = None
                    for objeto in capitao.grafo.vertices[capitao.vertice].objeto:
                        if isinstance(objeto, Criatura):
                            monstro = objeto
                    dano = monstro.pontos_ataque
                    capitao.receber_dano(dano)
                    if capitao.pontos_vida == 0:
                        capitao.morte()
                        
                    capitao.em_batalha = False
                    batalha = False
                    turno_monstro, turno_capitao, vez = False, False, False
                    ctrl_anim = 0
                    capitao.arma.uso()
                    tela_principal = Tela(1200, 700, "LostTreasureIsland")
                    tela_principal.definir_imagem_fundo("images\PNG map.jpg")
                    
                    # Com a tela
                    tela_principal.limpar_tela()
                    tela_principal.desenhar_elemento(tela_principal.imagem_fundo, (0,0))
                    mensagem = f"Você fugiu da criatura, mas antes que conseguisse, foi atingido com um golpe raspão. Perdeu {dano} pontos de vida."
                    tela_principal.exibir_mensagem(mensagem, (200, 350))
                    tela_principal.atualizar_tela()
                    #pg.time.delay(5000)
                    
                    capitao.mover()
                    
                decisao_jogador = None
        
        tela_luta.desenhar_elemento(tela_luta.imagem_fundo, (0, 0))
        tela_luta.desenhar_elemento(capitao.animacao.obter_frame_atual(), (75, 100))
        tela_luta.desenhar_elemento(monstro.animacao.obter_frame_atual(), (monstro.x_luta, monstro.y_luta))
        tela_luta.desenhar_vida(capitao.pontos_vida,100,15)
        tela_luta.desenhar_vida(monstro.pontos_vida,350,15,verde=(255, 0, 0))
        tela_luta.desenhar_ataquepts(capitao.pontos_ataque,15,15)
        tela_luta.atualizar_tela()
        
    else: # Lógica Capitão correndo no mapa
        capitao.animacao.atualizar()
        estado_anterior = capitao.estado

        destino = (capitao.grafo.vertices[capitao.vertice].x-123, capitao.grafo.vertices[capitao.vertice].y-123)
        mover_em_linha_reta(capitao, destino)

        capitao.animacao.definir_frames(capitao.lista_anim[capitao.estado], capitao.estado, estado_anterior)

        tela_principal.limpar_tela()
        tela_principal.desenhar_elemento(tela_principal.imagem_fundo, (0,0))
        tela_principal.desenhar_elemento(capitao.animacao.obter_frame_atual(), (capitao.x, capitao.y))
        tela_principal.desenhar_vida(capitao.pontos_vida,1028,15)
        tela_principal.desenhar_coracao(capitao.vidas_restantes)
        tela_principal.desenhar_arma(capitao.arma.imagem,capitao.arma.usos_restantes)
        tela_principal.desenhar_expedicao_tempo(capitao.expedicao)
        tela_principal.desenhar_tesouro(capitao.tesouro)
        tela_principal.desenhar_ataquepts(capitao.pontos_ataque,900,15)
        tela_principal.atualizar_tela()
         
pg.mixer.music.stop()
pg.quit()

### Área de comentários e observações

