from memoria_principal import MemoriaPrincipal
from memoria_cache import MemoriaCache
from processador import Processador

class Sistema:
    def __init__(self, quantidade_processadores, tamanho_memoria_principal, tamanho_cache, tamanho_linha_cache, total_figurinhas):
        self.memoria_principal = MemoriaPrincipal(tamanho_memoria_principal, tamanho_linha_cache)
        self.caches = [MemoriaCache(tamanho_cache, tamanho_linha_cache, self.memoria_principal) for _ in range(quantidade_processadores)]
        self.processadores = [Processador(i + 1, cache, self.memoria_principal, self) for i, cache in enumerate(self.caches)]
        self.total_figurinhas = total_figurinhas

    def executar(self):
        print("\n\033[92m-=-=-=-=-=-= SIMULADOR DE COLEÇÃO COMPARTILHADA DE FIGURINHAS =-=-=-=-=-=-\033[00m\n")
        while True:
            print(">>> Escolha um usuário para acessar:\n")
            for i in range(1, len(self.processadores) + 1):
                print(f"\033[93m{i}:\033[00m Usuário {i}")
            print("\033[93mm:\033[00m Mostrar coleção")
            print("\033[93mq:\033[00m Sair")
            escolha = input("\n> ")

            if escolha == 'q':
                print("Sistema finalizado.")
                return
            elif escolha == 'm':
                print("Memória principal:\n")
                print(self.memoria_principal)
            else:
                try:
                    processador_id = int(escolha) - 1
                    self.processadores[processador_id].executar()
                except (ValueError, IndexError):
                    print("\n\033[91mOpção Inválida.\033[00m")
