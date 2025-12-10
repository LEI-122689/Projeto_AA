from Interface_Ambiente import Ambiente
from typing import List, Tuple


# --- Classes Auxiliares ---

class Parede:
    def __init__(self, x, y):
        self.name = "Parede"
        self.x = x
        self.y = y


class Vazio:
    def __init__(self, x, y):
        self.name = "Vazio"
        self.x = x
        self.y = y


class Objetivo:
    def __init__(self, x, y):
        self.name = "Saida"
        self.x = x
        self.y = y


# --- Classe Principal ---

class AmbienteLabirinto(Ambiente):
    # 1. MAPA FÁCIL (10x10)
    MAPA_FACIL = [
        [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
        [1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 1, 0, 1, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 2]  # Saída no canto
    ]

    # 2. MAPA MÉDIO (15x15) - O TEU ORIGINAL
    MAPA_MEDIO = [
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1],
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
        [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2]
    ]

    # 3. MAPA DIFÍCIL (20x20)
    MAPA_DIFICIL = [
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 2]
    ]

    def __init__(self, dificuldade="medio"):
        # Seleciona o mapa com base na dificuldade
        if dificuldade == "facil":
            self.mapa_atual = self.MAPA_FACIL
        elif dificuldade == "dificil":
            self.mapa_atual = self.MAPA_DIFICIL
        else:
            self.mapa_atual = self.MAPA_MEDIO  # Padrão

        # O tamanho é definido automaticamente pelo mapa escolhido
        self.size = len(self.mapa_atual)

        self.agente_pos = (0, 0)
        self.objetivo = None
        self.paredes = []

        # Gerar Paredes e Objetivo
        self._gerar_paredes_do_mapa(self.mapa_atual)

    def _gerar_paredes_do_mapa(self, mapa_data: List[List[int]]):
        self.paredes = []
        posicao_objetivo = None

        for y in range(self.size):
            for x in range(self.size):
                valor = mapa_data[y][x]

                if valor == 1:
                    self.paredes.append(Parede(x, y))
                elif valor == 2:
                    posicao_objetivo = (x, y)

        self.agente_pos = (0, 0)

        if posicao_objetivo is not None:
            self.objetivo = Objetivo(posicao_objetivo[0], posicao_objetivo[1])
        else:
            # Se não houver '2' no mapa, assume o canto inferior direito
            self.objetivo = Objetivo(self.size - 1, self.size - 1)

        # Garante que o inicio não é parede
        if self.get_coisa_em(0, 0).name == "Parede":
            self.paredes = [p for p in self.paredes if (p.x, p.y) != (0, 0)]

    def reset(self):
        self.agente_pos = (0, 0)

    def get_coisa_em(self, x, y):
        if (self.objetivo.x, self.objetivo.y) == (x, y):
            return self.objetivo
        for p in self.paredes:
            if (p.x, p.y) == (x, y):
                return p
        return Vazio(x, y)

    def observacaoPara(self):
        return self.agente_pos

    def agir(self, accao: Tuple[int, int]) -> float:
        curr_x, curr_y = self.agente_pos
        dx, dy = accao
        new_x, new_y = curr_x + dx, curr_y + dy

        if not (0 <= new_x < self.size and 0 <= new_y < self.size):
            return -10  # Penalidade Limite

        coisa = self.get_coisa_em(new_x, new_y)

        if isinstance(coisa, Parede):
            return -5  # Penalidade Parede

        self.agente_pos = (new_x, new_y)

        if isinstance(coisa, Objetivo):
            return 100  # Objetivo

        return -1  # Custo Passo

    def jogo_terminou(self) -> bool:
        return self.agente_pos == (self.objetivo.x, self.objetivo.y)

    def render(self):
        pass