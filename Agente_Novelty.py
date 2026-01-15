import random
from Interface_Agente import Agente


class AgenteNovelty(Agente):
    def __init__(self):
        self.visitas = {}
        self.paredes_conhecidas = set()

        self.estado_atual = None
        self.posicao_anterior = None
        self.acao_anterior = None

        # Onde está o objetivo (Vem do Sensor)
        self.objetivo_detectado = None

        self.acoes = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # N, S, O, E

        self.historico_recente = []
        self.ja_agiu = False

        # Compatibilidade com Simulador
        self.recompensa_acumulada = 0
        self.epsilon = 0.0
        self.learning_mode = False

    def observacao(self, obs, alvo=None):
        """
        Recebe a posição atual (obs) e, opcionalmente, a posição do alvo (Sensor).
        """
        self.estado_atual = obs
        self.objetivo_detectado = alvo

        # 1. Deteção de Paredes (Aprendizagem passiva)
        if self.ja_agiu:
            if self.posicao_anterior == self.estado_atual and self.acao_anterior is not None:
                dx, dy = self.acao_anterior
                cx, cy = self.estado_atual
                # Se tentei mover e fiquei no mesmo sitio, é parede
                self.paredes_conhecidas.add((cx + dx, cy + dy))
            self.ja_agiu = False

        # 2. Registar Visita Global (Mapa de Calor)
        if self.estado_atual not in self.visitas:
            self.visitas[self.estado_atual] = 0
        self.visitas[self.estado_atual] += 1

        # 3. Atualizar Memória de Curto Prazo (Tabu List)
        self.historico_recente.append(self.estado_atual)
        if len(self.historico_recente) > 4:  # Tamanho da memória recente
            self.historico_recente.pop(0)

        self.posicao_anterior = self.estado_atual

    def age(self):
        cx, cy = self.estado_atual

        candidatos = []
        # Baralhar para não haver vício de direção em empates
        random.shuffle(self.acoes)

        for acao in self.acoes:
            dx, dy = acao
            vizinho = (cx + dx, cy + dy)

            # --- FILTRO 1: Segurança ---
            # Se for uma parede conhecida, ignoramos imediatamente
            if vizinho in self.paredes_conhecidas:
                continue

            # --- CÁLCULO DO SCORE (A Mente do Novelty) ---
            # Score Base = Número de vezes que já lá fui
            score = self.visitas.get(vizinho, 0)

            # Penalidade Tabu: Se estive lá há pouco tempo, torna-se muito desinteressante
            if vizinho in self.historico_recente:
                score += 1000

            # --- A TUA IDEIA: GRAVITATIONAL PULL ---
            # Se o sensor deteta o objetivo, aplicamos a "gravidade"
            if self.objetivo_detectado is not None:
                tx, ty = self.objetivo_detectado

                # Distância atual ao objetivo
                dist_atual = abs(cx - tx) + abs(cy - ty)
                # Distância do vizinho ao objetivo
                dist_vizinho = abs(vizinho[0] - tx) + abs(vizinho[1] - ty)

                # Se este movimento nos aproxima do objetivo...
                if dist_vizinho < dist_atual:
                    # ...damos um desconto no score!
                    # Subtrair 0.5 significa que o agente prefere ir para uma casa
                    # que o aproxima do objetivo do que para uma casa neutra,
                    # mesmo que tenham o mesmo número de visitas.
                    score -= 0.5

                    # Nota: Não usamos um valor gigante (tipo -1000) para não o forçar
                    # a entrar em loops se houver uma parede invisível.
                    # É apenas uma "sugestão" forte.

            candidatos.append((score, acao))

        # --- DECISÃO ---
        if not candidatos:
            # Encurralado? Tenta qualquer coisa (vai bater e atualizar paredes)
            acao = random.choice(self.acoes)
        else:
            # Escolhe o candidato com MENOR score (Mais Novidade + Gravidade)
            min_score = min(candidatos, key=lambda x: x[0])[0]
            melhores_opcoes = [acao for (s, acao) in candidatos if s == min_score]
            acao = random.choice(melhores_opcoes)

        self.acao_anterior = acao
        self.ja_agiu = True
        return acao

    def avaliacaoEstadoAtual(self, recompensa):
        self.recompensa_acumulada += recompensa

    def atualiza_posicao(self, nova_pos):
        pass