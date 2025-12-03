import numpy as np
import random


class AgenteNovelty:
    def __init__(self):
        self.recompensa_acumulada = 0

        self.input_size = 4
        self.output_size = 4

        # Pesos: Como ligo os sensores às ações
        self.pesos = np.random.uniform(-1, 1, (self.input_size, self.output_size))

        # BIAS: A "personalidade" base do agente (ajuda a não bloquear em zeros)
        self.bias = np.random.uniform(-1, 1, (self.output_size,))

        self.posicao_final = (0, 0)
        self.score_novidade = 0.0
        self.learning_mode = False
        self.epsilon = 0

    def mutate(self, taxa=0.1):
        # Mutação nos Pesos
        ruido_w = np.random.normal(0, 0.5, size=self.pesos.shape)
        mask_w = np.random.random(self.pesos.shape) < taxa
        self.pesos[mask_w] += ruido_w[mask_w]

        # Mutação no Bias (Importante!)
        ruido_b = np.random.normal(0, 0.5, size=self.bias.shape)
        mask_b = np.random.random(self.bias.shape) < taxa
        self.bias[mask_b] += ruido_b[mask_b]

        # Limitar valores para não explodir
        self.pesos = np.clip(self.pesos, -2, 2)
        self.bias = np.clip(self.bias, -2, 2)

    def observacao(self, obs):
        # MUDANÇA: Vazio agora é 0.5 para estimular a rede a ativar-se
        # Parede continua negativo para inibir
        mapeamento = {"Parede": -1.0, "Vazio": 0.5, "Saida": 2.0}

        sensores = [
            mapeamento.get(obs.get("N"), -1),
            mapeamento.get(obs.get("S"), -1),
            mapeamento.get(obs.get("W"), -1),
            mapeamento.get(obs.get("E"), -1)
        ]
        self.input_vector = np.array(sensores)

    def age(self):
        # Matemática: y = Wx + b (Pesos * Input + Bias)
        sinais = np.dot(self.input_vector, self.pesos) + self.bias

        # Função de Ativação (Tanh) para dar não-linearidade (Opcional mas bom)
        decisao = np.tanh(sinais)

        acao_idx = np.argmax(decisao)
        acoes = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        return acoes[acao_idx]

    def atualiza_posicao(self, pos):
        self.posicao_final = pos

    def avaliacaoEstadoAtual(self, recompensa):
        self.recompensa_acumulada += recompensa