from memoria_cache import MemoriaCache, Resposta, Estado
from memoria_principal import MemoriaPrincipal

class Processador:
    def __init__(self, id: int, cache: MemoriaCache, memoria_principal: MemoriaPrincipal, sistema):
        self.id = id
        self.cache = cache
        self.memoria_principal = memoria_principal
        self.sistema = sistema

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
                try:
                    endereco = int(input("Endereço: "))
                    print()
                    resultado = self.ler(endereco)
                    print(resultado[1])
                    print(f"Valor: {resultado[0]}")
                except:
                    print("\n\033[91mEndereço Inválido.\033[00m")
            elif escolha == '2':
                endereco = int(input("Endereço: "))
                dado = input("Dado: ")
                print()
                resultado = self.escrever(endereco, dado)
                print(resultado[1])
                print(f"Valor: {resultado[0]}")
            else:
                print("\n\033[91mOpção Inválida.\033[00m")

    def ler(self, endereco: int):
        '''
        Lê um dado no *endereco* da memória.
        '''
        resposta = self.cache.ler(endereco)
        if resposta[1] == Resposta.HIT:
            return resposta
        else: # MISS
            # Procura o bloco nas caches dos outros processadores
            for cache in self.sistema.caches:
                if cache != self.cache:
                    resposta = cache.ler(endereco)
                    if resposta[1] == Resposta.HIT:
                        # Atualiza a cache do processador atual com o bloco encontrado
                        
                        return resposta
            # Se não encontrar o bloco nas caches dos outros processadores, busca na memória principal
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
