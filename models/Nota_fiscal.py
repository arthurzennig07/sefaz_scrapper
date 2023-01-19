"""
Modelo da nota fiscal
"""
import datetime
from Services import scrap_sefaz_link as _scrap
# from Services import database
import json

test_link = "http://app.sefaz.es.gov.br/ConsultaNFCe?p=32210506626253113436650030001097981000120222%7C2%7C1%7C1%7C304bbbe70806276f170673e948bfb711b37cc610"


class NotaFiscal:
    ano: int = 1800
    mes: int = 99
    cnpj: str = "0000000000"
    isParsable: bool = False      #Link consegue ser mapeado como se fosse da Sefaz ES?
    isReachable: bool = False   #Link leva à Sefaz ES?
    isValid: bool = False       #Link leve à Sefaz ES e lá, entrega dados da compra?
    serie_nfe: str = "001"
    numero_nfe: str = "000000000"
    att_desconhecido0: str = "00"
    att_desconhecido1: str = "00"
    att_desconhecido2: str = "1000"
    att_desconhecido3: str = "000000"
    prefixo_link: str = "--"
    sufixo_link: str = "--"
    usr: str = ""

    def __init__(self, link, file_name):
        self.link = link
        self.isParsable = False
        self.isReachable = self.check_link_validity()
        self.file_name = file_name

    def parse(self):
        try:
            self.prefixo_link, self.sufixo_link = _scrap.divide_link(self.link)
            self.ano, self.mes = _scrap.parse_elementos_data(self.sufixo_link)
            self.cnpj = _scrap.parse_elementos_vendedor(self.sufixo_link)
            self.att_desconhecido0, self.att_desconhecido1, \
            self.att_desconhecido2, self.att_desconhecido3 = _scrap.parse_elementos_nota_desconhecido(self.sufixo_link)
            self.serie_nfe, self.numero_nfe = _scrap.parse_elementos_nota(self.sufixo_link)
            self.isParsable = True
        except:
            print("deu erro ao mapear codigo do link.")

    def check_link_validity(self) -> bool:
        self.isReachable = _scrap.check_is_valid_link(self.link)
        return self.isReachable

    def bad_link_tojson(self, usr) -> str:
        _data = {
            "user_id": usr
            , "link_from_qr_image": self.link
            , "isReachable": self.isReachable
            , "time_utc": str(datetime.datetime.utcnow())
            , "file_name": str(self.file_name)
        }
        d = json.loads(json.dumps(_data))
        return d

    def export_tojson(self):
        _data = {
            "user_id": self.usr
            , "link_emissao": self.link
            , "prefixo_link": self.prefixo_link
            , "sufixo_link": self.sufixo_link
            , "ano_emissao": self.ano
            , "mes_emissao": self.mes
            , "cnpj_emissao": self.cnpj
            , "isParsable": self.isParsable
            , "isReachable": self.isReachable
            , "serie_nfe": self.serie_nfe
            , "numero_nfe": self.numero_nfe
            , "atributo_desconhecido1": self.att_desconhecido0
            , "atributo_desconhecido2": self.att_desconhecido1
            , "atributo_desconhecido3": self.att_desconhecido2
            , "atributo_desconhecido4": self.att_desconhecido3
            , "data_processamento": str(datetime.datetime.utcnow())
            , "telegram_file_name": str(self.file_name)
        }
        d = json.loads(json.dumps(_data))
        return d

"""
nf = NotaFiscal(test_link)
nf.parse()
database.insert_mongo("processedLinks", nf.export_tojson(1873300))
print("finalizado")
"""