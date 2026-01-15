# Projeto Agentes Autónomos
Este projeto implementa e compara dois algoritmos de aprendizagem (Q-Learning e Novelty Search) em ambientes de navegação com obstáculos (Labirinto e Farol).

## Grupo:
Guilherme Silva | Nº: 123303

Luís Silva | Nº: 122689

## Dependências
O projeto requer Python 3 e a biblioteca pygame para a visualização gráfica.

    pip install pygame

## Como Executar
Para iniciar a simulação (treino seguido de teste):

    python3 Simulador.py

## Configuração da Simulação
Para alterar os modos, dificuldades ou algoritmos, deve-se editar as linhas finais do ficheiro Simulador.py (bloco if __name__ == "__main__":).

A função sim.cria aceita os seguintes parâmetros:

    Problema: "labirinto" ou "farol"

    Dificuldade: "facil", "medio" ou "dificil"

    Algoritmo: "qlearning" ou "novelty"

## Exemplo de configuração:

    if __name__ == "__main__":
        sim = Simulador()
    
        # Exemplo: Problema Farol, Dificuldade Difícil com Q-Learning
        sim.cria("farol", "dificil", "qlearning")
    
        # Ajuste de FPS e episódios
        sim.fps = 10
        sim.executa(episodios_treino=1000, episodios_teste=100)

## Análise de Performance (Gráficos)
O projeto inclui um módulo dedicado (Graficos.py) para comparar o desempenho dos agentes (Q-Learning vs Novelty) no mesmo cenário. Este script executa as simulações em segundo plano e gera gráficos comparativos de passos e recompensas.

Configurar o Cenário de Teste
Para escolher qual o problema e dificuldade a analisar, deve editar o final do ficheiro Graficos.py. Comente ou descomente as linhas conforme o desejado:

    if __name__ == "__main__":
    
        # Exemplo 1: Comparar no Labirinto (Dificuldade: Médio)
        #gerar_grafico_comparativo("labirinto", "medio")
    
        # Exemplo 2: Comparar no Farol (Dificuldade: Difícil)
        gerar_grafico_comparativo("farol", "dificil")