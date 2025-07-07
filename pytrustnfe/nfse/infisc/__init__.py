import os
from base64 import b64encode

from lxml import etree

# import suds
from OpenSSL import crypto
from pytrustnfe.certificado import extract_cert_and_key_from_pfx, save_cert_key
from pytrustnfe.client import get_authenticated_client
from pytrustnfe.nfse.assinatura import Assinatura
from pytrustnfe.xml import render_xml, sanitize_response
from requests import Session
from zeep import Client
from zeep.transports import Transport

# def sign_tag(certificado, **kwargs):
#     pkcs12 = crypto.load_pkcs12(certificado.pfx, certificado.password)
#     key = pkcs12.get_privatekey()
#     if "nfse" in kwargs:
#         for item in kwargs["nfse"]["lista_rps"]:
#             signed = crypto.sign(key, item["assinatura"], "SHA1")
#             item["assinatura"] = b64encode(signed)
#     if "cancelamento" in kwargs:
#         signed = crypto.sign(key, kwargs["cancelamento"]["assinatura"], "SHA1")
#         kwargs["cancelamento"]["assinatura"] = b64encode(signed)


def _get_url(**kwargs):

    try:
        cod_cidade = kwargs["nfse"]["cidade"]
    except (KeyError, TypeError):
        raise KeyError("Código de cidade inválido!")

    urls = {
        # Caxias do Sul - RS
        "5108": {
            "homologacao": "https://nfsehomol.caxias.rs.gov.br/services/nfse/ws/Servicos.wsdl",
            "producao": "https://nfse.caxias.rs.gov.br/services/nfse/ws/Servicos.wsdl",
        }
    }

    try:
        return urls[str(cod_cidade)]
    except KeyError:
        raise KeyError(f"INFSC não emite notas da cidade {cod_cidade}!")


def _render(certificado, method, **kwargs):
    path = os.path.join(os.path.dirname(__file__), "templates")
    xml_send = render_xml(path, f"{method}.xml", True, **kwargs)

    # import ipdb; ipdb.set_trace()  # noqa


    if not isinstance(xml_send, str):
        xml_send = etree.tostring(xml_send)

    # Este metodo nao precisa de assinatura
    # if method == "ConsultarNfsePorRps":
    #     return xml_send

    # reference = ""
    # ref_lote = ""

    cert, key = extract_cert_and_key_from_pfx(certificado.pfx, certificado.password)
    cert, key = save_cert_key(cert, key)

    # if method == "GerarNfse":
    #     reference = "rps:%s" % kwargs["rps"]["numero"]
    #     ref_lote = "lote%s" % kwargs["rps"]["numero_lote"]

    # elif method == "CancelarNfse":
    #     reference = "pedidoCancelamento_%s" % kwargs["cancelamento"]["numero_nfse"]

    signer = Assinatura(cert, key, certificado.password)

    xml_send = signer.assina_xml(xml_send, "")

    # if ref_lote:
    #     xml_send = signer.assina_xml(etree.fromstring(xml_send), ref_lote)

    return xml_send


def _send(certificado, method, **kwargs):
    path = os.path.join(os.path.dirname(__file__), "templates")

    # if method in (
    #     "GerarNfse",
    #     "RecepcionarLoteRps",
    #     "RecepcionarLoteRpsSincrono",
    #     "CancelarNfse",
    #     "SubstituirNfse",
    # ):
    #     sign_tag(certificado, **kwargs)

    url = _get_url(**kwargs)

    # if kwargs["emissor"] == "":
    #
    #     # fortaleza utiliza webservice diferente
    #     if kwargs["ambiente"] == "producao":
    #         base_url = "https://iss.fortaleza.ce.gov.br/grpfor-iss/ServiceGinfesImplService?wsdl"
    #     else:
    #         base_url = "http://isshomo.sefin.fortaleza.ce.gov.br/grpfor-iss/ServiceGinfesImplService?wsdl"
    #
    #     # o servico de cancelamento de fortaleza tem outro nome
    #     if method == "CancelarNfseV3":
    #         method = "CancelarNfse"
    #
    # else:
    #
    #     if kwargs["ambiente"] == "producao":
    #         base_url = "https://producao.ginfes.com.br/ServiceGinfesImpl?wsdl"
    #     else:
    #         base_url = "https://homologacao.ginfes.com.br/ServiceGinfesImpl?wsdl"
    #
    # if kwargs["ambiente"] == "producao":
    #     url = "http://e-gov.betha.com.br/e-nota-contribuinte-test-ws/nfseWS?wsdl"
    # else:
    #     url = "http://e-gov.betha.com.br/e-nota-contribuinte-ws/nfseWS?wsdl"

    # xml_send = _render(path, method, **kwargs)

    xml_send = kwargs["xml"]
    # xml_cabecalho = '<?xml version="1.0" encoding="UTF-8"?>\
    # <cabecalho xmlns="http://www.abrasf.org.br/nfse.xsd" versao="1.00">\
    # <versaoDados>1.00</versaoDados></cabecalho>'

    cert, key = extract_cert_and_key_from_pfx(certificado.pfx, certificado.password)

    cert, key = save_cert_key(cert, key)

    session = Session()
    session.cert = (cert, key)
    session.verify = False

    transport = Transport(session=session)
    client = Client(url, transport=transport)

    response, obj = sanitize_response(client.service[method](xml_send))

    return {
        "sent_xml": xml_send,
        "received_xml": response,
        "object": obj,
    }


# def gerar_nfse(certificado, **kwargs):
#     return _send(certificado, "GerarNfse", **kwargs)


# def enviar(certificado, **kwargs):
#     if "xml" not in kwargs:
#         kwargs["xml"] = xml_enviar(certificado, **kwargs)
#     return _send(certificado, "enviar", **kwargs)


def xml_envio_lote_rps(certificado, **kwargs):
    return _render(certificado, "EnvioLote", **kwargs)


def envio_lote_rps(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs["xml"] = xml_envio_lote_rps(certificado, **kwargs)

    return _send(certificado, "EnvioLote", **kwargs)


# def envio_lote_rps(certificado, **kwargs):
#     return _send(certificado, "RecepcionarLoteRpsSincrono", **kwargs)
#

# def cancelar_nfse(certificado, **kwargs):
#     return _send(certificado, "CancelarNfse", **kwargs)


# def substituir_nfse(certificado, **kwargs):
#     return _send(certificado, "SubstituirNfse", **kwargs)
#

# def consulta_situacao_lote_rps(certificado, **kwargs):
#     return _send(certificado, "ConsultaSituacaoLoteRPS", **kwargs)


# def consulta_nfse_por_rps(certificado, **kwargs):
#     return _send(certificado, "ConsultaNfsePorRps", **kwargs)


# def consultar_lote_rps(certificado, **kwargs):
#     return _send(certificado, "ConsultarLoteRps", **kwargs)
#

# def consulta_nfse_servico_prestado(certificado, **kwargs):
#     return _send(certificado, "ConsultarNfseServicoPrestado", **kwargs)
#
#
# def consultar_nfse_servico_tomado(certificado, **kwargs):
#     return _send(certificado, "ConsultarNfseServicoTomado", **kwargs)
#

# def consulta_nfse_faixe(certificado, **kwargs):
#     return _send(certificado, "ConsultarNfseFaixa", **kwargs)
#

# def consulta_cnpj(certificado, **kwargs):
#     return _send(certificado, "ConsultaCNPJ", **kwargs)
