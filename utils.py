import pygame as pg
import numpy as np

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
    if calcular_distancia(destino[0], destino[1], personagem.x, personagem.y) > 5:
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
        pass
    
    
