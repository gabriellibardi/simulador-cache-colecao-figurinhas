from sistema import Sistema
import random
import figurinhas

TAMANHO_MEMORIA_PRINCIPAL = 50
TAMANHO_CACHE = 10
TAMANHO_LINHA_CACHE = 5
QUANTIDADE_PROCESSADORES = 3

def main():
    # Cria as figurinhas
    total_figurinhas = figurinhas.cria_figurinhas(TAMANHO_MEMORIA_PRINCIPAL * 2)

    # Inicializa o sistema
    sistema = Sistema(QUANTIDADE_PROCESSADORES, TAMANHO_MEMORIA_PRINCIPAL, TAMANHO_CACHE, TAMANHO_LINHA_CACHE, total_figurinhas)

    # Preenche a memória principal com figurinhas aleatórias
    preencher_colecao(sistema.memoria_principal, total_figurinhas)

    # Executa o sistema
    sistema.executar()

def preencher_colecao(colecao, total_figurinhas: list[figurinhas.Figurinha]):
    '''
    Preenche a *colecao* com figurinhas aleatórias da lista *total_figurinhas*.
    '''
    for i in range(colecao.tamanho):
        colecao.escrever(i, random.choice(total_figurinhas))

if __name__ == "__main__":
    main()
