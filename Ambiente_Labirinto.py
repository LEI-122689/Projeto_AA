from Interface_Ambiente import Ambiente

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


class AmbienteLabirinto(Ambiente):
    def __init__(self):
        self.size = 20
        self.agente_pos = (0, 0)
        self.objetivo = Objetivo(19, 19)

        # Mapa de Paredes 20x20 (Garantido de ser solúvel)
        self.paredes = [
            # PAREDES HORIZONTAIS
            Parede(2, 1), Parede(3, 1), Parede(4, 1), Parede(5, 1), Parede(6, 1), Parede(7, 1),
            Parede(0, 3), Parede(1, 3), Parede(2, 3), Parede(3, 3), Parede(4, 3), Parede(5, 3),
            Parede(7, 3), Parede(8, 3), Parede(9, 3), Parede(10, 3), Parede(11, 3),
            Parede(13, 3), Parede(14, 3), Parede(15, 3), Parede(16, 3), Parede(17, 3), Parede(18, 3),
            Parede(1, 5), Parede(2, 5), Parede(4, 5), Parede(5, 5), Parede(6, 5), Parede(7, 5),
            Parede(9, 5), Parede(10, 5), Parede(12, 5), Parede(13, 5), Parede(15, 5), Parede(16, 5),
            Parede(18, 5), Parede(19, 5),
            Parede(0, 7), Parede(1, 7), Parede(3, 7), Parede(5, 7), Parede(6, 7), Parede(8, 7),
            Parede(10, 7), Parede(11, 7), Parede(13, 7), Parede(15, 7), Parede(17, 7), Parede(18, 7),
            Parede(2, 9), Parede(3, 9), Parede(4, 9), Parede(5, 9), Parede(7, 9), Parede(8, 9),
            Parede(9, 9), Parede(11, 9), Parede(12, 9), Parede(14, 9), Parede(15, 9), Parede(16, 9),
            Parede(18, 9), Parede(19, 9),
            Parede(0, 11), Parede(1, 11), Parede(3, 11), Parede(5, 11), Parede(6, 11), Parede(8, 11),
            Parede(10, 11), Parede(11, 11), Parede(13, 11), Parede(15, 11), Parede(16, 11), Parede(18, 11),
            Parede(2, 13), Parede(3, 13), Parede(4, 13), Parede(5, 13), Parede(7, 13), Parede(8, 13),
            Parede(9, 13), Parede(11, 13), Parede(12, 13), Parede(14, 13), Parede(15, 13), Parede(17, 13),
            Parede(18, 13), Parede(19, 13),
            Parede(0, 15), Parede(1, 15), Parede(3, 15), Parede(5, 15), Parede(6, 15), Parede(8, 15),
            Parede(10, 15), Parede(11, 15), Parede(13, 15), Parede(15, 15), Parede(16, 15), Parede(18, 15),
            Parede(2, 17), Parede(3, 17), Parede(4, 17), Parede(5, 17), Parede(7, 17), Parede(8, 17),
            Parede(9, 17), Parede(11, 17), Parede(12, 17), Parede(14, 17), Parede(15, 17), Parede(17, 17), Parede(18, 17),
        ]

    def reset(self):
        self.agente_pos = (0, 0)

    def get_coisa_em(self, x, y):
        if (self.objetivo.x, self.objetivo.y) == (x, y):
            return self.objetivo
        for p in self.paredes:
            if (p.x, p.y) == (x, y):
                return p
        return Vazio(x, y)

    def observacaoPara(self):
        x, y = self.agente_pos
        return self.get_coisa_em(x, y)

    def agir(self, accao):
        curr_x, curr_y = self.agente_pos
        dx, dy = accao
        new_x, new_y = curr_x + dx, curr_y + dy

        if not (0 <= new_x < self.size and 0 <= new_y < self.size):
            return -10

        coisa = self.get_coisa_em(new_x, new_y)

        if isinstance(coisa, Parede):
            return -5

        self.agente_pos = (new_x, new_y)

        if isinstance(coisa, Objetivo):
            return 100

        return -1

    def jogo_terminou(self):
        return self.agente_pos == (self.objetivo.x, self.objetivo.y)

    def render(self):
        pass