from memoria_principal import MemoriaPrincipal
from memoria_cache import MemoriaCache
from processador import Processador

TAMANHO_MEMORIA_PRINCIPAL = 50
TAMANHO_CACHE = 5
QUANTIDADE_PROCESSADORES = 3

def main():
    # Inicializa os componentes
    memoria_principal = MemoriaPrincipal(TAMANHO_MEMORIA_PRINCIPAL)
    caches = [MemoriaCache(TAMANHO_CACHE) for _ in range(QUANTIDADE_PROCESSADORES)]
    processadores = [Processador(i, cache, memoria_principal) for i, cache in enumerate(caches)]
    
    # Interface do usuário
    print("-=-=-=-=-=-= SIMULADOR DE COLEÇÃO COMPARTILHADA DE FIGURINHAS =-=-=-=-=-=-\n")
    while True:
        preencher_memoria()

        print("> Escolha um usuário para acessar:\n")
        for i in range(QUANTIDADE_PROCESSADORES):
            print(f"{i}: Usuário {i}")
        print("q: Sair")
        escolha = input("\nProcessador: ")
        print()
        if escolha == 'q':
            break
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

def preencher_memoria():
    '''
    Preenche a memória principal com valores aleatórios.
    '''
    pass

if __name__ == "__main__":
    main()
