from memoria_principal import MemoriaPrincipal
from memoria_cache import MemoriaCache
from processador import Processador
import random
import figurinhas

TAMANHO_MEMORIA_PRINCIPAL = 50
TAMANHO_CACHE = 10
TAMANHO_LINHA_CACHE = 5
QUANTIDADE_PROCESSADORES = 3

def main():
    # Inicializa os componentes
    memoria_principal = MemoriaPrincipal(TAMANHO_MEMORIA_PRINCIPAL, TAMANHO_LINHA_CACHE)
    caches = [MemoriaCache(TAMANHO_CACHE, TAMANHO_LINHA_CACHE) for _ in range(1, QUANTIDADE_PROCESSADORES + 1)]
    processadores = [Processador(i + 1, cache, memoria_principal) for i, cache in enumerate(caches)]

    # Cria as figurinhas e preenche a memória principal
    total_figurinhas = figurinhas.cria_figurinhas(TAMANHO_MEMORIA_PRINCIPAL * 2)
    preencher_colecao(memoria_principal, total_figurinhas)

    # Interface do usuário
    print("\n\033[92m-=-=-=-=-=-= SIMULADOR DE COLEÇÃO COMPARTILHADA DE FIGURINHAS =-=-=-=-=-=-\033[00m\n")
    while True:
        print(">>> Escolha um usuário para acessar:\n")
        for i in range(1, QUANTIDADE_PROCESSADORES + 1):
            print(f"\033[93m{i}:\033[00m Usuário {i}")
        print("\033[93mm:\033[00m Mostrar coleção")
        print("\033[93mq:\033[00m Sair")
        escolha = input("\n> ")
        print()

        if escolha == 'q':
            break
        elif escolha == 'm':
            print("Memória principal:\n")
            print(memoria_principal)
        else:
            try:
                escolha = int(escolha)
                processador = processadores[escolha - 1]
            except (ValueError, IndexError):
                print("Opção inválida.")
                print('\n' + '-' * 60)
                continue
            processador.executar()
        print('\n' + '-' * 60)

def preencher_colecao(colecao: MemoriaPrincipal, total_figurinhas: list[figurinhas.Figurinha]):
    '''
    Preenche a *colecao* com figurinhas aleatórias da lista *total_figurinhas*.
    '''
    for i in range(colecao.tamanho):
        colecao.escrever(i, random.choice(total_figurinhas))

if __name__ == "__main__":
    main()
