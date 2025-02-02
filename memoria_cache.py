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
    def __init__(self, tamanho: int, tamanho_linha: int, sistema):
        self.tamanho = tamanho
        self.tamanho_linha = tamanho_linha
        self.qnt_linhas = tamanho // tamanho_linha
        self.memoria = [Linha() for _ in range(self.qnt_linhas)]
        self.fila = []
        self.sistema = sistema
    
    def __repr__(self):
        buffer = ''
        for i in range(self.qnt_linhas):
            buffer += f'\033[34mLinha {i}:\033[00m {self.memoria[i]}\n'
        return buffer

    def procurar_linha(self, endereco: int):
        '''
        Procura a linha que armazena o *endereco* na cache, retornando a linha se encontrada.
        Caso a linha não seja encontrada, ou seja inválida, retorna None.
        '''
        tag = endereco // self.tamanho_linha
        for i in range(self.qnt_linhas):
            if self.memoria[i].tag == tag and self.memoria[i].estado != Estado.INVALID:
                return self.memoria[i]
        return None

    def ler(self, endereco: int):
        '''
        Lê o dado no *endereço* da memória principal e se encontrar, retorna HIT.
        Caso a cache não possua a linha que armazena o *endereço*, retorna MISS.
        '''
        linha = self.procurar_linha(endereco)
        posicao = endereco % self.tamanho_linha
        if linha is not None and linha.estado != Estado.INVALID:
            return linha.dados[posicao], Resposta.HIT
        return None, Resposta.MISS

    def carregar_linha(self, bloco, endereco: int, estado: Estado):
        '''
        Carrega o *bloco* da memória principal que possui o *endereco* para uma linha da cache.
        Se a cache estiver cheia, aplica a política de substituição FIFO.
        Caso a linha a ser substituída esteja no estado MODIFIED, atualiza o bloco na memória principal.
        '''
        tag = endereco // self.tamanho_linha
        for i in range(self.qnt_linhas):
            # Procura se a cache possui uma linha inválida
            if self.memoria[i].estado == Estado.INVALID:
                self.memoria[i].tag = tag
                self.memoria[i].dados = bloco.copy()
                self.memoria[i].estado = estado
                self.fila.append(i)
                return
        # Se a cache estiver cheia, aplica a política de substituição FIFO
        index_fifo = self.fila.pop(0)
        # Se a linha a ser substituída estiver no estado MODIFIED, atualiza o bloco na memória principal
        if self.memoria[index_fifo].estado == Estado.MODIFIED:
            endereco_substituido = self.memoria[index_fifo].tag * self.tamanho_linha
            self.sistema.memoria_principal.atualizar_bloco(self.memoria[index_fifo].dados, endereco_substituido)
        # Se a linha a ser substituída estiver no estado FORWARD, alguma outra cache que possui o bloco e
        # está no estado SHARED, irá para o estado FORWARD
        elif self.memoria[index_fifo].estado == Estado.FORWARD:
            self.promover_shared_para_forward(self.memoria[index_fifo].tag)
        self.memoria[index_fifo].tag = tag
        self.memoria[index_fifo].dados = bloco
        self.memoria[index_fifo].estado = estado
        self.fila.append(index_fifo)

    def promover_shared_para_forward(self, tag: int):
        '''
        Promove uma linha SHARED para FORWARD em outra cache que compartilha a mesma linha.
        '''
        for cache in self.sistema.caches:
            if cache != self:
                for linha in cache.memoria:
                    if linha.tag == tag and linha.estado == Estado.SHARED:
                        linha.estado = Estado.FORWARD
                        return

    def invalidar_linha(self, endereco: int):
        '''
        Invalida a linha que armazena o *endereco* na cache, tirando a linha da fila.
        '''
        tag = endereco // self.tamanho_linha
        for i in range(self.qnt_linhas):
            if self.memoria[i].tag == tag:
                self.memoria[i].estado = Estado.INVALID
                if i in self.fila:
                    self.fila.remove(i)
                return

    def atualizar_linha(self, endereco: int, dado):
        '''
        Atualiza o dado na linha que armazena o *endereco* na cache.
        '''
        tag = endereco // self.tamanho_linha
        for i in range(self.qnt_linhas):
            if self.memoria[i].tag == tag:
                self.memoria[i].dados[endereco % self.tamanho_linha] = dado
                return
