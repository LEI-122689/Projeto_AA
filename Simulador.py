import time
# Importar as classes dos outros ficheiros
from Ambientes import AmbienteFarol, AmbienteLabirinto
from Agentes import AgenteFarol, AgenteLabirinto


class Simulador:
    def __init__(self):
        self.ambiente = None
        self.agente = None
        self.passos = 0
        self.max_passos = 100
        self.modo = ""

    # Este método escolhe qual o problema que vamos correr [cite: 20]
    def cria(self, tipo_problema):
        self.modo = tipo_problema

        if tipo_problema == "farol":
            print("-> A carregar Problema 1: Farol")
            self.ambiente = AmbienteFarol()
            self.agente = AgenteFarol()

        elif tipo_problema == "labirinto":
            print("-> A carregar Problema 3: Labirinto")
            self.ambiente = AmbienteLabirinto()  # Aquele teu código do labirinto
            self.agente = AgenteLabirinto()

        else:
            raise Exception("Problema desconhecido! Escolhe 'farol' ou 'labirinto'.")

    def executa(self):
        if self.ambiente is None or self.agente is None:
            print("Erro: Tens de correr sim.cria() primeiro!")
            return

        print(f"--- Início da Simulação: {self.modo.upper()} ---")
        terminou = False

        # O Ciclo de Simulação é IGUAL para os dois problemas [cite: 55]
        while not terminou and self.passos < self.max_passos:
            print(f"\nPasso: {self.passos}")

            # 1. Mostrar Estado
            self.ambiente.render()

            # 2. Percepção [cite: 61]
            # No Farol devolve vetor (x,y); No Labirinto devolve objeto/parede
            percepcao = self.ambiente.observacaoPara()
            self.agente.observacao(percepcao)

            # 3. Deliberação e Ação [cite: 67]
            acao = self.agente.age()

            # 4. Execução e Recompensa [cite: 70]
            recompensa = self.ambiente.agir(acao)

            # 5. Aprendizagem/Avaliação [cite: 31]
            self.agente.avaliacaoEstadoAtual(recompensa)

            # 6. Verificar se terminou (O ambiente diz se o objetivo foi cumprido)
            # Vamos adicionar um método 'fim_de_jogo()' aos ambientes para facilitar
            if self.ambiente.jogo_terminou():
                print("--- SUCESSO! Objetivo alcançado. ---")
                self.ambiente.render()
                terminou = True

            self.passos += 1
            time.sleep(0.2)  # Atraso para visualização

        if not terminou:
            print("--- FIM: Limite de passos atingido. ---")


# Exemplo de uso:
if __name__ == "__main__":
    sim = Simulador()

    # AQUI TU ESCOLHES QUAL QUERES CORRER:
    # sim.cria("farol")      # Corre o problema 1
    sim.cria("labirinto")  # Corre o problema 3

    sim.executa()