import random
from Interface_Agente import Agente
# --- Parâmetros de Q-Learning ---
ALPHA = 0.1  # Taxa de Aprendizagem
GAMMA = 0.9  # Fator de Desconto
EPSILON_START = 1.0  # Probabilidade inicial de exploração (100%)
EPSILON_DECAY = 0.9999  # Fator de decaimento do epsilon por passo
MIN_EPSILON = 0.01  # Mínimo de exploração

# Ações possíveis: (dx, dy)
ACOES = [(0, -1), (0, 1), (-1, 0), (1, 0)]

# Mapa das 8 direções para discretização do Estado (S)
DIRECOES_MAP = {
    (0, -1): "N", (1, -1): "NE", (1, 0): "E", (1, 1): "SE",
    (0, 1): "S", (-1, 1): "SW", (-1, 0): "W", (-1, -1): "NW"
}


class AgenteFarol:
    def __init__(self):
        self.recompensa_acumulada = 0
        self.q_table = {}  # Tabela Q: Estado (Direção) -> {acao: valor_q}
        self.learning_mode = True

        # Variáveis de Estado e Ação
        self.estado_anterior = None
        self.acao_anterior = None
        self.ultima_observacao = None
        self.estado_atual = None  # A direção discretizada
        self.epsilon = EPSILON_START

        # Parâmetros de RL
        self.alpha = ALPHA
        self.gamma = GAMMA

    # --- Métodos de Suporte para Q-Learning ---

    def _converte_vetor_para_estado(self, vetor):
        """ Converte o vetor distância (dx, dy) para uma das 8 direções (Estado). """
        dx, dy = vetor

        # 1. Normaliza o vetor para determinar a direção principal
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

        # 2. Se o agente está no farol
        if (norm_x, norm_y) == (0, 0):
            return "FAROL"

        # 3. Mapeia para a direção (Estado)
        return DIRECOES_MAP.get((norm_x, norm_y), "UNKNOWN")

    def _get_q_valores(self, estado):
        """ Inicializa ou retorna o dicionário de Q-valores para um dado estado. """
        if estado not in self.q_table:
            self.q_table[estado] = {acao: 0.0 for acao in ACOES}
        return self.q_table[estado]

    def _escolhe_melhor_acao(self, estado):
        """ Escolhe a ação com o maior valor Q (Explotação). """
        q_valores = self._get_q_valores(estado)
        max_q = max(q_valores.values())
        melhores_acoes = [acao for acao, q in q_valores.items() if q == max_q]
        return random.choice(melhores_acoes)

    # --- Interface do Agente ---

    # Adicionamos um método 'dummy' para manter a compatibilidade com o Simulador do Labirinto,
    # caso ele tente chamar 'atualiza_posicao' (Embora não o devesse fazer no Farol)
    def atualiza_posicao(self, nova_pos):
        pass

    def observacao(self, obs):
        self.ultima_observacao = obs
        # Atualiza o estado (Direção) com base na nova observação (vetor)
        self.estado_atual = self._converte_vetor_para_estado(obs)

    def age(self):
        # Guardar o estado antes de agir
        self.estado_anterior = self.estado_atual

        # Política Epsilon-greedy:
        if self.learning_mode and random.random() < self.epsilon:
            # EXPLORAÇÃO: Escolhe aleatoriamente
            acao = random.choice(ACOES)
        else:
            # EXPLOTAÇÃO: Escolhe a melhor ação da Q-table
            acao = self._escolhe_melhor_acao(self.estado_atual)

        self.acao_anterior = acao
        return acao

    def avaliacaoEstadoAtual(self, recompensa):
        self.recompensa_acumulada += recompensa

        # ----------------------------------------------------
        # LÓGICA DE APRENDIZAGEM (Q-LEARNING)
        # ----------------------------------------------------
        if self.learning_mode and self.estado_anterior is not None and self.acao_anterior is not None:
            s = self.estado_anterior
            a = self.acao_anterior
            r = recompensa
            s_prime = self.estado_atual

            # Só aprende se não for o estado final
            if s != "FAROL":
                q_s = self._get_q_valores(s)
                q_s_prime = self._get_q_valores(s_prime)

                q_atual = q_s[a]

                # 1. Calcular o máximo Q para o novo estado (s')
                max_q_prime = max(q_s_prime.values())

                # 2. Aplicar a fórmula Q-Learning
                novo_q = (1 - self.alpha) * q_atual + self.alpha * (r + self.gamma * max_q_prime)

                # 3. Atualizar a Q-table
                q_s[a] = novo_q

            # 4. Decaimento do Epsilon
            if self.epsilon > MIN_EPSILON:
                self.epsilon *= EPSILON_DECAY