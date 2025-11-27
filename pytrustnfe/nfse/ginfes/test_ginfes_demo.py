"""Demo de assinatura GINFES (RecepcionarLoteRpsV3) usando PFX de teste.

Uso:
  python -m pytrustnfe.nfse.ginfes.test_ginfes_demo /caminho/demo_nfse.pfx SENHA

Gera XML mínimo com um RPS e aplica assinatura enveloped (SHA1) via
`pytrustnfe.nfse.assinatura.Assinatura`.
"""
from __future__ import annotations

import sys
import os
from datetime import date
from pytrustnfe.certificado import Certificado
from pytrustnfe.nfse.ginfes import xml_recepcionar_lote_rps


def build_kwargs():
    hoje = date.today().strftime("%Y-%m-%d")
    return {
        "emissor": "ginfes",  # ou 'fortaleza'
        "nfse": {
            "lote_id": "123",
            "numero_lote": "123",
            "cnpj_prestador": "12345678000199",
            "inscricao_municipal": "1234567",
            "lista_rps": [
                {
                    "numero": "1",
                    "serie": "A",
                    "tipo_rps": "1",
                    "data_emissao": hoje,
                    "natureza_operacao": "1",
                    "regime_tributacao": "6",
                    "optante_simples": "2",
                    "incentivador_cultural": "2",
                    "status": "1",
                    "numero_substituido": "",
                    "serie_substituido": "",
                    "tipo_substituido": "",
                    "valor_servico": "100.00",
                    "valor_deducao": "0.00",
                    "valor_pis": "0.00",
                    "valor_cofins": "0.00",
                    "valor_inss": "0.00",
                    "valor_ir": "0.00",
                    "valor_csll": "0.00",
                    "iss_retido": "2",
                    "valor_iss": "0.00",
                    "valor_iss_retido": "0.00",
                    "outras_retencoes": "0.00",
                    "base_calculo": "100.00",
                    "aliquota_issqn": "3.00",
                    "valor_liquido_nfse": "100.00",
                    "desconto_incondicionado": "0.00",
                    "desconto_condicionado": "0.00",
                    "codigo_servico": "0107",
                    "cnae_servico": "6204000",
                    "codigo_tributacao_municipio": "6204000",
                    "descricao": "Serviço de teste",
                    "codigo_municipio": "3550308",  # São Paulo
                    "prestador": {
                        "cnpj": "12345678000199",
                        "inscricao_municipal": "1234567",
                    },
                    "tomador": {
                        "cnpj_cpf": "11111111000191",
                        "inscricao_municipal": "",
                        "razao_social": "Cliente Teste",
                        "logradouro": "Rua X",
                        "numero": "100",
                        "complemento": "Sala 1",
                        "bairro": "Centro",
                        "cidade": "3550308",
                        "uf": "SP",
                        "cep": "01000000",
                        "telefone": "1130000000",
                        "email": "teste@example.com",
                    },
                }
            ],
        },
    }


def main():
    if len(sys.argv) < 3:
        print("Uso: python -m pytrustnfe.nfse.ginfes.test_ginfes_demo caminho.pfx SENHA")
        sys.exit(1)
    pfx_path = sys.argv[1]
    senha = sys.argv[2]
    if not os.path.isfile(pfx_path):
        print("Arquivo PFX não encontrado:", pfx_path)
        sys.exit(2)
    with open(pfx_path, "rb") as f:
        pfx_bytes = f.read()
    certificado = Certificado(pfx_bytes, senha)
    kwargs = build_kwargs()
    xml_assinado = xml_recepcionar_lote_rps(certificado, **kwargs)
    print("XML Assinado (primeiros 500 chars):")
    txt = xml_assinado[:500] + ("..." if len(xml_assinado) > 500 else "")
    print(txt)


if __name__ == "__main__":
    main()
