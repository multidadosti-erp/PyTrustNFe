"""assinatura.py
=================

Responsável por realizar a assinatura digital dos XMLs da NF-e utilizando a
biblioteca ``signxml``. Este módulo prioriza o uso de uma versão vendorizada
``signxml 2.9.0`` (copiada para ``_vendor/signxml_290``) para manter
compatibilidade com algoritmos baseados em **SHA1** exigidos pelos esquemas
atuais da NF-e (que ainda fixam ``rsa-sha1`` e ``sha1``). Caso a versão
vendorizada não esteja disponível, faz fallback para a versão instalada no
ambiente virtual.

Principais pontos:
------------------
1. Carregamento dinâmico da biblioteca (vendor > ambiente).
2. Assinatura sempre usando método enveloped.
3. Ajuste do namespace para tornar o prefixo ``ds`` namespace default, mantendo
    compatibilidade com estruturas esperadas em validações legadas.
4. Limpeza de textos em branco (normalização) para evitar divergência na
    canonicalização antes do cálculo do digest.
5. Retorno do XML assinado sem quebras de linha para evitar rejeições (ex.: erro 588).

Segurança:
----------
O uso de SHA1 permanece apenas por demanda do schema da NF-e. Para cenários em
que for permitido migrar, recomenda-se atualizar o processo para algoritmos
mais fortes (ex.: SHA256) ajustando também os XSD/validações envolvidos.

Função principal:
-----------------
``Assinatura.assina_xml(xml_element, reference, getchildren=False)``
     - ``xml_element``: Element raiz ou nó contendo a estrutura da NF-e.
     - ``reference``: Valor do atributo ``Id`` do elemento que será referenciado
        (ex.: ``NFe<chave>``).
     - ``getchildren``: Mantido conforme lógica histórica (inserção distinta da
        tag ``Signature``); normalmente ``False``.

Retorna ``str`` com o XML assinado (sem quebras de linha). Em caso de falha na
biblioteca de assinatura, a exceção original de ``signxml`` será propagada.

Nota importante:
----------------
Este módulo não valida o XML contra XSD; foca exclusivamente na assinatura.
Para validação, utilize processo separado com os schemas oficiais da SEFAZ.
"""
# © 2016 Danimar Ribeiro, Trustcode
# © 2025 Augusto Costa, Multidados
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import sys
import pathlib
from lxml import etree
from pytrustnfe.certificado import extract_cert_and_key_from_pfx

def _load_signxml():
    """Carrega o módulo ``signxml``.

    Ordem de resolução:
        1. Diretório vendorizado ``_vendor/signxml_290`` (versão 2.9.0).
        2. Import padrão do ambiente (qualquer versão instalada via requirements).

    Retorna:
        Module: referência ao módulo ``signxml`` (vendor ou ambiente).

    Observações:
        - O path vendorizado é inserido temporariamente no ``sys.path`` e
          removido imediatamente após o import para minimizar efeito colateral.
        - Não realiza pinagem rígida caso a estrutura vendorizada esteja
          incompleta; simplesmente cai para o módulo já instalado.
    """
    vendor_base = pathlib.Path(__file__).parent / '_vendor' / 'signxml_290'
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
    """Realiza assinatura digital de XML NF-e.

    Parâmetros do construtor:
        arquivo (str | bytes): Caminho para o arquivo PFX contendo certificado.
        senha (str): Senha do PFX.
    """

    def __init__(self, arquivo, senha):
        self.arquivo = arquivo
        self.senha = senha

    def assina_xml(self, xml_element, reference, getchildren=False):
        """Assina o XML informado usando método enveloped.

        Args:
            xml_element (etree._Element): Elemento raiz (geralmente <NFe>). Pode
                ser também elemento mais interno, mantendo compatibilidade
                histórica.
            reference (str): Valor do atributo ``Id`` para construir o
                ``reference_uri`` ("#<Id>"). Normalmente a chave completa da NF-e.
            getchildren (bool): Preserva comportamento legado de inserção da
                assinatura dependendo de hierarquia; mantenha ``False`` se não
                houver necessidade específica.

        Returns:
            str: XML assinado sem quebras de linha (adequado para envio).

        Raises:
            signxml.exceptions.*: Erros de assinatura (ex.: chave/cert inválidos).

        Processo:
            1. Extrai chave e certificado do PFX.
            2. Normaliza textos vazios.
            3. Configura ``XMLSigner`` com algoritmos SHA1 (NF-e atual).
            4. Ajusta namespace default para ``ds`` conforme implementação prévia.
            5. Executa assinatura enveloped.
            6. Opcionalmente reposiciona nó Signature seguindo regra antiga.
            7. Serializa removendo quebras de linha.

        Observação:
            Alterações estruturais pós-assinatura podem invalidar o digest;
            use o parâmetro ``getchildren`` com cautela.
        """
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

        # Tornar namespace ds default (compatível com lógica anterior)
        ns = {None: signer.namespaces["ds"]}
        signer.namespaces = ns

        ref_uri = f"#{reference}" if reference else None
        signed_root = signer.sign(
            xml_element,
            key=key.encode(),
            cert=cert.encode(),
            reference_uri=ref_uri,
        )

        if reference:
            element_signed = signed_root.find(f".//*[@Id='{reference}']")
            signature = signed_root.find(
                ".//{http://www.w3.org/2000/09/xmldsig#}Signature"
            )
            if getchildren and element_signed is not None and signature is not None:
                element_signed.getchildren().append(signature)
            elif element_signed is not None and signature is not None:
                element_signed.getparent().append(signature)

        xml_bytes = etree.tostring(signed_root, encoding=str)
        return xml_bytes.replace('\n', '')
