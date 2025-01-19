from enum import Enum
import random

class Raridade(Enum):
    COMUM = 1
    RARO = 2
    ÉPICO = 3
    LENDÁRIO = 4

class Figurinha:
    def __init__(self, id: int, raridade: Raridade):
        self.id = id
        self.raridade = raridade

    def __repr__(self):
        return f"Figurinha {self.id} ({self.raridade.name})"
    
    def __eq__(self, other):
        return self.id == other.id

def cria_figurinhas(qnt_figurinhas: int) -> list[Figurinha]:
    '''
    Cria uma lista de figurinhas aleatórias numeradas de 1 a *qnt_figurinhas*.
    '''
    figurinhas = []
    for i in range(1, qnt_figurinhas + 1):
        figurinhas.append(Figurinha(i, random.choice(list(Raridade))))
    return figurinhas
