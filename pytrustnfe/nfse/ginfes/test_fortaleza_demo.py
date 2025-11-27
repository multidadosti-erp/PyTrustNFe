"""Demo Fortaleza (GINFES) para lote e cancelamento.

Uso:
  python -m pytrustnfe.nfse.ginfes.test_fortaleza_demo caminho.pfx SENHA [NUMERO_NFSE]
"""
from __future__ import annotations

import sys
import os
from datetime import date
from pytrustnfe.certificado import Certificado
from pytrustnfe.nfse.ginfes import xml_recepcionar_lote_rps, xml_cancelar_nfse


def build_lote_kwargs():
    hoje = date.today().strftime("%Y-%m-%d")
    return {
        "emissor": "fortaleza",
        "nfse": {
            "lote_id": "F001",
            "numero_lote": "F001",
            "cnpj_prestador": "12345678000199",
            "inscricao_municipal": "7654321",
            "lista_rps": [
                {
                    "numero": "10",
                    "serie": "B",
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
                    "valor_servico": "50.00",
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
                    "base_calculo": "50.00",
                    "aliquota_issqn": "3.00",
                    "valor_liquido_nfse": "50.00",
                    "desconto_incondicionado": "0.00",
                    "desconto_condicionado": "0.00",
                    "codigo_servico": "0107",
                    "cnae_servico": "6204000",
                    "codigo_tributacao_municipio": "6204000",
                    "descricao": "Serviço Fortaleza teste",
                    "codigo_municipio": "2304400",  # Fortaleza
                    "prestador": {
                        "cnpj": "12345678000199",
                        "inscricao_municipal": "7654321",
                    },
                    "tomador": {
                        "cnpj_cpf": "11111111000191",
                        "inscricao_municipal": "",
                        "razao_social": "Cliente Fortaleza",
                        "logradouro": "Av Central",
                        "numero": "200",
                        "complemento": "Sala 5",
                        "bairro": "Bairro",
                        "cidade": "2304400",
                        "uf": "CE",
                        "cep": "60000000",
                        "telefone": "8530000000",
                        "email": "fortaleza@example.com",
                    },
                }
            ],
        },
    }


def build_cancel_kwargs(numero_nfse: str):
    return {
        "emissor": "fortaleza",
        "cancelamento": {
            "numero_nfse": numero_nfse,
            "cnpj_prestador": "12345678000199",
            "inscricao_municipal": "7654321",
        },
    }


def main():
    if len(sys.argv) < 3:
        print("Uso: python -m pytrustnfe.nfse.ginfes.test_fortaleza_demo caminho.pfx SENHA [NUMERO_NFSE]")
        sys.exit(1)
    pfx_path = sys.argv[1]
    senha = sys.argv[2]
    numero_nfse = sys.argv[3] if len(sys.argv) > 3 else "555"
    if not os.path.isfile(pfx_path):
        print("Arquivo PFX não encontrado:", pfx_path)
        sys.exit(2)
    with open(pfx_path, "rb") as f:
        pfx_bytes = f.read()
    certificado = Certificado(pfx_bytes, senha)
    lote_xml = xml_recepcionar_lote_rps(certificado, **build_lote_kwargs())
    cancel_xml = xml_cancelar_nfse(certificado, **build_cancel_kwargs(numero_nfse))
    print("XML Lote Fortaleza (snippet):")
    print(lote_xml[:400] + ("..." if len(lote_xml) > 400 else ""))
    print("\nXML Cancelamento Fortaleza (snippet):")
    print(cancel_xml[:400] + ("..." if len(cancel_xml) > 400 else ""))


if __name__ == "__main__":
    main()
