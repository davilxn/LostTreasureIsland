import pygame as pg
import numpy as np
from random import sample, choice
import json
from grafo import Vertice
from personagem import Personagem, Criatura, Arma, PlantaMedicinal


# Grafo
def inicializa_grafo(grafo, json_path):
    with open(json_path, 'r') as file:
        dados_json = json.load(file)
        
    i = 0
    for dado in dados_json:
        vertice = Vertice(i, x=dado['x'], y=dado['y'], grafo=grafo)
        grafo.adicionar_vertice(vertice)
        i+=1
        
    arestas = [(0,1),(0,2),(0,3),(3,4),(1,5),(2,20),
               (1,6),(4,7),(4,8),(3,9),(8,9),(23,31),
               (5,10),(5,11),(5,12),(6,12),(7,13),(13,20),
               (13,14),(9,15),(12,20),(28,27),(15,16),(15,22),
               (15,23),(14,22),(20,30),(20,21),(20,22),(21,22),
               (21,30),(21,31),(10,25),(10,17),(11,19),(11,17),
               (19,30),(19,18),(19,31),(18,17),(18,24),(24,25),
               (29,25),(29,31),(29,28),(26,28),(26,27),
               (26,23),(26,16)]
    
    for aresta in arestas:
        grafo.adicionar_aresta(grafo.vertices[aresta[0]], grafo.vertices[aresta[1]])
    
    inputGrafo(grafo)

def inputGrafo(grafo):
    vertices_possiveis = list(range(1,31))
    grafo.vertices[0].evento[0] = "praia"
    grafo.vertices[31].evento[0] = "tesouro"
    n = 6
    
    lista_monstros = inicializa_criaturas(grafo)
    lista_armas = inicializa_armas(grafo)
    lista_remedios = inicializa_remedios(grafo)
    lista_perigosa = ["Areia movediça", "Floresta dos sussuros", "Vulcão", "Poço de cobras", "Chuva de cocô dos pombos do Norte", "Pântano do Zé Jacaré"]
    
    num_checkpoints = sample(vertices_possiveis, 3)
    for num in num_checkpoints:
        vertices_possiveis.remove(num)
        grafo.vertices[num].evento.append('checkpoint')

    perigo = sample(vertices_possiveis, n)
    for num in perigo:
        perigo = choice(lista_perigosa)
        grafo.vertices[num].evento.append(perigo)

    num_ajudas = sample(vertices_possiveis, n)
    for num in num_ajudas:
        sorteado = choice([0, 1, 2])
        if sorteado == 0:
            remedio = choice(lista_remedios)
            grafo.vertices[num].objeto.append(remedio)
            grafo.vertices[num].evento.append('plantaMedicinal')
        if sorteado == 1: 
            arma = choice(lista_armas)
            grafo.vertices[num].objeto.append(arma)
            grafo.vertices[num].evento.append('arma')    
        else:
            arma = choice(lista_armas)
            remedio = choice(lista_remedios)
            grafo.vertices[num].objeto.append(arma)
            grafo.vertices[num].evento.append('arma')  
            grafo.vertices[num].objeto.append(remedio)
            grafo.vertices[num].evento.append('plantaMedicinal')
    
    num_monstros = sample(vertices_possiveis, n)
    for num in num_monstros:
        grafo.vertices[num].evento.append('monstro')
        
        monstro = choice(lista_monstros)
        monstro.vertice = num
        monstro.animacao.definir_frames(monstro.lista_anim[monstro.estado], monstro.estado, monstro.estado)
        
        grafo.vertices[num].objeto.append(monstro)
    
    for num in vertices_possiveis:
         grafo.vertices[num].evento.append('nada')

# De Animações
def carregar_frames(path_img, num_frames, espelhar=False, vertical=False):
    frames = pg.image.load(path_img)
    if vertical:
        largura_frame = frames.get_width()
        altura_frame = frames.get_height() // num_frames
    else:
        largura_frame = frames.get_width() // num_frames
        altura_frame = frames.get_height()
    
    lista_frames = []  
        
    for i in range(num_frames):
        if vertical:
            x_frame = 0
            y_frame = i * altura_frame
        else:   
            x_frame = i * largura_frame
            y_frame = 0

        frame_original = frames.subsurface((x_frame, y_frame, largura_frame, altura_frame))

        if espelhar:
            frame_original = pg.transform.flip(frame_original, True, False)

        lista_frames.append(frame_original)

    return lista_frames

def calcular_distancia(x_destino, y_destino, x_inicial, y_inicial):
        difx = x_destino - x_inicial
        dify = y_destino - y_inicial
        return (difx**2 + dify**2)**0.5

def mover_em_linha_reta(personagem, destino, num_frames_animacao = 60):
    estado_anterior = -1
    if calcular_distancia(destino[0], destino[1], personagem.x, personagem.y) > 8:
        dx = destino[0] - personagem.x
        dy = destino[1] - personagem.y
        distancia_total = calcular_distancia(destino[0], destino[1], personagem.x, personagem.y)
        angulo = np.arctan2(dy, dx)

        incremento_x = (distancia_total / num_frames_animacao) * np.cos(angulo)
        incremento_y = (distancia_total / num_frames_animacao) * np.sin(angulo)
        personagem.x += incremento_x
        personagem.y += incremento_y
        
        personagem.estado = 1
        estado_anterior = personagem.estado
    else:
        estado_anterior = personagem.estado
        personagem.estado = 0
        if estado_anterior != personagem.estado:
            personagem.interacao_vertice()
        

# De personagem
def inicializa_capitao(grafo):
    capitao = Personagem(grafo=grafo)
    arma_inicial = Arma("Lâmina do explorador", "Lâmina modesta e forte, aço leve e punho de couro. Boa para novatos.", pontos_ataque=20, vertice=capitao.vertice)
    capitao.equipar_arma(arma_inicial)
    capitao_idle = carregar_frames("images\capitao\Idle-5frm.png", 5, espelhar=False)
    capitao_caminha = carregar_frames("images\capitao\Run-6frm.png", 6, espelhar=False)
    capitao_ataca1 = carregar_frames("images\capitao\Atk1-6frm.png", 6, espelhar=False)
    capitao_ataca2 = carregar_frames("images\capitao\Atk2-6frm.png", 6, espelhar=False)
    capitao_ataca3 = carregar_frames("images\capitao\Atk3-6frm.png", 6, espelhar=False)
    capitao_ataca4 = carregar_frames("images\capitao\Gun-Shoot-5frm.png", 5, espelhar=False)
    capitao_dano = carregar_frames("images\capitao\Hit-3frm.png", 3, espelhar=False)
    capitao_morre = carregar_frames("images\capitao\Death-4frm.png", 4, espelhar=False)
    
    capitao.lista_anim = [capitao_idle, capitao_caminha, capitao_ataca1, capitao_ataca2, capitao_ataca3, capitao_ataca4, capitao_dano, capitao_morre]
    return capitao

def inicializa_criatura(grafo, sprites, espelhar, vertical=False, x_luta=0, y_luta=0):
    monstro = Criatura(grafo=grafo)
    monstro.x_luta, monstro.y_luta = x_luta, y_luta
    monstro_idle = carregar_frames(sprites[0][0], sprites[0][1], espelhar=espelhar, vertical=vertical)
    monstro_ataca = carregar_frames(sprites[1][0], sprites[1][1], espelhar=espelhar, vertical=vertical)
    monstro_dano = carregar_frames(sprites[2][0], sprites[2][1], espelhar=espelhar, vertical=vertical)
    monstro_morre = carregar_frames(sprites[3][0], sprites[3][1], espelhar = espelhar, vertical=vertical)
    
    monstro.lista_anim = [monstro_idle, monstro_ataca, monstro_dano, monstro_morre]
    
    return monstro
        

def inicializa_criaturas(grafo):
    sprites1 = [("images\monstros\lobo\idle_6frm.png", 6), 
               ("images\monstros\lobo\lobattack_5frm.png", 5), 
               ("images\monstros\lobo\hit_4frm.png", 4), 
               ("images\monstros\lobo\death_7frm.png", 7)]
    
    sprites2 = [("images\monstros\oscar\dark fantasy big boss idle_16frm.png", 16), 
               ("images\monstros\oscar\dark fantasy big boss attack 2_16frm.png", 16), 
               ("images\monstros\oscar\dark fantasy big boss hit_3frm.png", 3), 
               ("images\monstros\oscar\dark fantasy big boss death_16frm.png", 16)]
    
    sprites3 = [("images\monstros\sapovski\Toad_Idle_4frm.png", 4), 
               ("images\monstros\sapovski\Toad_Attack_8frm.png", 8), 
               ("images\monstros\sapovski\Toad_Damage_3frm.png", 3), 
               ("images\monstros\sapovski\Toad_Death_5frm.png", 5)]
    
    sprites4 = [("images\monstros\dona_morte\idle_7frm.png", 7), 
               ("images\monstros\dona_morte\morteataque_4frm.png", 4), 
               ("images\monstros\dona_morte\hit_6frm.png", 6), 
               ("images\monstros\dona_morte\morte_6frm.png", 6)]

    sprites5 = [("images\monstros\magrelo\Skeleton Idle.png", 11), 
               ("images\monstros\magrelo\Skeleton Attack.png", 18), 
               ("images\monstros\magrelo\Skeleton Hit.png", 8), 
               ("images\monstros\magrelo\Skeleton Dead.png", 15)]
    
    sprites6 = [("images\monstros\sprout\Sprout_idle.png", 4), 
               ("images\monstros\sprout\Sprout_attack.png", 6), 
               ("images\monstros\sprout\Sprout-damage.png", 5), 
               ("images\monstros\sprout\Sprout-death.png", 8)]
    
    sprites7 = [("images\monstros\master_magrelo\SL_idle.png", 4), 
               ("images\monstros\master_magrelo\SL_attack_1.png", 8), 
               ("images\monstros\master_magrelo\SL_damage.png", 4), 
               ("images\monstros\master_magrelo\SL_death.png", 8)]
    
    sprites8 = [("images\monstros\seeker\skeleton_seeker_idle.png", 6), 
               ("images\monstros\seeker\skeleton_skeleton_attack.png", 10), 
               ("images\monstros\seeker\skeleton_seeker_damage.png", 4), 
               ("images\monstros\seeker\skeleton_seeker_death.png", 5)]
    
    sprites9 = [("images\monstros\old_golem\Old_Golem_idle.png", 6), 
               ("images\monstros\old_golem\Old_Golem_attack2.png", 8), 
               ("images\monstros\old_golem\Old_Golem_hit.png", 4), 
               ("images\monstros\old_golem\Old_Golem_death.png", 10)]
    
    sprites10 = [("images\monstros\old_guardian\Old_Guardian_idle.png", 6), 
               ("images\monstros\old_guardian\Old_Guardian_attack_1.png", 10), 
               ("images\monstros\old_guardian\Old_Guardian_hit.png", 4), 
               ("images\monstros\old_guardian\Old_Guardian_death.png", 10)]
    
    
    # Opções extra
    jacob = inicializa_criatura(grafo, sprites1, False)
    oscar = inicializa_criatura(grafo, sprites2, True)
    sapovski = inicializa_criatura(grafo, sprites3, True)
    dona_morte = inicializa_criatura(grafo, sprites4, False, x_luta=350, y_luta=155)
    magrelo = inicializa_criatura(grafo, sprites5, True)
    
    # Monstros
    mr_eucalipto = inicializa_criatura(grafo, sprites6, True, True, x_luta=350, y_luta=145)
    master_magrelo = inicializa_criatura(grafo, sprites7, True, True, x_luta=350, y_luta=85)
    hidra_magrela = inicializa_criatura(grafo, sprites8, True, True, x_luta=350, y_luta=120)
    lagartixolem = inicializa_criatura(grafo, sprites9, False, True, x_luta=350, y_luta=100)
    barata_militar = inicializa_criatura(grafo, sprites10, True, True, x_luta=350, y_luta=135)
    
    monstros = [dona_morte, mr_eucalipto, master_magrelo, hidra_magrela, lagartixolem, barata_militar]
    return monstros

def inicializa_armas(grafo):
    descricao = "Uma espada lendária que brilha com poder místico. Dizem que corta através do destino dos inimigos."
    arma1 = Arma("Espada do Destino", descricao, pontos_ataque=30)
    
    descricao = "Uma lâmina afiada forjada nas profundezas do vulcão, capaz de cortar através das escamas mais resistentes."
    arma2 = Arma("Lâmina do Dragão", descricao, pontos_ataque=28)
    
    descricao = "Forjada com aço puro e adornada com símbolos sagrados, esta espada é o símbolo da justiça implacável."
    arma3 = Arma("Espada da Justiça", descricao, pontos_ataque=25)
    
    descricao = "Uma katana elegante, envolta em sombras misteriosas. Seu golpe corta como uma lâmina afiada no crepúsculo."
    arma4 = Arma("Katana do Crepúsculo", descricao, pontos_ataque=23)
    
    descricao = "Um revólver robusto com um cabo de madeira polida. Foi a arma de escolha de muitos fora da lei."
    arma5 = Arma("Desesperado", descricao, pontos_ataque=35)
    
    descricao = "Uma pistola de precisão mítica com insígnias de justiça gravadas em seu cano. Seus tiros nunca erram o alvo."
    arma6 = Arma("Justiceiro", descricao, pontos_ataque=32)
    
    descricao = "Um revólver sombrio como a noite, que sussurra promessas de morte ao disparar balas envenenadas."
    arma7 = Arma("Morte Súbita", descricao, pontos_ataque=34)
    
    descricao = "Um revólver de aparência simples, mas com uma história de ressurgimento, sempre encontrando seu caminho de volta para as mãos de seu verdadeiro dono."
    arma8 = Arma("Ressurgente", descricao, pontos_ataque=31)
    
    lista_armas = [arma1, arma2, arma3, arma4, arma5, arma6, arma7, arma8]
    
    return lista_armas

def inicializa_remedios(grafo):
    descricao = "Uma folha verde exuberante encontrada apenas nas profundezas da selva da ilha, conhecida por suas propriedades curativas naturais."
    med1 = PlantaMedicinal("Folha de Cura Tropical", descricao, pontos_vida=12)
    
    descricao = "Uma fruta suculenta e colorida encontrada pendurada nos galhos das árvores frondosas da ilha, conhecida por rejuvenescer os que a consomem."
    med2 = PlantaMedicinal("Fruta da Vitalidade", descricao, pontos_vida=15)
    
    descricao = "Um tônico preparado com raízes selvagens colhidas nas profundezas da ilha, que proporciona um impulso de energia instantâneo e revitaliza o corpo."
    med3 = PlantaMedicinal("Tônico de Raízes Selvagens", descricao, pontos_vida=18)
    
    descricao = "Uma flor delicada e perfumada que floresce apenas em certos recantos secretos da ilha, conhecida por suas propriedades calmantes e de cura."
    med4 = PlantaMedicinal("Flor da Serenidade", descricao, pontos_vida=21)
    
    descricao = "Um extrato concentrado obtido dos cactos que prosperam sob o sol escaldante da ilha, com propriedades que revigoram e restauram a vitalidade."
    med5 = PlantaMedicinal("Extrato de Cacto Solar", descricao, pontos_vida=24)
    
    descricao = "Uma bebida doce e refrescante feita com o néctar das flores exóticas que enfeitam a paisagem da ilha, conhecida por seu poder de cura instantâneo."
    med6 = PlantaMedicinal("Bebida de Néctar Floral", descricao, pontos_vida=27)
    
    descricao = "Um bálsamo feito com as lágrimas cristalinas das sereias que habitam as águas ao redor da ilha, com propriedades curativas lendárias."
    med7 = PlantaMedicinal("Bálsamo de Lágrimas de Sereia", descricao, pontos_vida=30)
    
    descricao = "Enquanto o derivado dos temidos Pombos do Norte o atingem como granizo ácido em tempestades mortais, este o impacta com a maciez da chuva leve e o calor suave do verão sereno."
    med8 = PlantaMedicinal("Cocô dos Pombos do Sul", descricao, pontos_vida=50)
    
    lista_meds = [med1, med2, med3, med4, med5, med6, med7, med8]
    return lista_meds
    

    
    
    
