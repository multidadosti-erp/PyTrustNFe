# Guia de Execução de Testes e Validações (pytrustnfe)

Este documento fica dentro de `pytrustnfe` para facilitar manutenção das rotinas de assinatura NF-e e NFSe.

## 1. Preparar Ambiente
```bash
cd /home/gustotc/Workspace
source .venv/bin/activate
pip install --upgrade --force-reinstall --no-cache-dir -r odoo/requirements.txt
pip install -e odoo/multierp/lib/pytrustnfe
```

Gerar PFX de teste (opcional):
```bash
cd odoo/multierp/lib/pytrustnfe/pytrustnfe/nfse
bash gen_test_pfx.sh demo_nfse DEMO1234
```

## 2. Pytest
```bash
cd /home/gustotc/Workspace
pytest -q            # todos
pytest -k assinatura # filtrar
pytest -vv           # verbose
```

Task VS Code disponível: `ACBrPagFor: Testes`.

## 3. NF-e Assinatura (Demo)
Se existir script de demo (ou criar semelhante ao NFSe):
```bash
cd odoo/multierp/lib/pytrustnfe
python -m pytrustnfe.nfe.test_assinatura_demo pytrustnfe/nfse/demo_nfse.pfx DEMO1234
```

Variável para obrigar SHA1 legado:
```bash
export NF_E_SIGNATURE_LEGACY_SHA1=1
python -m pytrustnfe.nfe.test_assinatura_demo demo_nfse.pfx DEMO1234
unset NF_E_SIGNATURE_LEGACY_SHA1
```

## 4. NFSe Assinaturas (Scripts)
Local dos scripts:
- `pytrustnfe/nfse/test_assinaturas_demo.py` (Goiânia, MGA, BH)
- `pytrustnfe/nfse/ginfes/test_ginfes_demo.py` (GINFES lote)
- `pytrustnfe/nfse/ginfes/test_ginfes_cancel_demo.py` (GINFES cancelamento)
- `pytrustnfe/nfse/ginfes/test_fortaleza_demo.py` (Fortaleza lote + cancelamento)

Exemplos:
```bash
cd odoo/multierp/lib/pytrustnfe
python -m pytrustnfe.nfse.test_assinaturas_demo pytrustnfe/nfse/demo_nfse.pfx DEMO1234
PROVEDORES="goiania,mga" python -m pytrustnfe.nfse.test_assinaturas_demo pytrustnfe/nfse/demo_nfse.pfx DEMO1234
python -m pytrustnfe.nfse.ginfes.test_ginfes_demo pytrustnfe/nfse/demo_nfse.pfx DEMO1234
python -m pytrustnfe.nfse.ginfes.test_ginfes_cancel_demo pytrustnfe/nfse/demo_nfse.pfx DEMO1234 777
python -m pytrustnfe.nfse.ginfes.test_fortaleza_demo pytrustnfe/nfse/demo_nfse.pfx DEMO1234 555
```

## 5. Referências e Algoritmos
- Vendorizado `signxml 2.9.0` para suportar SHA1.
- NFSe usa assinatura enveloped (rsa-sha1 / sha1) por exigência atual.
- Referências:
  - Goiânia/MGA/BH: Id do RPS ou elemento de lote.
  - GINFES lote: `rps<num>`; cancelamento sem Id → documento inteiro.
  - Fortaleza segue regra GINFES com remapeamento de método.

## 6. Erros Comuns
| Erro | Causa | Solução |
|------|-------|---------|
| Unable to resolve reference URI | Id ausente no XML | Assina sem reference_uri (já implementado) |
| Password given but private key not encrypted | Passphrase em chave sem proteção | Fallback já evita; não usar senha extra |
| ModuleNotFoundError (Jinja2/MarkupSafe) | Versões incompatíveis | Instalar versões do `requirements.txt` |
| pyOpenSSL flags ausentes | OpenSSL moderno vs lib antiga | Fallback para `cryptography` já implementado |

## 7. Migração para SHA256 Futuro
Alterar `signature_algorithm` e `digest_algorithm` nas classes de assinatura. Remover uso de env var legado e atualizar testes.

## 8. Pipeline CI (Sugestão)
1. Instalar dependências.
2. Rodar `pytest -q`.
3. Executar scripts de assinatura com PFX dummy e validar presença de `<Signature>`.
4. (Opcional) Validar contra XSD se disponível.

## 9. Reset Ambiente
```bash
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r odoo/requirements.txt
```

## 10. FAQ
- PFX real vs teste? Pode usar ambos; teste não valida cadeia.
- Precisa internet para assinatura? Não.
- Diferença NF-e vs NFSe? NF-e mantém lógica própria com env var SHA1 e estrutura do XML fiscal.

---
Manter este arquivo sincronizado com mudanças de provedores e algoritmos.
