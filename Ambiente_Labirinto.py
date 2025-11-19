# Classes auxiliares apenas para o Labirinto
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
        self.size = 8
        self.agente_pos = (0, 0)
        self.objetivo = Objetivo(7, 7)

        # Mapa de Paredes
        self.paredes = [
            Parede(1, 0), Parede(1, 1), Parede(1, 2),
            Parede(3, 2), Parede(3, 3), Parede(3, 4), Parede(3, 5),
            Parede(5, 1), Parede(5, 2), Parede(5, 6), Parede(5, 7),
            Parede(6, 1)
        ]

    def get_coisa_em(self, x, y):
        if (self.objetivo.x, self.objetivo.y) == (x, y):
            return self.objetivo
        for p in self.paredes:
            if (p.x, p.y) == (x, y):
                return p
        return Vazio(x, y)

    # Agente vê o objeto na posição atual
    def observacaoPara(self):
        x, y = self.agente_pos
        return self.get_coisa_em(x, y)

    def agir(self, accao):
        curr_x, curr_y = self.agente_pos
        dx, dy = accao
        new_x, new_y = curr_x + dx, curr_y + dy

        # Verificar limites
        if not (0 <= new_x < self.size and 0 <= new_y < self.size):
            return -10

        coisa = self.get_coisa_em(new_x, new_y)

        if isinstance(coisa, Parede):
            return -5  # Bateu na parede

        self.agente_pos = (new_x, new_y)

        if isinstance(coisa, Objetivo):
            return 100

        return -1

    def jogo_terminou(self):
        return self.agente_pos == (self.objetivo.x, self.objetivo.y)

    def render(self):
        print("-" * (self.size * 3 + 2))
        for i in range(self.size):
            row = "| "
            for j in range(self.size):
                if self.agente_pos == (j, i):
                    row += "A "
                elif self.objetivo.x == j and self.objetivo.y == i:
                    row += "S "
                elif any(p.x == j and p.y == i for p in self.paredes):
                    row += "# "
                else:
                    row += ". "
            row += "|"
            print(row)
        print("-" * (self.size * 3 + 2))