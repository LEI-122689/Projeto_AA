import random
from Interface_Agente import Agente
from typing import Tuple, Any

# --- Parâmetros (Ajustados para aprender sem "batota") ---
ALPHA = 0.3  # Aprende rápido com os erros (bater nas paredes)
GAMMA = 0.95  # Valoriza muito o futuro (encontrar a saída)
EPSILON_START = 1.0
EPSILON_DECAY = 0.9995
MIN_EPSILON = 0.01

ACOES = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # N, S, O, E

DIRECOES_MAP = {
    (0, -1): "N", (1, -1): "NE", (1, 0): "E", (1, 1): "SE",
    (0, 1): "S", (-1, 1): "SW", (-1, 0): "W", (-1, -1): "NW"
}


class AgenteFarol(Agente):
    def __init__(self):
        self.recompensa_acumulada = 0
        self.q_table = {}
        self.learning_mode = True

        self.estado_anterior = None
        self.acao_anterior = None
        self.estado_atual = None
        self.epsilon = EPSILON_START

        self.alpha = ALPHA
        self.gamma = GAMMA

    def atualiza_posicao(self, nova_pos):
        pass

    def _converte_vetor_para_estado(self, obs_completa) -> str:
        # Recebe ((dx, dy), (n, s, w, e))
        vetor, obstaculos = obs_completa

        # 1. Direção do Objetivo
        estado_dir = "SEM_SINAL"
        if vetor is not None:
            dx, dy = vetor
            norm_x = 0
            if dx > 0:
                norm_x = 1
            elif dx < 0:
                norm_x = -1

            norm_y = 0
            if dy > 0:
                norm_y = 1
            elif dy < 0:
                norm_y = -1

            if (norm_x, norm_y) == (0, 0):
                estado_dir = "FAROL"
            else:
                estado_dir = DIRECOES_MAP.get((norm_x, norm_y), "UNKNOWN")

        # 2. Obstáculos (0 ou 1 nas 4 direções)
        str_obstaculos = "".join(str(b) for b in obstaculos)

        # Estado Exemplo: "N_0100" (Objetivo a Norte, Parede a Sul)
        return f"{estado_dir}_{str_obstaculos}"

    def _get_q_valores(self, estado: str) -> dict:
        if estado not in self.q_table:
            # Inicializamos a zeros. O agente terá de descobrir sozinho.
            self.q_table[estado] = {acao: 0.0 for acao in ACOES}
        return self.q_table[estado]

    def _escolhe_melhor_acao(self, estado: str) -> Tuple[int, int]:
        q_valores = self._get_q_valores(estado)
        max_q = max(q_valores.values())
        melhores_acoes = [acao for acao, q in q_valores.items() if q == max_q]
        return random.choice(melhores_acoes)

    def observacao(self, obs: Any):
        self.estado_atual = self._converte_vetor_para_estado(obs)

    def age(self) -> Tuple[int, int]:
        self.estado_anterior = self.estado_atual

        # LÓGICA PURA: Epsilon-Greedy
        # Sem "If sensor override". O agente decide com base no que aprendeu.
        if self.learning_mode and random.random() < self.epsilon:
            acao = random.choice(ACOES)
        else:
            acao = self._escolhe_melhor_acao(self.estado_atual)

        self.acao_anterior = acao
        return acao

    def avaliacaoEstadoAtual(self, recompensa: float):
        self.recompensa_acumulada += recompensa

        if self.learning_mode and self.estado_anterior is not None and self.acao_anterior is not None:
            s = self.estado_anterior
            a = self.acao_anterior
            r = recompensa
            s_prime = self.estado_atual

            q_s = self._get_q_valores(s)

            if s_prime.startswith("FAROL"):
                max_q_prime = 0.0
            else:
                q_s_prime = self._get_q_valores(s_prime)
                max_q_prime = max(q_s_prime.values())

            q_atual = q_s[a]
            novo_q = (1 - self.alpha) * q_atual + self.alpha * (r + self.gamma * max_q_prime)
            q_s[a] = novo_q

            if self.epsilon > MIN_EPSILON:
                self.epsilon *= EPSILON_DECAY