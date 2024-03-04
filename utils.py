import pygame as pg
import numpy as np
from random import sample, choice
import json
from grafo import Vertice
from personagem import Personagem, Criatura, Arma
from animacoes import Animacao

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
               (29,25),(29,31),(29,28),(25,31),(26,28),(26,27),
               (26,23),(26,16)]
    
    for aresta in arestas:
        grafo.adicionar_aresta(grafo.vertices[aresta[0]], grafo.vertices[aresta[1]])
    
    inputGrafo(grafo)

def inputGrafo(grafo):
    vertices_possiveis = list(range(1,31))
    grafo.vertices[0].evento = "praia"
    grafo.vertices[31].evento = "tesouro"
    n = 6
    
    lista_monstros = inicializa_criaturas(grafo)

    perigo = sample(vertices_possiveis, n)
    for num in perigo:
        vertices_possiveis.remove(num)
        if(num % 2 == 0):
            grafo.vertices[num].evento = 'areiaMovedica'
        else:
            grafo.vertices[num].evento = 'florestaPerigosa'
    
    num_checkpoints = sample(vertices_possiveis, 3)
    for num in num_checkpoints:
        vertices_possiveis.remove(num)
        grafo.vertices[num].evento = 'checkpoint'

    num_ajudas = sample(vertices_possiveis, n)
    for num in num_ajudas:
        vertices_possiveis.remove(num)
        if(num % 2 == 0):
            grafo.vertices[num].evento = 'plantaMedicinal'
        else:
            grafo.vertices[num].evento = 'arma'
    
    num_monstros = sample(vertices_possiveis, n)
    for num in num_monstros:
        vertices_possiveis.remove(num)
        grafo.vertices[num].evento = 'monstro'
        
        monstro = choice(lista_monstros)
        monstro.vertice = grafo.vertices[num]
        monstro.animacao.definir_frames(monstro.lista_anim[monstro.estado], monstro.estado, monstro.estado)
        
        grafo.vertices[num].objeto = monstro
    
    for num in vertices_possiveis:
         grafo.vertices[num].evento = 'nada'

# De Animações
def carregar_frames(path_img, num_frames):
    frames = pg.image.load(path_img)
    largura_frame = frames.get_width() // num_frames
    altura_frame = frames.get_height()
    lista_frames = [frames.subsurface((i * largura_frame, 0, largura_frame, altura_frame)) for i in range(num_frames)]
    return lista_frames

def calcular_distancia(x_destino, y_destino, x_inicial, y_inicial):
        difx = x_destino - x_inicial
        dify = y_destino - y_inicial
        return (difx**2 + dify**2)**0.5

def mover_em_linha_reta(personagem, destino, num_frames_animacao = 60):
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
    else:
        personagem.estado = 0

# De personagem
def inicializa_capitao(grafo):
    capitao = Personagem(grafo=grafo)
    arma_inicial = Arma("Lâmina do explorador", "Lâmina modesta e forte, aço leve e punho de couro. Boa para novatos.", capitao.vertice, 10)
    capitao.arma = arma_inicial
    capitao_idle = carregar_frames("images\Idle-5frm.png", 5)
    capitao_caminha = carregar_frames("images\Run-6frm.png", 6)
    capitao_ataca = carregar_frames("images\Atk1-6frm.png", 6)
    capitao_dano = carregar_frames("images\Hit-3frm.png", 3)
    capitao_morre = carregar_frames("images\Death-4frm.png", 4)
    capitao_saca = carregar_frames("images\Gun-Out-6frm.png", 6)
    capitao_guarda = carregar_frames("images\Gun-in-5frm.png", 5)
    
    capitao.lista_anim = [capitao_idle, capitao_caminha, capitao_ataca, capitao_dano, capitao_morre, capitao_saca, capitao_guarda]
    return capitao

def inicializa_criatura(grafo, sprites):
    monstro = Criatura(grafo=grafo)
    monstro_idle = carregar_frames(sprites[0][0], sprites[0][1])
    monstro_ataca = carregar_frames(sprites[0][0], sprites[0][1])
    monstro_dano = carregar_frames(sprites[0][0], sprites[0][1])
    monstro_morre = carregar_frames(sprites[0][0], sprites[0][1])
    
    monstro.lista_anim = [monstro_idle, monstro_ataca, monstro_dano, monstro_morre]
    
    return monstro

def inicializa_criaturas(grafo):
    sprites1 = [("images\dark fantasy big boss idle.png", 16), 
               ("images\dark fantasy big boss attack 2.png", 16), 
               ("images\dark fantasy big boss hit.png", 3), 
               ("images\dark fantasy big boss death.png", 16)]
    
    
    monstro1 = inicializa_criatura(grafo, sprites1)
    monstros = [monstro1]
    return monstros
    

    
    
