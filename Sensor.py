class Sensor:
    def __init__(self, ambiente, dificuldade):
        self.ambiente = ambiente
        self.dificuldade = dificuldade

    def get_posicao_objetivo(self):
        """
        Devolve a posição (x, y) do objetivo se estiver dentro do alcance.
        Caso contrário, devolve None (sinal cego).
        """
        # 1. Descobrir onde estamos (Agente)
        ax, ay = self.ambiente.agente_pos

        # 2. Descobrir onde está o objetivo (depende do ambiente)
        target_x, target_y = None, None

        # Duck Typing: Verifica se o ambiente tem 'farol_x' ou 'objetivo'
        if hasattr(self.ambiente, 'farol_x'):
            # Ambiente Farol
            target_x, target_y = self.ambiente.farol_x, self.ambiente.farol_y
        elif hasattr(self.ambiente, 'objetivo') and self.ambiente.objetivo is not None:
            # Ambiente Labirinto
            target_x, target_y = self.ambiente.objetivo.x, self.ambiente.objetivo.y
        else:
            # Se não houver objetivo definido
            return None

            # 3. Calcular Distância Manhattan (Passos na grelha)
        distancia = abs(target_x - ax) + abs(target_y - ay)

        # 4. Aplicar Regras de Dificuldade
        visivel = False

        if self.dificuldade == "facil":
            visivel = True  # Alcance Infinito

        elif self.dificuldade == "medio":
            if distancia <= 15:  # Alcance Médio
                visivel = True

        elif self.dificuldade == "dificil":
            if distancia <= 10:  # Alcance Curto
                visivel = True

        # 5. Retornar informação ou silêncio
        if visivel:
            return (target_x, target_y)
        else:
            return None