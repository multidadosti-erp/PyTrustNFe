# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import tempfile
try:
    from OpenSSL import crypto  # type: ignore
except Exception:  # ImportError ou erro interno por incompatibilidade de flags
    crypto = None


def _fallback_extract(pfx_bytes, password):
    """Fallback usando cryptography se pyOpenSSL falhar por incompatibilidade.

    Evita quebrar fluxo em ambientes onde pyOpenSSL antigo não expõe flags
    presentes na versão de runtime do OpenSSL.
    """
    try:
        from cryptography.hazmat.primitives.serialization import (
            pkcs12,
            Encoding,
            PrivateFormat,
            NoEncryption,
        )
    except Exception:
        raise
    key, cert, _others = pkcs12.load_key_and_certificates(
        pfx_bytes, password.encode() if isinstance(password, str) else password
    )
    key_pem = key.private_bytes(Encoding.PEM, PrivateFormat.TraditionalOpenSSL, NoEncryption())
    cert_pem = cert.public_bytes(Encoding.PEM)
    return cert_pem.decode(), key_pem.decode()


class Certificado(object):
    def __init__(self, pfx, password):
        self.pfx = pfx
        self.password = password

    def save_pfx(self):
        pfx_temp = tempfile.mkstemp()[1]
        arq_temp = open(pfx_temp, "wb")
        arq_temp.write(self.pfx)
        arq_temp.close()
        return pfx_temp


def extract_cert_and_key_from_pfx(pfx, password):
    """Extrai certificado e chave privada de um PFX.

    Primeiro tenta via pyOpenSSL (compatível historicamente com o projeto).
    Se ocorrer erro de atributo (incompatibilidade de flags) ou qualquer
    exceção inesperada, tenta fallback via cryptography.
    """
    if crypto is not None:
        try:
            pfx_obj = crypto.load_pkcs12(pfx, password)
            key = crypto.dump_privatekey(crypto.FILETYPE_PEM, pfx_obj.get_privatekey())
            cert = crypto.dump_certificate(crypto.FILETYPE_PEM, pfx_obj.get_certificate())
            return cert.decode(), key.decode()
        except Exception:
            # Falha ao usar pyOpenSSL: segue para fallback
            pass
    # Fallback silencioso para não quebrar assinatura em ambiente legacy
    return _fallback_extract(pfx, password)


def save_cert_key(cert, key):
    cert_temp = tempfile.mkstemp()[1]
    key_temp = tempfile.mkstemp()[1]

    arq_temp = open(cert_temp, "w")
    arq_temp.write(cert)
    arq_temp.close()

    arq_temp = open(key_temp, "w")
    arq_temp.write(key)
    arq_temp.close()

    return cert_temp, key_temp
