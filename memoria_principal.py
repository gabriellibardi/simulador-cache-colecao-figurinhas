class MemoriaPrincipal:
    def __init__(self, tamanho: int):
        self.tamanho = tamanho
        self.memoria = [0] * tamanho

    def ler(self, endereco):
        '''
        Retorna o dado no *endereço* da memória.
        '''
        return self.memoria[endereco]
    
    def escrever(self, endereço, dado):
        '''
        Escreve o *dado* no *endereço* da memória.
        '''
        self.memoria[endereço] = dado

    def __repr__(self):
        buffer = ''
        for i in range(self.tamanho):
            buffer += '\033[34m{:>3} \033[00m{:<}\n'.format(str(i), str(self.memoria[i]))
        return buffer
