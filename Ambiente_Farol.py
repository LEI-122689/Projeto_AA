import math


class Ambiente_Farol:
    def __init__(self):
        # O Farol precisa de um espaço maior e aberto
        self.size_x = 20
        self.size_y = 10
        self.agente_pos = (0, 0)

        # Definição do objetivo (Farol)
        self.farol_x = 18
        self.farol_y = 5

    # Agente vê o vetor direção (distância X, distância Y)
    def observacaoPara(self):
        ax, ay = self.agente_pos
        fx, fy = self.farol_x, self.farol_y
        return (fx - ax, fy - ay)

    def agir(self, accao):
        # accao é (dx, dy)
        curr_x, curr_y = self.agente_pos
        dx, dy = accao

        new_x = curr_x + dx
        new_y = curr_y + dy

        # Verificar limites do mapa
        if not (0 <= new_x < self.size_x and 0 <= new_y < self.size_y):
            return -10  # Penalidade por bater na borda

        # Atualizar posição
        self.agente_pos = (new_x, new_y)

        # Verificar se chegou ao Farol
        if self.agente_pos == (self.farol_x, self.farol_y):
            return 100  # Recompensa grande

        return -1  # Custo por passo

    def jogo_terminou(self):
        return self.agente_pos == (self.farol_x, self.farol_y)

    def render(self):
        print("-" * (self.size_x + 2))
        for y in range(self.size_y):
            row = "|"
            for x in range(self.size_x):
                if self.agente_pos == (x, y):
                    row += "A"
                elif (self.farol_x, self.farol_y) == (x, y):
                    row += "F"
                else:
                    row += " "
            row += "|"
            print(row)
        print("-" * (self.size_x + 2))