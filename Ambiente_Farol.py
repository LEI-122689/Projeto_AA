from Interface_Ambiente import Ambiente
from typing import Tuple, Any


class AmbienteFarol(Ambiente):
    # Adicionamos o parâmetro 'mapa_tipo' para definir a dificuldade
    def __init__(self, mapa_tipo="facil"):
        self.size_x = 21
        self.size_y = 11

        self.agente_pos = (0, 0)
        self.farol_x = 10
        self.farol_y = 5

        self.tempo_luz = 0

        # Carrega o mapa com obstáculos
        self.mapa_obstaculos = self._carrega_mapa(mapa_tipo)

    def _carrega_mapa(self, tipo):
        """ Define diferentes níveis de dificuldade através de obstáculos (1=Pedras, 2=Correntes). """

        # O Farol é 3, a água rasa é 0
        mapa_base = [[0] * self.size_x for _ in range(self.size_y)]
        mapa_base[self.farol_y][self.farol_x] = 3

        if tipo == "facil":
            # Sem obstáculos, apenas água rasa
            return mapa_base

        elif tipo == "medio":
            mapa = mapa_base
            # Pedras/Recifes (1): Risco Médio (Recompensa -5)
            for x in range(5, 8): mapa[3][x] = 1
            for y in range(8, 11): mapa[y][15] = 1
            mapa[1][1] = 1
            mapa[9][1] = 1
            return mapa

        elif tipo == "dificil":
            mapa = self._carrega_mapa("medio")
            # Correntes Fortes (2): Alto Risco (Recompensa -10)
            for y in range(1, 10): mapa[y][9] = 2  # Coluna central de correntes perigosa
            mapa[5][1] = 2
            mapa[5][19] = 2
            return mapa

        else:
            raise ValueError("Tipo de mapa desconhecido! Escolha 'facil', 'medio' ou 'dificil'.")

    # --- IMPLEMENTAÇÃO DOS MÉTODOS ABSTRATOS (O que faltava) ---

    def reset(self):
        """ Coloca o agente na posição inicial (0, 0) e reseta o tempo da luz. """
        self.agente_pos = (0, 0)
        self.tempo_luz = 0

    def observacaoPara(self) -> Any:
        """ Devolve o estado (posição relativa do Farol). """
        ax, ay = self.agente_pos
        fx, fy = self.farol_x, self.farol_y
        return (fx - ax, fy - ay)

    def agir(self, accao: Tuple[int, int]) -> float:
        """ Executa a ação e devolve a recompensa baseada no terreno. """
        curr_x, curr_y = self.agente_pos
        dx, dy = accao

        new_x = curr_x + dx
        new_y = curr_y + dy

        # 1. Verificar Limites (Cair ao mar)
        if not (0 <= new_x < self.size_x and 0 <= new_y < self.size_y):
            return -50  # Penalidade severa

        # 2. Ler o Novo Terreno e Mover
        terreno = self.mapa_obstaculos[new_y][new_x]
        self.agente_pos = (new_x, new_y)

        # 3. Atribuir Recompensa
        if terreno == 3:  # Farol (Objetivo)
            return 1000

        elif terreno == 2:  # Correntes Fortes
            return -10

        elif terreno == 1:  # Pedras/Recifes
            return -5

        else:  # 0: Água Rasa (Passo Padrão)
            return -1

    def jogo_terminou(self) -> bool:
        """ Verifica se o agente atingiu o Farol. """
        return self.agente_pos == (self.farol_x, self.farol_y)

    def render(self):
        """ Método de renderização exigido pela interface (implementação no Pygame). """
        pass