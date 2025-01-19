from memoria_cache import MemoriaCache
from memoria_principal import MemoriaPrincipal
from enum import Enum

class Resposta:
    HIT = "\033[92mHit\033[00m"
    MISS = "\033[91mMiss\033[00m"

class Processador:
    def __init__(self, id: int, cache: MemoriaCache, memoria_principal: MemoriaPrincipal):
        self.id = id
        self.cache = cache
        self.memoria_principal = memoria_principal

    def executar(self):
        '''
        Executa a lógica do processador.
        '''
        print(f"Processador {self.id} executando...")
        
        while True:
            print("\n>>> Escolha a operação:\n")
            print("\033[93m1:\033[00m Ler")
            print("\033[93m2:\033[00m Escrever")
            print("\033[93mc:\033[00m Mostrar cache")
            print("\033[93mm:\033[00m Mostrar memória principal")
            print("\033[93mq:\033[00m Voltar")
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
                print()
                resultado = self.ler(endereco)
                print(resultado[1])
                print(f"Valor: {resultado[0]}")
            elif escolha == '2':
                endereco = int(input("Endereço: "))
                dado = input("Dado: ")
                print()
                resultado = self.escrever(endereco, dado)
                print(resultado[1])
                print(f"Valor: {resultado[0]}")
            else:
                print("Opção inválida.")

    def ler(self, endereco: int):
        '''
        Lê um dado no *endereco* da memória.
        '''
        try:
            return self.cache.ler(endereco), Resposta.HIT
        except:
            self.cache.carregar_linha(self.memoria_principal.buscar_bloco(endereco), endereco)
            return self.memoria_principal.ler(endereco), Resposta.MISS
    
    def escrever(self, endereco: int, dado):
        '''
        Escreve um *dado* no *endereco* da memória.
        '''
        try:
            return (self.cache.buscar_endereco(endereco), Resposta.HIT)
        except:
            return (self.memoria_principal.escrever(endereco, dado), Resposta.MISS)
