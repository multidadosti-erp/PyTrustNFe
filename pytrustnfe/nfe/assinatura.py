# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import signxml
from lxml import etree
from pytrustnfe.certificado import extract_cert_and_key_from_pfx
from signxml import XMLSigner, SignatureMethod, DigestAlgorithm, CanonicalizationMethod


class Assinatura(object):
    def __init__(self, arquivo, senha):
        self.arquivo = arquivo
        self.senha = senha

    def assina_xml(self, xml_element, reference, getchildren=False):
        cert, key = extract_cert_and_key_from_pfx(self.arquivo, self.senha)

        for element in xml_element.iter("*"):
            if element.text is not None and not element.text.strip():
                element.text = None

        signer = XMLSigner(
            method=signxml.methods.enveloped,
            signature_algorithm=SignatureMethod.RSA_SHA256,
            digest_algorithm=DigestAlgorithm.SHA256,
            c14n_algorithm=CanonicalizationMethod.CANONICAL_XML_1_1,
        )

        ns = {}
        ns[None] = signer.namespaces["ds"]
        signer.namespaces = ns

        ref_uri = ("#%s" % reference) if reference else None
        signed_root = signer.sign(
            xml_element, key=key.encode(), cert=cert.encode(), reference_uri=ref_uri
        )
        if reference:
            element_signed = signed_root.find(".//*[@Id='%s']" % reference)
            signature = signed_root.find(
                ".//{http://www.w3.org/2000/09/xmldsig#}Signature"
            )

            if getchildren and element_signed is not None and signature is not None:
                child = element_signed.getchildren()
                child.append(signature)
            elif element_signed is not None and signature is not None:
                parent = element_signed.getparent()
                parent.append(signature)

        signed_root = etree.tostring(signed_root, encoding=str)

        # Corrige erro 588
        # Rejeicao: Nao eh permitida a presenca de caracteres de edicao no inicio/fim da mensagem ou entre as tags da mensagem (Elemento: enviNFe/NFe[1]/Signature/KeyInfo/X509Data/X509Certificate/)
        # o SEFAZ passou a validar se a assinatura possui quebra de linha
        return signed_root.replace('\n', '')