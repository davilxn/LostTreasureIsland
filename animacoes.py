import pygame as pg
def carregar_frames(path_anim, num_frames):
    frames = pg.image.load(path_anim)
    largura_frame = frames.get_width() // num_frames
    altura_frame = frames.get_height()
    lista_frames = [frames.subsurface((i * largura_frame, 0, largura_frame, altura_frame)) for i in range(num_frames)]
    return lista_frames

class Animacao:
    def __init__(self, frames, fps=10):
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