import pygame as pg

def carregar_frames(path_img, num_frames):
    frames = pg.image.load(path_img)
    largura_frame = frames.get_width() // num_frames
    altura_frame = frames.get_height()
    lista_frames = [frames.subsurface((i * largura_frame, 0, largura_frame, altura_frame)) for i in range(num_frames)]
    return lista_frames

def calc_distancia(xf, yf, xi, yi):
    difx = xf - xi
    dify = yf - yi
    dist = ((difx**2) + (dify**2))**0.5
    return dist

class Animacao:
    def __init__(self, frames=[], fps=10):
        self.frames = frames
        self.num_frames = len(frames)
        self.indice_frame = 0
        self.fps = fps
        self.tempo_animacao = pg.time.get_ticks()

    def atualizar(self):
        tempo_atual = pg.time.get_ticks()
        if tempo_atual - self.tempo_animacao > 1000 / self.fps:
            self.indice_frame = (self.indice_frame + 1) % self.num_frames
            self.tempo_animacao = tempo_atual

    def obter_frame_atual(self):
        frame_atual = self.frames[self.indice_frame]
        return frame_atual
    
    def reiniciar_animacao(self):
        self._indice_frame = 0

    def definir_frames(self, novos_frames):
        self.frames = novos_frames
        self.num_frames = len(self.frames)
        self.reiniciar_animacao()