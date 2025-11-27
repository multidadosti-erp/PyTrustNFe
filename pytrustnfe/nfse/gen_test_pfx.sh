#!/usr/bin/env bash
set -euo pipefail

# Gera um certificado autoassinado e empacota em PFX para testes NFSe/NFe.
# Uso:
#   bash gen_test_pfx.sh NOME_BASE SENHA
# Exemplo:
#   bash gen_test_pfx.sh teste_nfse TEST1234
# Saídas: teste_nfse.key, teste_nfse.crt, teste_nfse.pfx no diretório atual.

BASE_NAME=${1:-teste_nfse}
PASSWORD=${2:-TEST1234}

if ! command -v openssl >/dev/null 2>&1; then
  echo "openssl não encontrado no PATH" >&2
  exit 1
fi

echo "Gerando chave privada RSA 2048...";
openssl genrsa -out "${BASE_NAME}.key" 2048 >/dev/null 2>&1

echo "Gerando certificado X.509 autoassinado (válido 365 dias)...";
openssl req -x509 -new -nodes -key "${BASE_NAME}.key" -sha256 -days 365 \
  -subj "/C=BR/ST=SP/L=SaoPaulo/O=EmpresaTeste/CN=www.exemplo.com" \
  -out "${BASE_NAME}.crt" >/dev/null 2>&1

echo "Empacotando em PKCS#12 (PFX)...";
openssl pkcs12 -export -out "${BASE_NAME}.pfx" -inkey "${BASE_NAME}.key" -in "${BASE_NAME}.crt" -password "pass:${PASSWORD}" >/dev/null 2>&1

echo "Concluído. Arquivos gerados:";
ls -1 "${BASE_NAME}.key" "${BASE_NAME}.crt" "${BASE_NAME}.pfx"
echo "Senha do PFX: ${PASSWORD}";
echo "Use para testes: python -m pytrustnfe.nfse.test_assinaturas_demo ${BASE_NAME}.pfx ${PASSWORD}";
