'''
analisa os dados do link do sefaz
e.g.
http://app.sefaz.es.gov.br/ConsultaNFCe/qrcode.aspx?p=32210113469300000166650010004337771005062012%7C2%7C1%7C1%7C2E6E0BD2DE1A62DE50E0CA009522BB0ABEFC8149
32 21 01 13469300000166 65 0010004337771005062012
http://app.sefaz.es.gov.br/ConsultaNFCe?p=32210506626253113436650030001097981000120222%7C2%7C1%7C1%7C304bbbe70806276f170673e948bfb711b37cc610
onde> 32 21 05 06626253113436 65 003 000109798 1000 120222
32 - nao sei
21 - ano da nota fiscal
05 - mês da nota fiscal
06626253113436 - cnpj da empresa emitiu nota fiscal
65 - não sei
003 - série da e-Nfe
000109798 - número nota fiscal eletronica
1000 - id caixa? (nao sei).
120222 - não sei
'''


def parse_elementos_data(addr: str) -> str:
    _addr = addr
    return _addr[2:4], _addr[4:6]


def parse_elementos_nota(addr: str) -> str:
    _addr = addr
    _serie_notafiscal = _addr[22:25]
    _numero_notafiscal = _addr[25:34]
    return _serie_notafiscal, _numero_notafiscal


def parse_elementos_nota_desconhecido(addr: str) -> str:
    _addr = addr
    desconhecido0 = _addr[:2]
    desconhecido1 = _addr[20:22]
    desconhecido2 = _addr[34:38]
    desconhecido3 = _addr[38:44]
    return desconhecido0, desconhecido1, desconhecido2, desconhecido3


def parse_elementos_vendedor(addr: str) -> str:
    _addr = addr
    cnpj = _addr[6:20]
    return cnpj


def divide_link(addr: str) -> str:
    _addr = addr
    idx_prefixo = _addr.find('?p=')
    idx_sufixo = _addr.find('%7C')  # unicode para "|"

    return _addr[:idx_prefixo + 3], _addr[idx_prefixo + 3: idx_sufixo]


def check_is_valid_link(addr: str) -> bool:
    match = "app.sefaz.es.gov.br/ConsultaNFCe"
    _addr = addr
    try:
        prefix, suf = divide_link(_addr)
        if match in prefix:
            return True
        else:
            return False
    except:
        return False
