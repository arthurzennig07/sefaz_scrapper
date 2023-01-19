class Vendedor:
    def __init__(self, nome, codigo, endereco):
        super().__init__()
        self.nome = nome
        self.cnpj = codigo
        self.endereco = endereco

    def to_json(self):
        return {"nome": self.nome, "cnpj": self.cnpj, "endereco": self.endereco}
