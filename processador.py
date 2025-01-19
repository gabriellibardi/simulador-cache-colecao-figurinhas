from memoria_cache import MemoriaCache
from memoria_principal import MemoriaPrincipal

class Processador:
    def __init__(self, id: int, cache: MemoriaCache, memoria_principal: MemoriaPrincipal):
        self.id = id
        self.cache = cache
        self.memoria_principal = memoria_principal

    def executar(self):
        '''
        Executa a lógica do processador.
        '''
        print(f"Processador {self.id} executando...\n")
        
        while True:
            print(">>> Escolha a operação:\n")
            print("1: Ler")
            print("2: Escrever")
            print("c: Mostrar cache")
            print("m: Mostrar memória principal")
            print("q: Voltar")
            escolha = input("\n> ")
            print()

            if escolha == 'q':
                print("Processador finalizado.")
                return
            elif escolha == 'c':
                print(f"Cache {self.id}:\n")
                print(self.cache)
            elif escolha == 'm':
                print("Memória principal:\n")
                print(self.memoria_principal)
            elif escolha == '1':
                endereco = int(input("Endereço: "))
                print(f"Valor: {self.cache.ler(endereco)}")
            elif escolha == '2':
                endereco = int(input("Endereço: "))
                dado = input("Dado: ")
                self.cache.escrever(endereco, dado)
            else:
                print("Opção inválida.")
