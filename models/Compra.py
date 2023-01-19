from models.Produto import Produto
from models.Vendedor import Vendedor
from models.Nota_fiscal import NotaFiscal
from typing import List


class Compra:
    nota_fiscal: NotaFiscal = None

    def __init__(self, id, data, valor_total,
                 tributos, produtos: List[Produto],
                 vendedor: Vendedor):
        self.id = id
        self.data = data
        self.produtos = produtos
        self.valorTotal = valor_total
        self.vendedor = vendedor

    def to_json(self):
        if isinstance(self, Compra):
            return {"id": self.id, "data": self.data, "produtos": [x.to_json() for x in self.produtos],
                    "valorTotal": self.valorTotal, "vendedor": self.vendedor.to_json()}
