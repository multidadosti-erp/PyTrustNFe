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

from lxml import etree


def _load_signxml():
    """Carrega signxml (vendorizado 2.9.0 compartilhado com módulo NF-e)."""
    vendor_base = pathlib.Path(__file__).parent.parent / '_vendor' / 'signxml_290'
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

        with open(self.private_key, 'rb') as key_file:
            key_data = key_file.read()
        passphrase = self.password.encode() if self.password else None

        with open(self.cert_pem, 'rb') as cert_file:
            cert_data = cert_file.read().decode('utf-8')

        signer = XMLSigner(
            method=methods.enveloped,
            signature_algorithm="rsa-sha1",
            digest_algorithm="sha1",
            c14n_algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315",
        )

        ref_uri = f"#{reference}" if reference else None
        signed_root = signer.sign(
            template,
            key=key_data,
            passphrase=passphrase,
            cert=cert_data,
            reference_uri=ref_uri,
        )

        return etree.tostring(signed_root, encoding=str)