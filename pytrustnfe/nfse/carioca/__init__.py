# © 2018 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
from lxml import etree
from requests import Session
from zeep import Client
from zeep.transports import Transport

from pytrustnfe.certificado import extract_cert_and_key_from_pfx, save_cert_key
from pytrustnfe.nfe.assinatura import Assinatura
from pytrustnfe.xml import render_xml, sanitize_response


def _render(certificado, method, **kwargs):
    path = os.path.join(os.path.dirname(__file__), "templates")
    xml_send = render_xml(path, "%s.xml" % method, True, **kwargs)

    if not isinstance(xml_send, str):
        xml_send = etree.tostring(xml_send)

    # Este metodo nao precisa de assinatura
    if method == 'ConsultarNfsePorRps':
        return xml_send

    reference = ""

    if method == "GerarNfse":
        reference = "r%s" % kwargs["rps"]["numero"]

    elif method == "CancelarNfse":
        reference = "Cancelamento_NF%s" % kwargs["cancelamento"]["numero_nfse"]

    signer = Assinatura(certificado.pfx, certificado.password)
    xml_send = signer.assina_xml(etree.fromstring(xml_send), reference)

    return xml_send


def _send(certificado, method, **kwargs):
    base_url = ""
    if kwargs["ambiente"] == "producao":
        base_url = "https://notacarioca.rio.gov.br/WSNacional/nfse.asmx?wsdl"
    else:
        base_url = "https://notacariocahom.rio.gov.br/WSNacional/nfse.asmx?wsdl"  # noqa

    xml_send = kwargs["xml"]

    cert, key = extract_cert_and_key_from_pfx(
        certificado.pfx, certificado.password)

    cert, key = save_cert_key(cert, key)

    session = Session()
    session.cert = (cert, key)
    session.verify = False
    transport = Transport(session=session)

    client = Client(base_url, transport=transport)

    response = client.service[method](xml_send)

    response, obj = sanitize_response(response)

    return {"sent_xml": xml_send, "received_xml": response, "object": obj}


def xml_gerar_nfse(certificado, **kwargs):
    return _render(certificado, "GerarNfse", **kwargs)


def gerar_nfse(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs["xml"] = xml_gerar_nfse(certificado, **kwargs)
    return _send(certificado, "GerarNfse", **kwargs)


def xml_cancelar_nfse(certificado, **kwargs):
    return _render(certificado, "CancelarNfse", **kwargs)


def cancelar_nfse(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs["xml"] = xml_cancelar_nfse(certificado, **kwargs)
    return _send(certificado, "CancelarNfse", **kwargs)


def xml_consultar_nfse_por_rps(certificado, **kwargs):
    return _render(certificado, "ConsultarNfsePorRps", **kwargs)


def consultar_nfse_por_rps(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs["xml"] = xml_consultar_nfse_por_rps(certificado, **kwargs)
    return _send(certificado, "ConsultarNfsePorRps", **kwargs)