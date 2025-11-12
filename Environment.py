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


class AmbienteLabirinto:
    def __init__(self):
        self.size = 5  # Tamanho da grelha 5x5
        self.agente_pos = (0, 0)  # Posição inicial do agente

        # Definir o mapa: (0,0) é inicio, (4,4) é a Saída
        # Vamos criar paredes nas posições (1,1) e (1,2) como exemplo
        self.paredes = [
            Parede(1, 0), Parede(1, 1), Parede(1, 2), Parede(1, 3),  # Coluna de paredes
            Parede(3, 1), Parede(3, 2), Parede(3, 3), Parede(3, 4)  # Outra coluna
        ]
        self.objetivo = Objetivo(4, 4)

        # O agente pergunta: "O que há nesta coordenada?"

    def get_coisa_em(self, x, y):
        if (self.objetivo.x, self.objetivo.y) == (x, y):
            return self.objetivo

        for p in self.paredes:
            if (p.x, p.y) == (x, y):
                return p

        return Vazio(x, y)

    # O simulador/agente pede para observar
    def observacaoPara(self):
        # Retorna o objeto na posição atual do agente
        x, y = self.agente_pos
        return self.get_coisa_em(x, y)

    # O agente tenta mover-se
    def agir(self, accao):
        # accao é um tuplo (dx, dy), ex: (0, 1)
        curr_x, curr_y = self.agente_pos
        dx, dy = accao

        new_x = curr_x + dx
        new_y = curr_y + dy

        # Verificar se saiu do mapa
        if not (0 <= new_x < self.size and 0 <= new_y < self.size):
            return -10  # Penalidade grande por bater nas bordas

        # Verificar o que há na nova posição
        coisa = self.get_coisa_em(new_x, new_y)

        if isinstance(coisa, Parede):
            return -5  # Penalidade por bater na parede (não move)

        if isinstance(coisa, Objetivo):
            self.agente_pos = (new_x, new_y)  # Move
            return 100  # Grande recompensa por chegar à saída!

        # Se for vazio
        self.agente_pos = (new_x, new_y)  # Move
        return -1  # Pequena penalidade por cada passo (incentiva rapidez)

    def render(self):
        for i in range(self.size):
            row = ""
            for j in range(self.size):
                if self.agente_pos == (j, i):
                    row += " A "  # Agente
                elif self.objetivo.x == j and self.objetivo.y == i:
                    row += " S "  # Saída
                elif any(p.x == j and p.y == i for p in self.paredes):
                    row += " # "  # Parede
                else:
                    row += " . "  # Vazio
            print(row)
        print("\n")