from bs4 import BeautifulSoup
from models.Vendedor import Vendedor
from models.Produto import Produto
from models.Compra import Compra
import requests

VALID_LINK_ROOT = 'app.sefaz.es.gov.br/ConsultaNFCe'


def get_nota_id(link):
    idx_init = link.find("=")
    idx_fim = link.find("%")
    return link[idx_init + 1:idx_fim]


def listar_compras(produtos):
    ret = ""
    for prod in produtos:
        ret += ", \n " + prod.nome
    return ret


def parse_compra_sefaz(body: str, uri: str) -> Compra:
    """
    Parses HTML body into Compra object.
    :param page: HTML body of returned request to be parsed.
    :return: Compra Object filled with sales information.
    """
    soup = BeautifulSoup(body, 'html.parser')
    invalid_qr_code_sefaz = soup.find_all(text='QR Code Inválido.')

    if invalid_qr_code_sefaz:
        raise ValueError("SEFAZ could not find the sales description.")

    # dados da compra (data da compra.)
    tag_info = soup.find("div", {"id": "infos"})
    info = tag_info.find("li").get_text()
    idx_init = info.find("/") - 2
    idx_fim = info.find("-") - 2
    data_compra = info[idx_init:idx_fim]
    # id nota
    nota_id = get_nota_id(uri)
    # tributos
    # tributos = soup.find("span",{"class":"totalNumb txtObs"}).get_text() #nem toda nota fiscal mostra tributos.
    tributos = 0
    # valor_total
    valor_total = soup.find("span", {"class": "totalNumb txtMax"}).get_text()

    # dados do vendedor
    tag_vendendor = soup.find("div", {"class": "txtCenter"})
    tagged_data = tag_vendendor.find_all("div")
    vendedor_name = tagged_data[0].get_text().replace("\n", " ")
    vendedor_cnpj = ''.join(tagged_data[1].get_text().split())
    vendedor_endereco = ''.join(tagged_data[2].get_text().split())
    vendedor = Vendedor(vendedor_name, vendedor_cnpj, vendedor_endereco)
    # dados da compra realizada
    lista_compras = soup.find("table", {"id": "tabResult"})
    itens = lista_compras.find_all("tr")
    lista_produtos = []
    for item in itens:
        # cada item da compra
        prod_nome = item.find("span", {"class": "txtTit"}).get_text().strip()
        prod_cod = item.find("span", {"class": "RCod"}).get_text().strip()[9:-1]
        prod_qtd = item.find("span", {"class": "Rqtd"}).get_text().strip()[6:]
        prod_preco = item.find("span", {"class": "RvlUnit"}).get_text().strip()[11:]
        prod = Produto(prod_nome, prod_cod, prod_qtd, prod_preco)
        lista_produtos.append(prod)

    compra = Compra(nota_id, data_compra, valor_total, tributos, lista_produtos, vendedor)
    return compra


def fetch_and_parse_sefaz_link(url) -> Compra:
    """
    Fetch and Parse SEFAZ ES site into a Sales object (Compra)
    :param url: ES Sefaz Link to be fetched and parsed
    :return: Compra object filled with Sales data, or error object.
    """
    if not url:
        raise ValueError("url must be provided.");

    if len(url) > len(VALID_LINK_ROOT) and VALID_LINK_ROOT in url:
        page = requests.get(url)
        if page.status_code and page.status_code == 200:
            compra = parse_compra_sefaz(body=page.text, uri=url)
        else:
            raise ValueError("url unreachable or broken.")
        # pass
    else:
        raise TypeError("Url is incomplete or it does not match SEFAZ_ES URL path. provided URI >> {} \n".format(url))

    return compra
