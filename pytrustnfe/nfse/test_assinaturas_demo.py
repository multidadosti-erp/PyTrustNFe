"""Teste de assinaturas NFSe para provedores (Goiânia, MGA, BH, Ginfes).

Uso:
    python -m pytrustnfe.nfse.test_assinaturas_demo /caminho/certificado.pfx SENHA

Opcional:
    PROVEDORES="goiania,mga,bh,ginfes" python -m pytrustnfe.nfse.test_assinaturas_demo pfx senha

Requisitos:
 - PFX válido contendo chave e certificado.
 - Dependências já instaladas (lxml, signxml vendorizado).

Objetivo:
 - Gerar XML mínimo por provedor e aplicar assinatura.
 - Exibir presença e posição de <Signature>.
 - Facilitar diagnóstico pós-atualização de lxml / signxml.
"""
from __future__ import annotations

import sys
import os
from lxml import etree

from pytrustnfe.nfse.assinatura import Assinatura as AssinaturaGenerica
import importlib.util
import pathlib

_BASE = pathlib.Path(__file__).parent


def _load_assinatura_local(subdir: str):
    """Carrega classe Assinatura de um módulo assinatura.py sem executar __init__ do pacote NFSe.

    Evita dependências extras (jinja2, suds, zeep) que não são necessárias
    para o teste de assinatura.
    """
    mod_path = _BASE / subdir / "assinatura.py"
    spec = importlib.util.spec_from_file_location(f"nfse_{subdir}_assinatura", str(mod_path))
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)  # type: ignore
    return getattr(module, "Assinatura")


AssinaturaGoiania = _load_assinatura_local("goiania")
AssinaturaMGA = _load_assinatura_local("mga")
AssinaturaBH = _load_assinatura_local("bh")


def xml_goiania():
    ns = "http://nfse.goiania.go.gov.br/xsd/nfse_gyn_v02.xsd"
    root = etree.Element(f"{{{ns}}}EnviarLoteRpsEnvio")
    lote = etree.SubElement(root, f"{{{ns}}}LoteRps")
    rps = etree.SubElement(lote, f"{{{ns}}}Rps")
    etree.SubElement(rps, f"{{{ns}}}InfRps", Id="RPS0001")
    return root


def xml_mga():
    ns = "http://www.mga.gov.br/nfse"
    root = etree.Element(f"{{{ns}}}EnviarLoteRpsEnvio")
    bloco = etree.SubElement(root, f"{{{ns}}}LoteRps")
    interno = etree.SubElement(bloco, f"{{{ns}}}Rps", Id="RPSMGA1")
    etree.SubElement(interno, f"{{{ns}}}Dummy")
    return root


def xml_bh():
    ns = "http://bh.gov.br/nfse"
    root = etree.Element(f"{{{ns}}}PedidoConsultaNfse")
    etree.SubElement(root, f"{{{ns}}}Identificacao", Id="BHID1")
    return root


def xml_ginfes():
    ns = "http://www.ginfes.com.br/servico_consultar_nfse_envio"
    root = etree.Element(f"{{{ns}}}ConsultarNfseEnvio")
    etree.SubElement(root, f"{{{ns}}}Prestador", Id="GINFES1")
    return root


PROVEDOR_FUNCS = {
    "goiania": (xml_goiania, AssinaturaGoiania, True),
    "mga": (xml_mga, AssinaturaMGA, True),
    "bh": (xml_bh, AssinaturaBH, True),
}


def assinar(provedor: str, pfx: str, senha: str):
    build_fn, cls, needs_reference = PROVEDOR_FUNCS[provedor]
    xml_elem = build_fn()
    with open(pfx, 'rb') as f:
        pfx_bytes = f.read()
    assinatura = cls(pfx_bytes, senha)
    # alguns provedores esperam referência (Id). Usamos o primeiro atributo Id encontrado
    ref = None
    if needs_reference:
        id_node = xml_elem.xpath("//*[@Id]")
        if id_node:
            ref = id_node[0].get("Id")

    try:
        if provedor == "goiania":
            signed = assinatura.assina_xml(xml_elem)
        else:
            signed = assinatura.assina_xml(xml_elem, ref or "")
    except Exception as e:
        return provedor, False, f"ERRO: {e}", None

    has_sig = "<Signature" in signed
    return provedor, has_sig, "OK" if has_sig else "Sem Signature", signed[:400] + ("..." if len(signed) > 400 else "")


def main():
    if len(sys.argv) < 3:
        print("Uso: python -m pytrustnfe.nfse.test_assinaturas_demo /caminho/certificado.pfx SENHA")
        sys.exit(1)
    pfx = sys.argv[1]
    senha = sys.argv[2]

    if not os.path.isfile(pfx):
        print("Arquivo PFX não encontrado:", pfx)
        sys.exit(2)

    selecionados = os.getenv("PROVEDORES", "goiania,mga,bh").split(",")
    print("Provedores alvo:", selecionados)
    print("================ RESULTADOS ================")
    for prov in selecionados:
        prov = prov.strip().lower()
        if prov not in PROVEDOR_FUNCS:
            print(f"[SKIP] Provedor desconhecido: {prov}")
            continue
        nome, ok, msg, snippet = assinar(prov, pfx, senha)
        status = "SUCESSO" if ok else "FALHA"
        print(f"[{status}] {nome}: {msg}")
        if snippet:
            print(f"  Snippet: {snippet}")


if __name__ == "__main__":
    main()
