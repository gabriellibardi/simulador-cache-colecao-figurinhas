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
        
        print(">>> Escolha a operação:\n")
        print("1: Ler")
        print("2: Escrever")
        print("q: Sair")
        escolha = input("\n> ")

        print("Processador finalizado.")