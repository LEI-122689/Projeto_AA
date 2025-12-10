from Interface_Ambiente import Ambiente
from typing import List, Tuple, Any


# --- Classes Auxiliares (Elementos do Ambiente) ---

class Parede:
    """ Representa um bloco que bloqueia o movimento. """

    def __init__(self, x, y):
        self.name = "Parede"
        self.x = x
        self.y = y


class Vazio:
    """ Representa um bloco de caminho aberto. """

    def __init__(self, x, y):
        self.name = "Vazio"
        self.x = x
        self.y = y


class Objetivo:
    """ Representa o bloco de saída/meta. """

    def __init__(self, x, y):
        self.name = "Saida"
        self.x = x
        self.y = y


# --- Classe Principal: AmbienteLabirinto ---

class AmbienteLabirinto(Ambiente):
    # Convenção: 0: Vazio, 1: Parede, 2:
    MAPA_PADRAO_15X15_EXEMPLO = [
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
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]  #(Objetivo em 14,14)
    ]

    def __init__(self, mapa_data: List[List[int]] = None):
        self.size = 15  # Tamanho padrão
        self.agente_pos = (0, 0)  # Posição inicial FIXA
        self.objetivo = None
        self.paredes = []

        if mapa_data is None:
            mapa_data = self.MAPA_PADRAO_15X15_EXEMPLO

        # Gerar Paredes e encontrar o Objetivo a partir dos dados do mapa
        self._gerar_paredes_do_mapa(mapa_data)

    def _gerar_paredes_do_mapa(self, mapa_data: List[List[int]]):
        """
        Gera a lista self.paredes e define o objetivo (2).
        A Posição de Início é FIXA em (0, 0).
        Convenção: 0: Vazio, 1: Parede, 2: Objetivo, -1: Ignorado.
        """
        if len(mapa_data) != self.size or len(mapa_data[0]) != self.size:
            raise ValueError(f"O mapa deve ser {self.size}x{self.size}.")

        self.paredes = []
        posicao_objetivo = None

        # 1. Percorrer o mapa para identificar Paredes e Objetivo
        for y in range(self.size):
            for x in range(self.size):
                valor = mapa_data[y][x]

                if valor == 1:
                    self.paredes.append(Parede(x, y))
                elif valor == 2:
                    if posicao_objetivo:
                        print("Aviso: Múltiplos Objetivos (2) encontrados.")
                    posicao_objetivo = (x, y)

        # 2. Definir Posição e Objetivo

        # Posição inicial FIXA em (0, 0)
        self.agente_pos = (0, 0)

        # Define a posição do Objetivo
        if posicao_objetivo is not None:
            self.objetivo = Objetivo(posicao_objetivo[0], posicao_objetivo[1])
        else:
            self.objetivo = Objetivo(self.size - 1, self.size - 1)
            print(
                f"Aviso: Objetivo (2) não encontrado. Assumindo a posição padrão ({self.objetivo.x}, {self.objetivo.y}).")

        # 3. VERIFICAÇÃO CRÍTICA: Garantir que (0, 0) não é uma parede

        # Se (0, 0) foi definido como parede, removemos essa parede para garantir o início
        if self.get_coisa_em(0, 0).name == "Parede":
            self.paredes = [p for p in self.paredes if (p.x, p.y) != (0, 0)]
            print("Aviso: (0, 0) era uma parede e foi removida para garantir o início.")

    # --- Métodos de Interação com o Ambiente ---

    def reset(self):
        """ Reseta a posição do agente para a posição inicial FIXA em (0, 0). """
        self.agente_pos = (0, 0)

    def get_coisa_em(self, x, y):
        """ Retorna o objeto (Objetivo, Parede, Vazio) numa dada coordenada. """
        if (self.objetivo.x, self.objetivo.y) == (x, y):
            return self.objetivo
        for p in self.paredes:
            if (p.x, p.y) == (x, y):
                return p
        return Vazio(x, y)

    def observacaoPara(self):
        """ A observação é a posição atual do agente (estado 's'). """
        return self.agente_pos

    def agir(self, accao: Tuple[int, int]) -> float:
        """
        Move o agente de acordo com a ação (dx, dy) e devolve a recompensa.
        Recompensas: +100 (Objetivo), -5 (Parede), -10 (Limite), -1 (Passo).
        """
        curr_x, curr_y = self.agente_pos
        dx, dy = accao
        new_x, new_y = curr_x + dx, curr_y + dy

        # 1. Verificar Limites
        if not (0 <= new_x < self.size and 0 <= new_y < self.size):
            return -10  # Penalidade por sair do mapa

        coisa = self.get_coisa_em(new_x, new_y)

        # 2. Verificar Parede
        if isinstance(coisa, Parede):
            return -5  # Penalidade por bater na parede (não move o agente)

        # 3. Mover o Agente
        self.agente_pos = (new_x, new_y)

        # 4. Verificar Objetivo
        if isinstance(coisa, Objetivo):
            return 100  # Recompensa por atingir o objetivo

        # 5. Passo Normal
        return -1  # Custo por cada passo

    def jogo_terminou(self) -> bool:
        """ Verifica se o agente está na posição do objetivo. """
        return self.agente_pos == (self.objetivo.x, self.objetivo.y)

    def render(self):
        """ Método exigido pela interface (implementação visual no Pygame_Simulador). """
        pass