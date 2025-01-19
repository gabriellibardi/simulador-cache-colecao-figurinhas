class MemoriaCache:
    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.memoria = [0] * tamanho
    
    def buscar_linha(self, tag):
        '''
        Busca uma linha na cache por sua *tag*. 
        '''
        for i in range(self.tamanho):
            if self.memoria[i][0] == tag:
                return i
            
class Linha:
    def __init__(self, tag, dados):
        self.tag = tag
        self.dados = dados

    def __repr__(self):
        return str(self.dados)