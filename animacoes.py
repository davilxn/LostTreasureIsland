import pygame as pg

class Animacao:
    def __init__(self, frames=[], fps=10):
        """
        Inicializa uma instância de Animacao com a lista de frames fornecida e a taxa de frames por segundo (fps) especificada.
         
        Args:
            frames (list): Lista contendo os frames da animação.
            fps (int): Taxa de frames por segundo da animação (padrão é 10).
        """
        self.frames = frames
        self.num_frames = len(frames)
        self.indice_frame = 0
        self.fps = fps
        self.tempo_animacao = pg.time.get_ticks()

    def atualizar(self):
        """
        Calcula a diferença entre o instante atual e o instante em que uma animação foi criada ou atualizada pela últlima vez. Verifica se 
        esse valor de tempo percorrido já ultrapassou um limite arbitrário, que se refere à quantidade de tempo máxima que um frame apareceu
        na tela e, em caso afirmativo, incrementa "indice_frame" para indicar o próximo frame da lista de frames atual da animação.
        """
        tempo_atual = pg.time.get_ticks()
        if tempo_atual - self.tempo_animacao > 1000 / self.fps:
            self.indice_frame = (self.indice_frame + 1) % self.num_frames
            self.tempo_animacao = tempo_atual

    def obter_frame_atual(self):
        """
        Obtém o frame atual com base em "indice_frame" e retorna.
        
        Returns:
            Frame atual da animação.
        """
        frame_atual = self.frames[self.indice_frame]
        return frame_atual
    
    def reiniciar_animacao(self):
        """
        Usado para zerar "indice_frame". Este método foi criado para auxiliar na troca de lista de frames de uma mesma animação, como forma de 
        forçar com que o índice seja zero após a troca, e que a próxima animação (leitura da lista de frames) comece do início.
        """
        self.indice_frame = 0

    def definir_frames(self, novos_frames, est_atual, est_anterior):
        """
        Realiza a troca da lista de frames de uma animação. Ex: Ao se mover entre os vértices da ilha, a lista de frames do Capitão Daleo é
        a lista de frames de corrida. Quando o Capitão chega a um vértice, a lista de frames passa a ser a de parada (idle).
        
        Args:
            novos_frames (list): Nova lista de frames.
            est_atual (str): Estado atual da animação.
            est_anterior (str): Estado anterior da animação.
        """
        if est_atual != est_anterior:
            self.reiniciar_animacao()
        self.frames = novos_frames
        self.num_frames = len(self.frames)