"""Demo de assinatura de CancelarNfseV3 (GINFES).

Uso:
  python -m pytrustnfe.nfse.ginfes.test_ginfes_cancel_demo caminho.pfx SENHA [NUMERO_NFSE]

Gera XML mínimo de cancelamento e aplica assinatura enveloped.
"""
from __future__ import annotations

import sys
import os
from pytrustnfe.certificado import Certificado
from pytrustnfe.nfse.ginfes import xml_cancelar_nfse


def build_kwargs(numero_nfse: str):
    return {
        "emissor": "ginfes",
        "cancelamento": {
            "numero_nfse": numero_nfse,
            "cnpj_prestador": "12345678000199",
            "inscricao_municipal": "1234567",
        },
    }


def main():
    if len(sys.argv) < 3:
        print("Uso: python -m pytrustnfe.nfse.ginfes.test_ginfes_cancel_demo caminho.pfx SENHA [NUMERO_NFSE]")
        sys.exit(1)
    pfx_path = sys.argv[1]
    senha = sys.argv[2]
    numero_nfse = sys.argv[3] if len(sys.argv) > 3 else "999"
    if not os.path.isfile(pfx_path):
        print("Arquivo PFX não encontrado:", pfx_path)
        sys.exit(2)
    with open(pfx_path, "rb") as f:
        pfx_bytes = f.read()
    certificado = Certificado(pfx_bytes, senha)
    kwargs = build_kwargs(numero_nfse)
    xml_assinado = xml_cancelar_nfse(certificado, **kwargs)
    print("XML Cancelamento Assinado (primeiros 500 chars):")
    txt = xml_assinado[:500] + ("..." if len(xml_assinado) > 500 else "")
    print(txt)


if __name__ == "__main__":
    main()
