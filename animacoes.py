import pygame as pg

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