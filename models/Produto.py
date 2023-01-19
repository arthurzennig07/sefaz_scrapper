class Produto:
    def __init__(self, nome, codigo, qtd, valor):
        self.nome = nome
        self.codigo = codigo
        self.quantidade = qtd
        self.valor = valor

    def to_json(self):
        return {"nome": self.nome, "codigo": self.codigo, "quantidade": self.quantidade, "valor": self.valor}
