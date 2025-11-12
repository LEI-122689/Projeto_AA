import time
from Environment import AmbienteLabirinto, Objetivo
from Agent import AgenteLabirinto


class Simulador:
    def __init__(self):
        self.ambiente = AmbienteLabirinto()
        self.agente = AgenteLabirinto()
        self.passos = 0
        #self.max_passos = 20  # Limite para não ficar em loop infinito

    def executa(self):
        print("--- Início da Simulação: Labirinto ---")

        terminou = False

        while not terminou: #and self.passos < self.max_passos:
            print(f"Passo: {self.passos}")
            self.ambiente.render()

            # 1. Agente decide
            acao = self.agente.age()

            # 2. Ambiente executa e dá feedback
            recompensa = self.ambiente.agir(acao)

            # 3. Agente aprende
            self.agente.avaliacaoEstadoAtual(recompensa)

            # 4. Verifica se chegou ao fim
            # O método observacaoPara devolve onde o agente está
            onde_estou = self.ambiente.observacaoPara()

            if isinstance(onde_estou, Objetivo):
                print("SUCESSO! O agente encontrou a saída.")
                self.ambiente.render()
                terminou = True

            self.passos += 1
            time.sleep(0.5)  # Pausa para conseguires ver

        if not terminou:
            print("Falhou: O agente não encontrou a saída a tempo.")


if __name__ == "__main__":
    sim = Simulador()
    sim.executa()