from memoria_principal import MemoriaPrincipal
from memoria_cache import MemoriaCache
from processador import Processador
import random
import figurinhas

TAMANHO_MEMORIA_PRINCIPAL = 50
TAMANHO_CACHE = 5
QUANTIDADE_PROCESSADORES = 3

def main():
    # Inicializa os componentes
    memoria_principal = MemoriaPrincipal(TAMANHO_MEMORIA_PRINCIPAL)
    caches = [MemoriaCache(TAMANHO_CACHE) for _ in range(QUANTIDADE_PROCESSADORES)]
    processadores = [Processador(i, cache, memoria_principal) for i, cache in enumerate(caches)]

    # Cria as figurinhas e preenche a memória principal
    total_figurinhas = figurinhas.cria_figurinhas(TAMANHO_MEMORIA_PRINCIPAL * 2)
    preencher_colecao(memoria_principal, total_figurinhas)

    # Interface do usuário
    print("\033[92m-=-=-=-=-=-= SIMULADOR DE COLEÇÃO COMPARTILHADA DE FIGURINHAS =-=-=-=-=-=-\033[00m\n")
    while True:

        print(">>> Escolha um usuário para acessar:\n")
        for i in range(QUANTIDADE_PROCESSADORES):
            print(f"{i}: Usuário {i}")
        print("c: Mostrar coleção")
        print("q: Sair")
        escolha = input("\n> ")
        print()

        if escolha == 'q':
            break
        elif escolha == 'c':
            print("Memória principal:\n")
            print(memoria_principal)
        else:
            try:
                escolha = int(escolha)
                processador = processadores[escolha]
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
