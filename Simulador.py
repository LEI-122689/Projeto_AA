import time
# Importar as classes dos outros ficheiros
from Ambiente_Labirinto import AmbienteLabirinto
from Agente_Labirinto import AgenteLabirinto
from Ambiente_Farol import AmbienteFarol
from Agente_Farol import AgenteFarol


class Simulador:
    def __init__(self):
        self.ambiente = None
        self.agente = None
        self.passos = 0
        self.max_passos = 200  # Limite de passos por episódio
        self.modo = ""

    # Este método escolhe qual o problema que vamos correr
    def cria(self, tipo_problema):
        self.modo = tipo_problema

        if tipo_problema == "farol":
            print("-> A carregar Problema 1: Farol (Q-Learning)")
            self.ambiente = AmbienteFarol()
            self.agente = AgenteFarol()
            # Informar o agente do estado inicial (vetor)
            self.agente.observacao(self.ambiente.observacaoPara())

        elif tipo_problema == "labirinto":
            print("-> A carregar Problema 3: Labirinto (Q-Learning)")
            self.ambiente = AmbienteLabirinto()  # Aquele teu código do labirinto
            self.agente = AgenteLabirinto()
            # Informar o agente da sua posição inicial (Estado)
            self.agente.atualiza_posicao(self.ambiente.agente_pos)

        else:
            raise Exception("Problema desconhecido! Escolhe 'farol' ou 'labirinto'.")

    # Método para executar um único ciclo de tentativa (episódio)
    def executa_episodio(self, renderizar=False):
        # 1. Resetar o estado do ambiente e do agente para um novo episódio
        self.passos = 0
        terminou = False

        if self.modo == "labirinto":
            # Recria o ambiente (para labirintos estáticos, isto é um reset)
            self.ambiente = AmbienteLabirinto()
            self.agente.recompensa_acumulada = 0
            # O Agente Labirinto usa a posição absoluta como estado
            self.agente.atualiza_posicao(self.ambiente.agente_pos)

        elif self.modo == "farol":
            # Usa o método reset() e reinicia o estado
            self.ambiente.reset()
            self.agente.recompensa_acumulada = 0
            # O Agente Farol usa a observação inicial para definir o estado (Direção)
            self.agente.observacao(self.ambiente.observacaoPara())

        # O Ciclo de Simulação
        while not terminou and self.passos < self.max_passos:
            if renderizar:
                print(f"\nPasso: {self.passos}")
                self.ambiente.render()

            # 2. Percepção
            percepcao = self.ambiente.observacaoPara()
            self.agente.observacao(percepcao)

            # 3. Deliberação e Ação
            acao = self.agente.age()

            # 4. Execução e Recompensa
            recompensa = self.ambiente.agir(acao)

            # ATUALIZAÇÃO SÓ PARA O LABIRINTO: Comunica a nova posição (estado)
            if self.modo == "labirinto":
                self.agente.atualiza_posicao(self.ambiente.agente_pos)

            # 5. Aprendizagem/Avaliação
            self.agente.avaliacaoEstadoAtual(recompensa)

            # 6. Verificar se terminou
            if self.ambiente.jogo_terminou():
                if renderizar:
                    print("--- SUCESSO! Objetivo alcançado. ---")
                    self.ambiente.render()
                terminou = True

            self.passos += 1
            if renderizar:
                time.sleep(0.05)

        if renderizar and not terminou:
            print("--- FIM: Limite de passos atingido. ---")

        return terminou, self.passos, self.agente.recompensa_acumulada

    # Método principal para correr múltiplos episódios de aprendizagem
    def executa(self):
        if self.ambiente is None or self.agente is None:
            print("Erro: Tens de correr sim.cria() primeiro!")
            return

        # Configuração: Número de episódios
        if self.modo == "farol":
            num_episodios = 1000
        else:
            num_episodios = 500

        self.agente.learning_mode = True

        print(f"--- Início da Simulação: {self.modo.upper()} ({num_episodios} Episódios de Aprendizagem) ---")

        # Loop de Episódios
        for episodio in range(1, num_episodios + 1):
            # Renderizar apenas o último episódio (após a aprendizagem)
            render_agora = (episodio == num_episodios)

            sucesso, passos, recompensa_total = self.executa_episodio(renderizar=render_agora)

            # Mostrar o progresso
            if episodio % (num_episodios // 10) == 0 or episodio == num_episodios or episodio == 1:
                print(
                    f"Episódio {episodio}/{num_episodios} | Sucesso: {sucesso} | Passos: {passos} | Recompensa Total: {recompensa_total:.2f} | Epsilon: {self.agente.epsilon:.4f}")

        print("--- FIM: Simulação Concluída. ---")


# Exemplo de uso:
if __name__ == "__main__":
    sim = Simulador()

    sim.cria("farol")  # Corre o problema 1 com Q-Learning
    # sim.cria("labirinto")

    sim.executa()