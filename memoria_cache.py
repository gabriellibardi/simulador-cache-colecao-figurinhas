from enum import Enum
from copy import copy

class Estado(Enum):
    MODIFIED = 'M'
    EXCLUSIVE = 'E'
    SHARED = 'S'
    INVALID = 'I'
    FORWARD = 'F'

class Linha:
    def __init__(self, tag, dados, estado):
        self.tag = tag
        self.dados = dados
        self.estado = estado

    def __repr__(self):
        return str(self.dados)

class MemoriaCache:
    def __init__(self, tamanho: int, tamanho_linha: int):
        self.tamanho = tamanho
        self.tamanho_linha = tamanho_linha
        self.qnt_linhas = tamanho // tamanho_linha
        self.memoria = [Linha(None, [0] * tamanho_linha, Estado.INVALID) for _ in range(self.qnt_linhas)]
    
    def __repr__(self):
        buffer = ''
        for i in range(self.qnt_linhas):
            buffer += f'Linha {i}: {self.memoria[i]}\n'
        return buffer

    def buscar_linha(self, tag):
        '''
        Busca uma linha na cache por sua *tag*. 
        '''
        for i in range(self.tamanho):
            if self.memoria[i][0] == tag:
                return i
