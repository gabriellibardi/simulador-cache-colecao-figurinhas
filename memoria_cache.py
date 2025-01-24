from enum import Enum
from copy import copy

class Estado(Enum):
    MODIFIED = "Modified"
    EXCLUSIVE = "Exclusive"
    SHARED = "Shared"
    INVALID = "Invalid"
    FORWARD = "Forward"

class Resposta:
    HIT = "\033[92mHit\033[00m"
    MISS = "\033[91mMiss\033[00m"    

class Linha:
    def __init__(self, tag, dados, estado):
        self.tag = tag
        self.dados = dados
        self.estado = estado

    def __repr__(self):
        return str(self.dados) + ' | Bloco: ' + str(self.tag) + ' | Estado: '+ self.estado.value

class MemoriaCache:
    def __init__(self, tamanho: int, tamanho_linha: int):
        self.tamanho = tamanho
        self.tamanho_linha = tamanho_linha
        self.qnt_linhas = tamanho // tamanho_linha
        self.memoria = [Linha(None, [0] * tamanho_linha, Estado.INVALID) for _ in range(self.qnt_linhas)]
    
    def __repr__(self):
        buffer = ''
        for i in range(self.qnt_linhas):
            buffer += f'\033[34mLinha {i}:\033[00m {self.memoria[i]}\n'
        return buffer

    def ler(self, endereco: int):
        '''
        Lê o dado no *endereço* da memória principal e se encontrar, retorna HIT.
        Caso a cache não possua a linha que armazena o *endereço*, retorna MISS.
        '''
        tag = endereco // self.tamanho_linha
        posicao = endereco % self.tamanho_linha
        for i in range(self.qnt_linhas):
            if self.memoria[i].tag == tag:
                return self.memoria[i].dados[posicao], Resposta.HIT
        return None, Resposta.MISS
    
    def carregar_linha(self, bloco, endereco: int):
        '''
        Carrega o *bloco* da memória principal que possui o *endereco* para uma linha da cache.
        Se a cache estiver cheia, aplica a política de substituição FIFO.
        '''
        tag = endereco // self.tamanho_linha
        for i in range(self.qnt_linhas):
            if self.memoria[i].estado == Estado.INVALID:
                self.memoria[i].tag = tag
                self.memoria[i].dados = bloco
                self.memoria[i].estado = Estado.SHARED
                return
        self._fifo(tag)
