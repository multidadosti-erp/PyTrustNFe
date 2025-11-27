"""Assinatura NFSe (Goiânia) usando signxml vendorizado compartilhado.

Reutiliza loader de NFSe genérica evitando dependência direta de xmlsec.
"""
from lxml import etree
from pytrustnfe.certificado import extract_cert_and_key_from_pfx
from pytrustnfe.nfse.assinatura import XMLSigner, methods


class Assinatura(object):

    def __init__(self, arquivo, senha):
        self.arquivo = arquivo
        self.senha = senha

    def assina_xml(self, xml_element):
        cert, key = extract_cert_and_key_from_pfx(self.arquivo, self.senha)

        for element in xml_element.iter("*"):
            if element.text is not None and not element.text.strip():
                element.text = None

        signer = XMLSigner(
            method=methods.enveloped,
            signature_algorithm="rsa-sha1",
            digest_algorithm="sha1",
            c14n_algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315",
        )

        ns = {}
        ns[None] = signer.namespaces["ds"]
        signer.namespaces = ns
        element_signed = xml_element.find(".//{http://nfse.goiania.go.gov.br/xsd/nfse_gyn_v02.xsd}Rps")
        signed_root = signer.sign(
            xml_element, key=key.encode(), cert=cert.encode()
        )
        signature = signed_root.find(
            ".//{http://www.w3.org/2000/09/xmldsig#}Signature"
        )

        if element_signed is not None and signature is not None:
            parent = xml_element.getchildren()[0]
            parent.append(signature)

        return etree.tostring(xml_element, encoding=str)
