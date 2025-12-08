"""Assinatura de RPS/NFSe.

Atualizado para utilizar a mesma estratégia do módulo de NF-e:
- Prioriza ``signxml`` vendorizado (versão 2.9.0) para evitar problemas de
    compatibilidade entre ``lxml``/``xmlsec``.
- Remove dependência direta de ``xmlsec`` ao usar ``signxml.XMLSigner`` com o
    método enveloped padrão exigido pelos provedores NFSe.

Fluxo resumido:
1. Recebe caminhos para certificado e chave privada (ambos PEM).
2. Normaliza o XML usando ``lxml.etree``.
3. Carrega chave/certificado da filesystem e assina com SHA1 (requisito atual).
4. Retorna string resultante da assinatura.

Observação: apesar do uso de SHA1, mantemos esse algoritmo para compatibilidade
com provedores NFSe que ainda não aceitaram SHA256. Quando possível, avalie
migrar.
"""

# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# © 2025 Augusto Costa, Multidados
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os.path
import pathlib
import sys
import xmlsec
consts = xmlsec.constants
from lxml import etree


def _load_signxml():
    """Carrega signxml (vendorizado 2.9.0 compartilhado com módulo NF-e)."""
    vendor_base = pathlib.Path(__file__).parent.parent / "_vendor" / "signxml_290"
    if vendor_base.exists():
        sys.path.insert(0, str(vendor_base))
        try:
            import signxml as mod  # type: ignore
        finally:
            sys.path.pop(0)
        return mod
    import signxml as mod  # type: ignore

    return mod


_signxml = _load_signxml()
XMLSigner = _signxml.XMLSigner
methods = _signxml.methods


class Assinatura(object):
    """Responsável por assinar mensagens NFSe usando signxml."""

    def __init__(self, cert_pem, private_key, password):
        """Armazena parâmetros para assinatura.

        Args:
            cert_pem (str): Caminho para o certificado público em formato PEM.
            private_key (str): Caminho para a chave privada (PEM) protegida.
            password (str): Senha usada para abrir a chave privada.
        """
        self.cert_pem = cert_pem
        self.private_key = private_key
        self.password = password

    def _checar_certificado(self):
        """Garante que arquivos necessários existem."""
        if not os.path.isfile(self.private_key):
            raise Exception("Caminho do certificado não existe.")

    def assina_xml(self, xml, reference):
        """Assina XML NFSe via signxml enveloped signature."""
        self._checar_certificado()
        template = etree.fromstring(xml)

        key = xmlsec.Key.from_file(
            self.private_key,
            format=xmlsec.constants.KeyDataFormatPem,
            password=self.password,
        )

        signature_node = xmlsec.template.create(
            template,
            c14n_method=consts.TransformInclC14N,
            sign_method=consts.TransformRsaSha1,
        )

        template.append(signature_node)

        ref = xmlsec.template.add_reference(
            signature_node, consts.TransformSha1, uri=""
        )

        xmlsec.template.add_transform(ref, consts.TransformEnveloped)
        xmlsec.template.add_transform(ref, consts.TransformInclC14N)

        ki = xmlsec.template.ensure_key_info(signature_node)
        xmlsec.template.add_x509_data(ki)

        ctx = xmlsec.SignatureContext()
        ctx.key = key
        ctx.key.load_cert_from_file(self.cert_pem, consts.KeyDataFormatPem)
        ctx.sign(signature_node)

        return etree.tostring(template, encoding=str)
