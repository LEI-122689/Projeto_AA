from Interface_Ambiente import Ambiente
class AmbienteFarol:
    def __init__(self):
        # Tamanho impar (21x11) para termos um "centro" exato
        self.size_x = 21
        self.size_y = 11

        self.agente_pos = (0, 0)

        # Farol no Centro do Mundo
        self.farol_x = 10
        self.farol_y = 5

        # Contador interno para controlar a rotação da luz
        self.tempo_luz = 0

    def reset(self):
        """ Reseta a posição do agente para o início do episódio (0, 0). """
        self.agente_pos = (0, 0)
        self.tempo_luz = 0 

    def observacaoPara(self):
        # O Agente continua a receber o vetor distância até ao farol
        ax, ay = self.agente_pos
        fx, fy = self.farol_x, self.farol_y
        return (fx - ax, fy - ay)

    def agir(self, accao):
        curr_x, curr_y = self.agente_pos
        dx, dy = accao

        # Calcular nova posição
        new_x = curr_x + dx
        new_y = curr_y + dy

        # Verificar limites (não pode sair da grelha)
        if not (0 <= new_x < self.size_x and 0 <= new_y < self.size_y):
            return -10  # Penalidade borda

        self.agente_pos = (new_x, new_y)

        # Verificar se chegou ao Farol
        if self.agente_pos == (self.farol_x, self.farol_y):
            return 1000  # Grande Sucesso!

        return -1  # Custo de movimento

    def jogo_terminou(self):
        return self.agente_pos == (self.farol_x, self.farol_y)

    # --- A LÓGICA VISUAL NOVA ESTÁ AQUI ---
    def render(self):
        # 1. Calcular onde está a luz neste momento
        # Lista de 8 direções (Sentido horário: N, NE, E, SE, S, SW, W, NW)
        direcoes = [
            (0, -1), (1, -1), (1, 0), (1, 1),
            (0, 1), (-1, 1), (-1, 0), (-1, -1)
        ]

        # O operador % 8 garante que o índice roda entre 0 e 7 infinitamente
        dir_atual = direcoes[self.tempo_luz % 8]

        # Calcular as coordenadas do feixe de luz (Alcance 3)
        luz_coords = []
        for i in range(1, 4):  # 1, 2, 3
            lx = self.farol_x + (dir_atual[0] * i)
            ly = self.farol_y + (dir_atual[1] * i)
            luz_coords.append((lx, ly))

        # 2. Desenhar o mapa
        print("-" * (self.size_x * 2 + 2))
        for y in range(self.size_y):
            row = "|"
            for x in range(self.size_x):
                char = " ."  # O ponto que pediste (espaço vazio)

                # Se for posição da Luz
                if (x, y) in luz_coords:
                    char = " *"  # Luz do farol

                # Se for o Farol (sobrepõe a luz)
                if (x, y) == (self.farol_x, self.farol_y):
                    char = " F"

                # Se for o Agente (sobrepõe tudo)
                if (x, y) == self.agente_pos:
                    char = " A"

                row += char
            row += " |"
            print(row)
        print("-" * (self.size_x * 2 + 2))

        # Incrementa o tempo para a luz rodar no próximo frame
        self.tempo_luz += 1