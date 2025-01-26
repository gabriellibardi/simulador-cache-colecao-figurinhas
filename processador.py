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

            # Voltar
            if escolha == 'q': 
                print("Processador finalizado.\n")
                return
            # Mostrar cache
            elif escolha == 'c':
                print(f"Cache {self.id}:\n")
                print(self.cache)
            # Mostrar memória principal
            elif escolha == 'm':
                print("Memória principal:\n")
                print(self.memoria_principal)
            # Ler
            elif escolha == '1':
                try:
                    endereco = int(input("Endereço: "))
                    print()
                    resultado = self.ler(endereco)
                    print(f"\nValor: {resultado}")
                except:
                    print("\n\033[91mEndereço Inválido.\033[00m")
            # Escrever
            elif escolha == '2':
                try:
                    endereco = int(input("Endereço: "))
                    if endereco >= self.memoria_principal.tamanho:
                        raise ValueError(f"Endereço {endereco} fora dos limites da memória.")
                except:
                    print("\n\033[91mEndereço Inválido.\033[00m")
                dado = input(f"Número da figurinha (1 até {len(self.sistema.total_figurinhas)}): ")
                if not dado.isdigit() or int(dado) < 1 or int(dado) > len(self.sistema.total_figurinhas):
                    print("\n\033[91mNúmero da figurinha inválido.\033[00m")
                figurinha = self.sistema.total_figurinhas[int(dado) - 1]
                print()
                self.escrever(endereco, figurinha)
                print(f"\nValor escrito: {figurinha}")
            else:
                print("\n\033[91mOpção Inválida.\033[00m")

    def ler(self, endereco: int):
        '''
        Lê um dado no *endereco* da memória.
        '''
        resposta = self.cache.ler(endereco)
        if resposta[1] == Resposta.HIT:
            print("\033[92mHit\033[00m")
            return resposta[0]
        else: # MISS
            print("\033[91mMiss\033[00m")
            # Procura o bloco nas caches dos outros processadores
            print("\nBuscando bloco nas outras caches...")
            for cache in self.sistema.caches:
                if cache != self.cache: # Evita a busca na própria cache
                    resposta = cache.procurar_linha(endereco)
                    if resposta is not None:
                        print("Bloco encontrado na cache de outro processador.")
                        if resposta.estado == Estado.FORWARD: # Mais de uma cache possui o bloco
                            self.cache.carregar_linha(resposta.dados, endereco, Estado.SHARED)
                        elif resposta.estado == Estado.EXCLUSIVE: # Uma única cache possui o bloco
                            self.cache.carregar_linha(resposta.dados, endereco, Estado.SHARED)
                            resposta.estado = Estado.FORWARD
                        elif resposta.estado == Estado.MODIFIED: # Uma única cache possui o bloco e está modificando
                            self.memoria_principal.atualizar_bloco(resposta.dados, endereco)
                            resposta.estado = Estado.FORWARD
                            self.cache.carregar_linha(resposta.dados, endereco, Estado.SHARED)
                        return cache.ler(endereco)[0]
            # Se não encontrar o bloco nas caches dos outros processadores, busca na memória principal
            print("Buscando bloco na memória principal...")
            self.cache.carregar_linha(self.memoria_principal.buscar_bloco(endereco), endereco, Estado.EXCLUSIVE)
            return self.memoria_principal.ler(endereco)
    
    def escrever(self, endereco: int, dado):
        '''
        Escreve um *dado* no *endereco* da memória.
        '''
        linha = self.cache.procurar_linha(endereco)
        if linha is not None: # HIT
            print("\033[92mHit\033[00m")
            if linha.estado == Estado.MODIFIED: # O bloco está na cache e já foi modificado
                linha.dados[endereco % self.cache.tamanho_linha] = dado
            elif linha.estado == Estado.EXCLUSIVE: # O bloco está na cache e é exclusivo
                linha.dados[endereco % self.cache.tamanho_linha] = dado
                linha.estado = Estado.MODIFIED
            elif linha.estado == Estado.SHARED or linha.estado == Estado.FORWARD: # O bloco está na cache e é compartilhado
                # Invalida as outras caches que possuem o bloco
                for cache in self.sistema.caches:
                    if cache != self.cache:
                        resposta = cache.procurar_linha(endereco)
                        if resposta is not None:
                            cache.invalidar_linha(endereco)
                linha.dados[endereco % self.cache.tamanho_linha] = dado
                linha.estado = Estado.MODIFIED
        else: # MISS
            print("\033[91mMiss\033[00m")
            # Procura o bloco nas caches dos outros processadores
            print("\nBuscando bloco nas outras caches...")
            for cache in self.sistema.caches:
                if cache != self.cache: # Evita a busca na própria cache
                    resposta = cache.procurar_linha(endereco)
                    if resposta is not None:
                        print("Bloco encontrado na cache de outro processador.")
                        if resposta.estado == Estado.FORWARD or resposta.estado == Estado.SHARED or resposta.estado == Estado.EXCLUSIVE:
                            # Invalida as outras caches que possuem o bloco
                            for cache in self.sistema.caches:
                                if cache != self.cache:
                                    resposta = cache.procurar_linha(endereco)
                                    if resposta is not None:
                                        cache.invalidar_linha(endereco)
                            self.cache.carregar_linha(resposta.dados, endereco, Estado.MODIFIED)
                            return
                        if resposta.estado == Estado.MODIFIED:
                            self.memoria_principal.atualizar_bloco(resposta.dados, endereco)
                            cache.invalidar_linha(endereco)
                            break
            # Se não encontrar o bloco nas caches dos outros processadores, traz da memória principal
            print("Buscando bloco na memória principal...")
            self.cache.carregar_linha(self.memoria_principal.buscar_bloco(endereco), endereco, Estado.MODIFIED)
            linha = self.cache.procurar_linha(endereco)
            linha.dados[endereco % self.cache.tamanho_linha] = dado
