from enum import Enum

class Estado(Enum):
    MODIFIED = "Modified"
    EXCLUSIVE = "Exclusive"
    SHARED = "Shared"
    INVALID = "Invalid"
    FORWARD = "Forward"

class Resposta:
    HIT = 1
    MISS = 2   

class Linha:
    def __init__(self):
        self.tag = None
        self.dados = None
        self.estado = Estado.INVALID

    def __repr__(self):
        return str(self.dados) + ' | Bloco: ' + str(self.tag) + ' | Estado: '+ self.estado.value

class MemoriaCache:
    def __init__(self, tamanho: int, tamanho_linha: int):
        self.tamanho = tamanho
        self.tamanho_linha = tamanho_linha
        self.qnt_linhas = tamanho // tamanho_linha
        self.memoria = [Linha() for _ in range(self.qnt_linhas)]
    
    def __repr__(self):
        buffer = ''
        for i in range(self.qnt_linhas):
            buffer += f'\033[34mLinha {i}:\033[00m {self.memoria[i]}\n'
        return buffer

    def procurar_linha(self, endereco: int):
        '''
        Procura a linha que armazena o *endereco* na cache.
        '''
        tag = endereco // self.tamanho_linha
        for i in range(self.qnt_linhas):
            if self.memoria[i].tag == tag:
                return self.memoria[i]
        return None

    def ler(self, endereco: int):
        '''
        Lê o dado no *endereço* da memória principal e se encontrar, retorna HIT.
        Caso a cache não possua a linha que armazena o *endereço*, retorna MISS.
        '''
        linha = self.procurar_linha(endereco)
        posicao = endereco % self.tamanho_linha
        if linha is not None:
            return linha.dados[posicao], Resposta.HIT
        return None, Resposta.MISS
    
    def carregar_linha(self, bloco, endereco: int, estado: Estado):
        '''
        Carrega o *bloco* da memória principal que possui o *endereco* para uma linha da cache.
        Se a cache estiver cheia, aplica a política de substituição FIFO.
        '''
        tag = endereco // self.tamanho_linha
        for i in range(self.qnt_linhas):
            # Procura se a cache possui uma linha vazia
            if self.memoria[i].estado == Estado.INVALID:
                self.memoria[i].tag = tag
                self.memoria[i].dados = bloco
                self.memoria[i].estado = estado
                return
        self._fifo(tag)

    def envia_memoria(self, endereco: int):
        '''
        Envia o bloco da cache para a memória principal.
        '''
        tag = endereco // self.tamanho_linha
        for i in range(self.qnt_linhas):
            if self.memoria[i].tag == tag:
                self.memoria[i].estado = Estado.FORWARD
                return