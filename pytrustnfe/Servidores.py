# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

WS_NFE_AUTORIZACAO = 'NfeAutorizacao'
WS_NFE_RET_AUTORIZACAO = 'NfeRetAutorizacao'
WS_NFE_CANCELAMENTO = 'RecepcaoEventoCancelamento'
WS_NFE_INUTILIZACAO = 'NfeInutilizacao'
WS_NFE_CONSULTA = 'NfeConsultaProtocolo'
WS_NFE_SITUACAO = 'NfeStatusServico'
WS_NFE_CADASTRO = 'NfeConsultaCadastro'

WS_NFCE_AUTORIZACAO = 'NfeAutorizacao'
WS_NFCE_RET_AUTORIZACAO = 'NfeRetAutorizacao'
WS_NFCE_CANCELAMENTO = 'RecepcaoEventoCancelamento'
WS_NFCE_INUTILIZACAO = 'NfeInutilizacao'
WS_NFCE_CONSULTA = 'NfeConsultaProtocolo'
WS_NFCE_SITUACAO = 'NfeStatusServico'
WS_NFCE_CADASTRO = 'NfeConsultaCadastro'
WS_NFCE_RECEPCAO_EVENTO = 'RecepcaoEventoCarta'
WS_NFCE_QR_CODE = 'NfeQRCode'
WS_NFCE_CONSULTA_DESTINADAS = 'NfeConsultaDest',
WS_NFCE_RET_AUTORIZACAO = 'NFeRetAutorizacao',


WS_NFE_CADASTRO = 'NfeConsultaCadastro'
WS_DPEC_RECEPCAO = 'RecepcaoEventoEPEC'
WS_DPEC_CONSULTA = 8

WS_NFE_RECEPCAO_EVENTO = 'RecepcaoEventoCarta'
WS_NFE_RECEPCAO_EVENTO_MANIFESTO = 'RecepcaoEventoManifesto'
WS_DFE_DISTRIBUICAO = 'NFeDistribuicaoDFe'
WS_DOWNLOAD_NFE = 'nfeDistDFeInteresse'

NFE_AMBIENTE_PRODUCAO = 1
NFE_AMBIENTE_HOMOLOGACAO = 2
NFCE_AMBIENTE_PRODUCAO = 1
NFCE_AMBIENTE_HOMOLOGACAO = 2

NFE_MODELO = '55'
NFCE_MODELO = '65'

SIGLA_ESTADO = {
    '12': 'AC',
    '27': 'AL',
    '13': 'AM',
    '16': 'AP',
    '29': 'BA',
    '23': 'CE',
    '53': 'DF',
    '32': 'ES',
    '52': 'GO',
    '21': 'MA',
    '31': 'MG',
    '50': 'MS',
    '51': 'MT',
    '15': 'PA',
    '25': 'PB',
    '26': 'PE',
    '22': 'PI',
    '41': 'PR',
    '33': 'RJ',
    '24': 'RN',
    '11': 'RO',
    '14': 'RR',
    '43': 'RS',
    '42': 'SC',
    '28': 'SE',
    '35': 'SP',
    '17': 'TO',
}


def localizar_url(servico, estado, mod='55', ambiente=2):

    # import ipdb; ipdb.set_trace()
    sigla = SIGLA_ESTADO[estado]
    ws = ESTADO_WS[sigla]

    if servico in (WS_DFE_DISTRIBUICAO, WS_DOWNLOAD_NFE,
                   WS_NFE_RECEPCAO_EVENTO_MANIFESTO):
        ws = AN

    if mod in ws:
        dominio = ws[mod][ambiente]['servidor']
        complemento = ws[mod][ambiente][servico]
    else:
        dominio = ws[ambiente]['servidor']
        complemento = ws[ambiente][servico]

    if sigla == 'RS' and servico == WS_NFE_CADASTRO:
        dominio = 'cad.sefazrs.rs.gov.br'
    if sigla in ('AC', 'RN', 'PB', 'SC', 'RJ') and \
       servico == WS_NFE_CADASTRO:
        dominio = 'cad.svrs.rs.gov.br'

    return "https://%s/%s" % (dominio, complemento)


def localizar_qrcode(estado, ambiente=2):
    sigla = SIGLA_ESTADO[estado]
    dominio = ESTADO_WS[sigla]['65'][ambiente]['servidor']
    complemento = ESTADO_WS[sigla]['65'][ambiente][WS_NFCE_QR_CODE]
    if 'https://' in complemento:
        return complemento
    return "https://%s/%s" % (dominio, complemento)


METODO_WS = {
    WS_NFE_AUTORIZACAO: {
        'webservice': 'NfeAutorizacao',
        'metodo': 'NfeAutorizacao',
    },
    WS_NFE_RET_AUTORIZACAO: {
        'webservice': 'NfeRetAutorizacao',
        'metodo': 'NfeRetAutorizacao',
    },
    WS_NFE_INUTILIZACAO: {
        'webservice': 'NfeInutilizacao2',
        'metodo': 'nfeInutilizacaoNF2',
    },
    WS_NFE_CONSULTA: {
        'webservice': 'NfeConsulta2',
        'metodo': 'nfeConsultaNF2',
    },
    WS_NFE_SITUACAO: {
        'webservice': 'NfeStatusServico2',

        'metodo': 'nfeStatusServicoNF2',
    },
    WS_NFE_CADASTRO: {
        'webservice': 'CadConsultaCadastro2',
        'metodo': 'consultaCadastro2',
    },
    WS_NFE_RECEPCAO_EVENTO: {
        'webservice': 'RecepcaoEvento',
        'metodo': 'nfeRecepcaoEvento',
    },
}

SVRS = {
    NFE_AMBIENTE_PRODUCAO: {
        'servidor': 'nfe.svrs.rs.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'ws/recepcaoevento/recepcaoevento4.asmx',
        WS_NFE_CANCELAMENTO: 'ws/recepcaoevento/recepcaoevento4.asmx',
        WS_NFE_AUTORIZACAO: 'ws/NfeAutorizacao/NFeAutorizacao4.asmx',
        WS_NFE_RET_AUTORIZACAO: 'ws/NfeRetAutorizacao/NFeRetAutorizacao4.asmx',
        WS_NFE_CADASTRO: 'ws/cadconsultacadastro/cadconsultacadastro4.asmx',
        WS_NFE_INUTILIZACAO: 'ws/nfeinutilizacao/nfeinutilizacao4.asmx',
        WS_NFE_CONSULTA: 'ws/NfeConsulta/NfeConsulta4.asmx',
        WS_NFE_SITUACAO: 'ws/NfeStatusServico/NfeStatusServico4.asmx',
    },
    NFE_AMBIENTE_HOMOLOGACAO: {
        'servidor': 'nfe-homologacao.svrs.rs.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'ws/recepcaoevento/recepcaoevento4.asmx',
        WS_NFE_CANCELAMENTO: 'ws/recepcaoevento/recepcaoevento4.asmx',
        WS_NFE_AUTORIZACAO: 'ws/NfeAutorizacao/NFeAutorizacao4.asmx',
        WS_NFE_RET_AUTORIZACAO: 'ws/NfeRetAutorizacao/NFeRetAutorizacao4.asmx',
        WS_NFE_CADASTRO: 'ws/cadconsultacadastro/cadconsultacadastro4.asmx',
        WS_NFE_INUTILIZACAO: 'ws/nfeinutilizacao/nfeinutilizacao4.asmx',
        WS_NFE_CONSULTA: 'ws/NfeConsulta/NfeConsulta4.asmx',
        WS_NFE_SITUACAO: 'ws/NfeStatusServico/NfeStatusServico4.asmx',
    }
}

SVAN = {
    NFE_AMBIENTE_PRODUCAO: {
        'servidor': 'www.sefazvirtual.fazenda.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'NFeRecepcaoEvento4/NFeRecepcaoEvento4.asmx',
        WS_NFE_AUTORIZACAO: 'NFeAutorizacao4/NFeAutorizacao4.asmx',
        WS_NFE_RET_AUTORIZACAO: 'NFeRetAutorizacao4/NFeRetAutorizacao4.asmx',
        WS_NFE_INUTILIZACAO: 'NFeInutilizacao4/NFeInutilizacao4.asmx',
        WS_NFE_CONSULTA: 'NFeConsultaProtocolo4/NFeConsultaProtocolo4.asmx',
        WS_NFE_SITUACAO: 'NFeStatusServico4/NFeStatusServico4.asmx',
    },
    NFE_AMBIENTE_HOMOLOGACAO: {
        'servidor': 'hom.sefazvirtual.fazenda.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'NFeRecepcaoEvento4/NFeRecepcaoEvento4.asmx',
        WS_NFE_AUTORIZACAO: 'NFeAutorizacao4/NFeAutorizacao4.asmx',
        WS_NFE_RET_AUTORIZACAO: 'NFeRetAutorizacao4/NFeRetAutorizacao4.asmx',
        WS_NFE_INUTILIZACAO: 'NFeInutilizacao4/NFeInutilizacao4.asmx',
        WS_NFE_CONSULTA: 'NFeConsultaProtocolo4/NFeConsultaProtocolo4.asmx',
        WS_NFE_SITUACAO: 'NFeStatusServico4/NFeStatusServico4.asmx',
    }
}

SCAN = {
    NFE_AMBIENTE_PRODUCAO: {
        'servidor': 'www.scan.fazenda.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'NFeRecepcaoEvento4/NFeRecepcaoEvento4.asmx',
        WS_NFE_AUTORIZACAO: 'NFeAutorizacao4/NFeAutorizacao4.asmx',
        WS_NFE_RET_AUTORIZACAO: 'NFeRetAutorizacao4/NFeRetAutorizacao4.asmx',
        WS_NFE_INUTILIZACAO: 'NFeInutilizacao4/NFeInutilizacao4.asmx',
        WS_NFE_CONSULTA: 'NFeConsultaProtocolo4/NFeConsultaProtocolo4.asmx',
        WS_NFE_SITUACAO: 'NFeStatusServico4/NFeStatusServico4.asmx'
    },
    NFE_AMBIENTE_HOMOLOGACAO: {
        'servidor': 'hom.nfe.fazenda.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'NFeRecepcaoEvento4/NFeRecepcaoEvento4.asmx',
        WS_NFE_AUTORIZACAO: 'NFeAutorizacao4/NFeAutorizacao4.asmx',
        WS_NFE_RET_AUTORIZACAO: 'NFeRetAutorizacao4/NFeRetAutorizacao4.asmx',
        WS_NFE_INUTILIZACAO: 'NFeInutilizacao4/NFeInutilizacao4.asmx',
        WS_NFE_CONSULTA: 'NFeConsultaProtocolo4/NFeConsultaProtocolo4.asmx',
        WS_NFE_SITUACAO: 'NFeStatusServico4/NFeStatusServico4.asmx'
    }
}

SVC_AN = {
    NFE_AMBIENTE_PRODUCAO: {
        'servidor': 'www.svc.fazenda.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'NFeRecepcaoEvento4/NFeRecepcaoEvento4.asmx',
        WS_NFE_AUTORIZACAO: 'NFeAutorizacao4/NFeAutorizacao4.asmx',
        WS_NFE_RET_AUTORIZACAO: 'NFeRetAutorizacao4/NFeRetAutorizacao4.asmx',
        WS_NFE_INUTILIZACAO: 'NFeInutilizacao4/NFeInutilizacao4.asmx',
        WS_NFE_CONSULTA: 'NFeConsultaProtocolo4/NFeConsultaProtocolo4.asmx',
        WS_NFE_SITUACAO: 'NFeStatusServico4/NFeStatusServico4.asmx',
    },
    NFE_AMBIENTE_HOMOLOGACAO: {
        'servidor': 'hom.svc.fazenda.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'NFeRecepcaoEvento4/NFeRecepcaoEvento4.asmx',
        WS_NFE_AUTORIZACAO: 'NFeAutorizacao4/NFeAutorizacao4.asmx',
        WS_NFE_RET_AUTORIZACAO: 'NFeRetAutorizacao4/NFeRetAutorizacao4.asmx',
        WS_NFE_INUTILIZACAO: 'NFeInutilizacao4/NFeInutilizacao4.asmx',
        WS_NFE_CONSULTA: 'NFeConsultaProtocolo4/NFeConsultaProtocolo4.asmx',
        WS_NFE_SITUACAO: 'NFeStatusServico4/NFeStatusServico4.asmx',
    }
}

SVC_RS = {
    NFE_AMBIENTE_PRODUCAO: {
        'servidor': 'nfe.svrs.rs.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'ws/recepcaoevento/recepcaoevento4.asmx',
        WS_NFE_AUTORIZACAO: 'ws/NfeAutorizacao/NFeAutorizacao4.asmx',
        WS_NFE_RET_AUTORIZACAO: 'NfeRetAutorizacao/NFeRetAutorizacao4.asmx',
        WS_NFE_CONSULTA: 'ws/NfeConsulta/NfeConsulta4.asmx',
        WS_NFE_SITUACAO: 'ws/NfeStatusServico/NfeStatusServico4.asmx',
    },
    NFE_AMBIENTE_HOMOLOGACAO: {
        'servidor': 'nfe-homologacao.svrs.rs.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'ws/recepcaoevento/recepcaoevento4.asmx',
        WS_NFE_AUTORIZACAO: 'ws/NfeAutorizacao/NFeAutorizacao4.asmx',
        WS_NFE_RET_AUTORIZACAO: 'NfeRetAutorizacao/NFeRetAutorizacao4.asmx',
        WS_NFE_CONSULTA: 'ws/NfeConsulta/NfeConsulta4.asmx',
        WS_NFE_SITUACAO: 'ws/NfeStatusServico/NfeStatusServico4.asmx',
    }
}

DPEC = {
    NFE_AMBIENTE_PRODUCAO: {
        'servidor': 'www.nfe.fazenda.gov.br',
        WS_DPEC_CONSULTA: 'SCERecepcaoRFB/SCERecepcaoRFB.asmx',
        WS_DPEC_RECEPCAO: 'SCEConsultaRFB/SCEConsultaRFB.asmx'
    },
    NFE_AMBIENTE_HOMOLOGACAO: {
        'servidor': 'hom.nfe.fazenda.gov.br',
        WS_DPEC_CONSULTA: 'SCERecepcaoRFB/SCERecepcaoRFB.asmx',
        WS_DPEC_RECEPCAO: 'SCEConsultaRFB/SCEConsultaRFB.asmx'
    }
}

AN = {
    NFE_AMBIENTE_PRODUCAO: {
        'servidor': 'www.nfe.fazenda.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'NFeRecepcaoEvento4/NFeRecepcaoEvento4.asmx',
        WS_DFE_DISTRIBUICAO: 'NFeDistribuicaoDFe/NFeDistribuicaoDFe.asmx',  # Usa url diferente
        WS_DOWNLOAD_NFE: 'NFeDistribuicaoDFe/NFeDistribuicaoDFe.asmx',
        WS_NFE_RECEPCAO_EVENTO_MANIFESTO: 'NFeRecepcaoEvento4/NFeRecepcaoEvento4.asmx',
    },
    NFE_AMBIENTE_HOMOLOGACAO: {
        'servidor': 'hom.nfe.fazenda.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'NFeRecepcaoEvento4/NFeRecepcaoEvento4.asmx',
        WS_DFE_DISTRIBUICAO: 'NFeDistribuicaoDFe/NFeDistribuicaoDFe.asmx',
        WS_DOWNLOAD_NFE: 'NFeDistribuicaoDFe/NFeDistribuicaoDFe.asmx',
        WS_NFE_RECEPCAO_EVENTO_MANIFESTO: 'NFeRecepcaoEvento4/NFeRecepcaoEvento4.asmx',
    },
}

UFAM = {
    NFE_MODELO: {
        NFE_AMBIENTE_PRODUCAO: {
            'servidor': 'nfe.sefaz.am.gov.br',
            WS_NFE_RECEPCAO_EVENTO: 'services2/services/RecepcaoEvento4',
            WS_NFE_CANCELAMENTO: 'services2/services/RecepcaoEvento4',
            WS_NFE_AUTORIZACAO: 'services2/services/NfeAutorizacao4',
            WS_NFE_RET_AUTORIZACAO: 'services2/services/NfeRetAutorizacao4',
            WS_NFE_INUTILIZACAO: 'services2/services/NfeInutilizacao4',
            WS_NFE_CONSULTA: 'services2/services/NfeConsulta4',
            WS_NFE_SITUACAO: 'services2/services/NfeStatusServico4',
            # WS_NFE_CADASTRO: 'services2/services/cadconsultacadastro2',
        },
        NFE_AMBIENTE_HOMOLOGACAO: {
            'servidor': 'homnfe.sefaz.am.gov.br',
            WS_NFE_RECEPCAO_EVENTO: 'services2/services/RecepcaoEvento4',
            WS_NFE_CANCELAMENTO: 'services2/services/RecepcaoEvento4',
            WS_NFE_AUTORIZACAO: 'services2/services/NfeAutorizacao4',
            WS_NFE_RET_AUTORIZACAO: 'services2/services/NfeRetAutorizacao4',
            WS_NFE_INUTILIZACAO: 'services2/services/NfeInutilizacao4',
            WS_NFE_CONSULTA: 'services2/services/NfeConsulta4',
            WS_NFE_SITUACAO: 'services2/services/NfeStatusServico4',
            # WS_NFE_CADASTRO: 'services2/services/cadconsultacadastro2',
        }
    },
    NFCE_MODELO: {
        NFE_AMBIENTE_PRODUCAO: {
            'servidor': 'nfe.sefaz.am.gov.br',
            WS_NFE_RECEPCAO_EVENTO: 'services2/services/RecepcaoEvento4',
            WS_NFE_CANCELAMENTO: 'services2/services/RecepcaoEvento4',
            WS_NFE_AUTORIZACAO: 'services2/services/NfeAutorizacao4',
            WS_NFE_RET_AUTORIZACAO: 'services2/services/NfeRetAutorizacao4',
            WS_NFE_INUTILIZACAO: 'services2/services/NfeInutilizacao4',
            WS_NFE_CONSULTA: 'services2/services/NfeConsulta4',
            WS_NFE_SITUACAO: 'services2/services/NfeStatusServico4',
            # WS_NFE_CADASTRO: 'services2/services/cadconsultacadastro2',
        },
        NFE_AMBIENTE_HOMOLOGACAO: {
            'servidor': 'homnfce.sefaz.am.gov.br',
            WS_NFE_RECEPCAO_EVENTO: 'nfce-services-nac/services/RecepcaoEvento4',
            WS_NFE_CANCELAMENTO: 'nfce-services-nac/services/RecepcaoEvento4',
            WS_NFE_AUTORIZACAO: 'nfce-services-nac/services/NfeAutorizacao4',
            WS_NFE_RET_AUTORIZACAO: 'nfce-services-nac/services/NfeRetAutorizacao4',
            WS_NFE_INUTILIZACAO: 'nfce-services-nac/services/NfeInutilizacao4',
            WS_NFE_CONSULTA: 'nfce-services-nac/services/NfeConsulta4',
            WS_NFE_SITUACAO: 'nfce-services-nac/services/NfeStatusServico4',
            WS_NFCE_QR_CODE: 'http://homnfce.sefaz.am.gov.br/nfceweb/consultarNFCe.jsp',
        }
    }
}

UFBA = {
    NFE_AMBIENTE_PRODUCAO: {
        'servidor': 'nfe.sefaz.ba.gov.br',
        WS_NFE_AUTORIZACAO: 'webservices/NFeAutorizacao4/NFeAutorizacao4.asmx',
        WS_NFE_RET_AUTORIZACAO: 'webservices/NFeRetAutorizacao4/NFeRetAutorizacao4.asmx',
        WS_NFE_CONSULTA: 'webservices/NFeConsultaProtocolo4/NFeConsultaProtocolo4.asmx',
        WS_NFE_SITUACAO: 'webservices/NFeStatusServico4/NFeStatusServico4.asmx',
        WS_NFE_INUTILIZACAO: 'webservices/NFeInutilizacao4/NFeInutilizacao4.asmx',
        WS_NFE_CADASTRO: 'webservices/CadConsultaCadastro4/CadConsultaCadastro4.asmx',
        WS_NFE_RECEPCAO_EVENTO: 'webservices/NFeRecepcaoEvento4/NFeRecepcaoEvento4.asmx',
        WS_NFE_CANCELAMENTO: 'webservices/NFeRecepcaoEvento4/NFeRecepcaoEvento4.asmx',
    },
    NFE_AMBIENTE_HOMOLOGACAO: {
        'servidor': 'hnfe.sefaz.ba.gov.br',
        WS_NFE_AUTORIZACAO: 'webservices/NFeAutorizacao4/NFeAutorizacao4.asmx',
        WS_NFE_RET_AUTORIZACAO: 'webservices/NFeRetAutorizacao4/NFeRetAutorizacao4.asmx',
        WS_NFE_CONSULTA: 'webservices/NFeConsultaProtocolo4/NFeConsultaProtocolo4.asmx',
        WS_NFE_SITUACAO: 'webservices/NFeStatusServico4/NFeStatusServico4.asmx',
        WS_NFE_INUTILIZACAO: 'webservices/NFeInutilizacao4/NFeInutilizacao4.asmx',
        WS_NFE_CADASTRO: 'webservices/CadConsultaCadastro4/CadConsultaCadastro4.asmx',
        WS_NFE_RECEPCAO_EVENTO: 'webservices/NFeRecepcaoEvento4/NFeRecepcaoEvento4.asmx',
        WS_NFE_CANCELAMENTO: 'webservices/NFeRecepcaoEvento4/NFeRecepcaoEvento4.asmx',
    }
}

UFCE = {
    NFE_AMBIENTE_PRODUCAO: {
        'servidor': 'nfe.sefaz.ce.gov.br',
        WS_NFE_AUTORIZACAO: 'nfe4/services/NFeAutorizacao4?wsdl',
        WS_NFE_RET_AUTORIZACAO: 'nfe4/services/NFeRetAutorizacao4?wsdl',
        WS_NFE_INUTILIZACAO: 'nfe4/services/NFeInutilizacao4?wsdl',
        WS_NFE_CONSULTA: 'nfe4/services/NFeConsultaProtocolo4?wsdl',
        WS_NFE_SITUACAO: 'nfe4/services/NFeStatusServico4?wsdl',
        WS_NFE_CADASTRO: 'nfe4/services/CadConsultaCadastro4?wsdl',
        WS_NFE_RECEPCAO_EVENTO: 'nfe4/services/NFeRecepcaoEvento4?wsdl',
        WS_NFE_CANCELAMENTO: 'nfe4/services/NFeRecepcaoEvento4?wsdl',
    },
    NFE_AMBIENTE_HOMOLOGACAO: {
        'servidor': 'nfeh.sefaz.ce.gov.br',
        WS_NFE_AUTORIZACAO: 'nfe4/services/NFeAutorizacao4?wsdl',
        WS_NFE_RET_AUTORIZACAO: 'nfe4/services/NFeRetAutorizacao4?wsdl',
        WS_NFE_INUTILIZACAO: 'nfe4/services/NFeInutilizacao4?wsdl',
        WS_NFE_CONSULTA: 'nfe4/services/NFeConsultaProtocolo4?wsdl',
        WS_NFE_SITUACAO: 'nfe4/services/NFeStatusServico4?wsdl',
        WS_NFE_CADASTRO: 'nfe4/services/CadConsultaCadastro4?wsdl',
        WS_NFE_RECEPCAO_EVENTO: 'nfe4/services/NFeRecepcaoEvento4?wsdl',
        WS_NFE_CANCELAMENTO: 'nfe4/services/NFeRecepcaoEvento4?wsdl',
    }
}


UFGO = {
    NFE_AMBIENTE_PRODUCAO: {
        'servidor': 'nfe.sefaz.go.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'nfe/services/NFeRecepcaoEvento4?wsdl',
        WS_NFE_AUTORIZACAO: 'nfe/services/NFeAutorizacao4?wsdl',
        WS_NFE_RET_AUTORIZACAO: 'nfe/services/NFeRetAutorizacao4?wsdl',
        WS_NFE_INUTILIZACAO: 'nfe/services/NFeInutilizacao4?wsdl',
        WS_NFE_CONSULTA: 'nfe/services/NFeConsultaProtocolo4?wsdl',
        WS_NFE_SITUACAO: 'nfe/services/NFeStatusServico4?wsdl',
        WS_NFE_CADASTRO: 'nfe/services/CadConsultaCadastro4?wsdl',
        WS_NFE_CANCELAMENTO: 'nfe/services/NFeRecepcaoEvento4?wsdl',
    },
    NFE_AMBIENTE_HOMOLOGACAO: {
        'servidor': 'homolog.sefaz.go.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'nfe/services/NFeRecepcaoEvento4?wsdl',
        WS_NFE_AUTORIZACAO: 'nfe/services/NFeAutorizacao4?wsdl',
        WS_NFE_RET_AUTORIZACAO: 'nfe/services/NFeRetAutorizacao4?wsdl',
        WS_NFE_INUTILIZACAO: 'nfe/services/NFeInutilizacao4?wsdl',
        WS_NFE_CONSULTA: 'nfe/services/NFeConsultaProtocolo4?wsdl',
        WS_NFE_SITUACAO: 'nfe/services/NFeStatusServico4?wsdl',
        WS_NFE_CADASTRO: 'nfe/services/CadConsultaCadastro4?wsdl',
        WS_NFE_CANCELAMENTO: 'nfe/services/NFeRecepcaoEvento4?wsdl',
    }
}


UFMT = {
    NFE_AMBIENTE_PRODUCAO: {
        'servidor': 'nfe.sefaz.mt.gov.br',
        WS_NFE_AUTORIZACAO: 'nfews/v2/services/NfeAutorizacao4?wsdl',
        WS_NFE_RET_AUTORIZACAO: 'nfews/v2/services/NfeRetAutorizacao4?wsdl',
        WS_NFE_INUTILIZACAO: 'nfews/v2/services/NfeInutilizacao4?wsdl',
        WS_NFE_CONSULTA: 'nfews/v2/services/NfeConsulta4?wsdl',
        WS_NFE_SITUACAO: 'nfews/v2/services/NfeStatusServico4?wsdl',
        WS_NFE_CADASTRO: 'nfews/v2/services/CadConsultaCadastro4?wsdl',
        WS_NFE_RECEPCAO_EVENTO: 'nfews/v2/services/RecepcaoEvento4?wsdl',
        WS_NFE_CANCELAMENTO: 'nfews/v2/services/RecepcaoEvento4?wsdl',
    },
    NFE_AMBIENTE_HOMOLOGACAO: {
        'servidor': 'homologacao.sefaz.mt.gov.br',
        WS_NFE_AUTORIZACAO: 'nfews/v2/services/NfeAutorizacao4?wsdl',
        WS_NFE_RET_AUTORIZACAO: 'nfews/v2/services/NfeRetAutorizacao4?wsdl',
        WS_NFE_INUTILIZACAO: 'nfews/v2/services/NfeInutilizacao4?wsdl',
        WS_NFE_CONSULTA: 'nfews/v2/services/NfeConsulta4?wsdl',
        WS_NFE_SITUACAO: 'nfews/v2/services/NfeStatusServico4?wsdl',
        WS_NFE_CADASTRO: 'nfews/v2/services/CadConsultaCadastro4?wsdl',
        WS_NFE_RECEPCAO_EVENTO: 'nfews/v2/services/RecepcaoEvento4?wsdl',
        WS_NFE_CANCELAMENTO: 'nfews/v2/services/RecepcaoEvento4?wsdl',
    }
}

UFMS = {
    NFE_AMBIENTE_PRODUCAO: {
        'servidor': 'nfe.fazenda.ms.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'ws/NFeRecepcaoEvento4',
        WS_NFE_AUTORIZACAO: 'ws/NFeAutorizacao4',
        WS_NFE_RET_AUTORIZACAO: 'ws/NFeRetAutorizacao4',
        WS_NFE_CADASTRO: 'ws/CadConsultaCadastro4',
        WS_NFE_INUTILIZACAO: 'ws/NFeInutilizacao4',
        WS_NFE_CONSULTA: 'ws/NFeConsultaProtocolo4',
        WS_NFE_SITUACAO: 'ws/NFeStatusServico4',
        WS_NFE_CANCELAMENTO: 'ws/NFeRecepcaoEvento4',
    },
    NFE_AMBIENTE_HOMOLOGACAO: {
        'servidor': 'homologacao.nfe.ms.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'ws/NFeRecepcaoEvento4',
        WS_NFE_AUTORIZACAO: 'ws/NFeAutorizacao4',
        WS_NFE_RET_AUTORIZACAO: 'ws/NFeRetAutorizacao4',
        WS_NFE_CADASTRO: 'ws/CadConsultaCadastro4',
        WS_NFE_INUTILIZACAO: 'ws/NFeInutilizacao4',
        WS_NFE_CONSULTA: 'ws/NFeConsultaProtocolo4',
        WS_NFE_SITUACAO: 'ws/NFeStatusServico4',
        WS_NFE_CANCELAMENTO: 'ws/NFeRecepcaoEvento4',
    }
}

UFMG = {
    NFE_AMBIENTE_PRODUCAO: {
        'servidor': 'nfe.fazenda.mg.gov.br',
        WS_NFE_AUTORIZACAO: 'nfe2/services/NFeAutorizacao4',
        WS_NFE_RET_AUTORIZACAO: 'nfe2/services/NFeRetAutorizacao4',
        WS_NFE_INUTILIZACAO: 'nfe2/services/NFeInutilizacao4',
        WS_NFE_CONSULTA: 'nfe2/services/NFeConsultaProtocolo4',
        WS_NFE_SITUACAO: 'nfe2/services/NFeStatusServico4',
        WS_NFE_CADASTRO: 'nfe2/services/CadConsultaCadastro4',
        WS_NFE_RECEPCAO_EVENTO: 'nfe2/services/NFeRecepcaoEvento4',
        WS_NFE_CANCELAMENTO: 'nfe2/services/NFeRecepcaoEvento4',
    },
    NFE_AMBIENTE_HOMOLOGACAO: {
        'servidor': 'hnfe.fazenda.mg.gov.br',
        WS_NFE_AUTORIZACAO: 'nfe2/services/NFeAutorizacao4',
        WS_NFE_RET_AUTORIZACAO: 'nfe2/services/NFeRetAutorizacao4',
        WS_NFE_INUTILIZACAO: 'nfe2/services/NFeInutilizacao4',
        WS_NFE_CONSULTA: 'nfe2/services/NFeConsultaProtocolo4',
        WS_NFE_SITUACAO: 'nfe2/services/NFeStatusServico4',
        WS_NFE_CADASTRO: 'nfe2/services/CadConsultaCadastro4',
        WS_NFE_RECEPCAO_EVENTO: 'nfe2/services/NFeRecepcaoEvento4',
        WS_NFE_CANCELAMENTO: 'nfe2/services/NFeRecepcaoEvento4',
    }
}

UFPR = {
    NFE_AMBIENTE_PRODUCAO: {
        'servidor': 'nfe.sefa.pr.gov.br',
        WS_NFE_AUTORIZACAO: 'nfe/NFeAutorizacao4?wsdl',
        WS_NFE_RET_AUTORIZACAO: 'nfe/NFeRetAutorizacao4?wsdl',
        WS_NFE_INUTILIZACAO: 'nfe/NFeInutilizacao4?wsdl',
        WS_NFE_CONSULTA: 'nfe/NFeConsultaProtocolo4?wsdl',
        WS_NFE_SITUACAO: 'nfe/NFeStatusServico4?wsdl',
        WS_NFE_CADASTRO: 'nfe/CadConsultaCadastro4?wsdl',
        WS_NFE_RECEPCAO_EVENTO: 'nfe/NFeRecepcaoEvento4?wsdl',
        WS_NFE_CANCELAMENTO: 'nfe/NFeRecepcaoEvento4?wsdl',
    },
    NFE_AMBIENTE_HOMOLOGACAO: {
        'servidor': 'homologacao.nfe.sefa.pr.gov.br',
        WS_NFE_AUTORIZACAO: 'nfe/NFeAutorizacao4?wsdl',
        WS_NFE_RET_AUTORIZACAO: 'nfe/NFeRetAutorizacao4?wsdl',
        WS_NFE_INUTILIZACAO: 'nfe/NFeInutilizacao4?wsdl',
        WS_NFE_CONSULTA: 'nfe/NFeConsultaProtocolo4?wsdl',
        WS_NFE_SITUACAO: 'nfe/NFeStatusServico4?wsdl',
        WS_NFE_CADASTRO: 'nfe/CadConsultaCadastro4?wsdl',
        WS_NFE_RECEPCAO_EVENTO: 'nfe/NFeRecepcaoEvento4?wsdl',
        WS_NFE_CANCELAMENTO: 'nfe/NFeRecepcaoEvento4?wsdl',
    }
}

UFPE = {
    NFE_AMBIENTE_PRODUCAO: {
        'servidor': 'nfe.sefaz.pe.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'nfe-service/services/NFeRecepcaoEvento4',
        WS_NFE_CANCELAMENTO: 'nfe-service/services/NFeRecepcaoEvento4',
        WS_NFE_AUTORIZACAO: 'nfe-service/services/NFeAutorizacao4',
        WS_NFE_RET_AUTORIZACAO: 'nfe-service/services/NFeRetAutorizacao4',
        WS_NFE_INUTILIZACAO: 'nfe-service/services/NFeInutilizacao4',
        WS_NFE_CONSULTA: 'nfe-service/services/NFeConsultaProtocolo4',
        WS_NFE_SITUACAO: 'nfe-service/services/NFeStatusServico4',
        WS_NFE_CADASTRO: 'nfe-service/services/CadConsultaCadastro4?wsdl',
    },
    NFE_AMBIENTE_HOMOLOGACAO: {
        'servidor': 'nfehomolog.sefaz.pe.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'nfe-service/services/NFeRecepcaoEvento4',
        WS_NFE_CANCELAMENTO: 'nfe-service/services/NFeRecepcaoEvento4',
        WS_NFE_AUTORIZACAO: 'nfe-service/services/NFeAutorizacao4',
        WS_NFE_RET_AUTORIZACAO: 'nfe-service/services/NFeRetAutorizacao4',
        WS_NFE_INUTILIZACAO: 'nfe-service/services/NFeInutilizacao4',
        WS_NFE_CONSULTA: 'nfe-service/services/NFeConsultaProtocolo4',
        WS_NFE_SITUACAO: 'nfe-service/services/NFeStatusServico4',
        WS_NFE_CADASTRO: 'nfe-service/services/CadConsultaCadastro4?wsdl',
    }
}


UFRS = {
    NFE_MODELO: {
        NFE_AMBIENTE_PRODUCAO: {
            'servidor': 'nfe.sefazrs.rs.gov.br',
            WS_NFE_RECEPCAO_EVENTO: 'ws/recepcaoevento/recepcaoevento4.asmx',
            WS_NFE_AUTORIZACAO: 'ws/NfeAutorizacao/NFeAutorizacao4.asmx',
            WS_NFE_RET_AUTORIZACAO: 'ws/NfeRetAutorizacao/NFeRetAutorizacao4.asmx',
            WS_NFE_CADASTRO: 'ws/cadconsultacadastro/cadconsultacadastro4.asmx',
            WS_NFE_INUTILIZACAO: 'ws/NfeInutilizacao/nfeinutilizacao4.asmx',
            WS_NFE_CONSULTA: 'ws/NfeConsulta/NfeConsulta4.asmx',
            WS_NFE_SITUACAO: 'ws/NfeStatusServico/NfeStatusServico4.asmx',
            WS_NFE_CANCELAMENTO: 'ws/recepcaoevento/recepcaoevento4.asmx',
        },
        NFE_AMBIENTE_HOMOLOGACAO: {
            'servidor': 'nfe-homologacao.sefazrs.rs.gov.br',
            WS_NFE_RECEPCAO_EVENTO: 'ws/recepcaoevento/recepcaoevento4.asmx',
            WS_NFE_AUTORIZACAO: 'ws/NfeAutorizacao/NFeAutorizacao4.asmx',
            WS_NFE_RET_AUTORIZACAO: 'ws/NFeRetAutorizacao4/NFeRetAutorizacao4.asmx',
            WS_NFE_CADASTRO: 'ws/cadconsultacadastro/cadconsultacadastro4.asmx',
            WS_NFE_INUTILIZACAO: 'ws/NfeInutilizacao/nfeinutilizacao4.asmx',
            WS_NFE_CONSULTA: 'ws/NfeConsulta/NfeConsulta4.asmx',
            WS_NFE_SITUACAO: 'ws/NfeStatusServico/NfeStatusServico4.asmx',
            WS_NFE_CANCELAMENTO: 'ws/recepcaoevento/recepcaoevento4.asmx',
        }
    },
    NFCE_MODELO: {
        NFE_AMBIENTE_PRODUCAO: {
            'servidor': 'nfce.sefazrs.rs.gov.br',
            WS_NFCE_RECEPCAO_EVENTO: 'ws/recepcaoevento/recepcaoevento4.asmx',
            WS_NFCE_AUTORIZACAO: 'ws/NfeAutorizacao/NFeAutorizacao4.asmx',
            WS_NFCE_RET_AUTORIZACAO: 'ws/NfeRetAutorizacao/NFeRetAutorizacao4.asmx',
            WS_NFCE_CADASTRO: 'ws/cadconsultacadastro/cadconsultacadastro4.asmx',
            WS_NFCE_INUTILIZACAO: 'ws/NfeInutilizacao/nfeinutilizacao4.asmx',
            WS_NFCE_CONSULTA: 'ws/NfeConsulta/NfeConsulta4.asmx',
            WS_NFCE_SITUACAO: 'ws/NfeStatusServico/NfeStatusServico4.asmx',
            WS_NFCE_CANCELAMENTO: 'ws/recepcaoevento/recepcaoevento4.asmx',
            WS_NFCE_QR_CODE: 'https://www.sefaz.rs.gov.br/NFCE/NFCE-COM.aspx',
        },
        NFE_AMBIENTE_HOMOLOGACAO: {
            'servidor': 'nfce-homologacao.sefazrs.rs.gov.br',
            WS_NFCE_RECEPCAO_EVENTO: 'ws/recepcaoevento/recepcaoevento4.asmx',
            WS_NFCE_AUTORIZACAO: 'ws/NfeAutorizacao/NFeAutorizacao4.asmx',
            WS_NFCE_RET_AUTORIZACAO: 'ws/NfeRetAutorizacao/NFeRetAutorizacao4.asmx',
            WS_NFCE_CADASTRO: 'ws/cadconsultacadastro/cadconsultacadastro4.asmx',
            WS_NFCE_INUTILIZACAO: 'ws/NfeInutilizacao/nfeinutilizacao4.asmx',
            WS_NFCE_CONSULTA: 'ws/NfeConsulta/NfeConsulta4.asmx',
            WS_NFCE_SITUACAO: 'ws/NfeStatusServico/NfeStatusServico4.asmx',
            WS_NFCE_CANCELAMENTO: 'ws/recepcaoevento/recepcaoevento4.asmx',
            WS_NFCE_QR_CODE: 'https://www.sefaz.rs.gov.br/NFCE/NFCE-COM.aspx'
        }
    }
}

UFSP = {
    NFE_MODELO: {
        NFE_AMBIENTE_PRODUCAO: {
            'servidor': 'nfe.fazenda.sp.gov.br',
            WS_NFE_AUTORIZACAO: 'ws/nfeautorizacao4.asmx',
            WS_NFE_RET_AUTORIZACAO: 'ws/nferetautorizacao4.asmx',
            WS_NFE_INUTILIZACAO: 'ws/nfeinutilizacao4.asmx',
            WS_NFE_CONSULTA: 'ws/nfeconsulta4.asmx',
            WS_NFE_SITUACAO: 'ws/nfestatusservico4.asmx',
            WS_NFE_CADASTRO: 'ws/cadconsultacadastro4.asmx',
            WS_NFE_RECEPCAO_EVENTO: 'ws/nferecepcaoevento4.asmx',
            WS_NFE_CANCELAMENTO: 'ws/nferecepcaoevento4.asmx',
        },
        NFE_AMBIENTE_HOMOLOGACAO: {
            'servidor': 'homologacao.nfe.fazenda.sp.gov.br',
            WS_NFE_AUTORIZACAO: 'ws/nfeautorizacao4.asmx',
            WS_NFE_RET_AUTORIZACAO: 'ws/nferetautorizacao4.asmx',
            WS_NFE_INUTILIZACAO: 'ws/nfeinutilizacao4.asmx',
            WS_NFE_CONSULTA: 'ws/nfeconsulta4.asmx',
            WS_NFE_SITUACAO: 'ws/nfestatusservico4.asmx',
            WS_NFE_CADASTRO: 'ws/cadconsultacadastro4.asmx',
            WS_NFE_RECEPCAO_EVENTO: 'ws/nferecepcaoevento4.asmx',
            WS_NFE_CANCELAMENTO: 'ws/nferecepcaoevento4.asmx',
        }
    },
    NFCE_MODELO: {
        NFCE_AMBIENTE_PRODUCAO: {
            'servidor': 'nfce.fazenda.sp.gov.br',
            WS_NFCE_AUTORIZACAO: 'ws/nfeautorizacao4.asmx',
            WS_NFCE_RET_AUTORIZACAO: 'ws/nferetautorizacao4.asmx',
            WS_NFCE_INUTILIZACAO: 'ws/nfeinutilizacao4.asmx',
            WS_NFCE_CONSULTA: 'ws/nfeconsulta4.asmx',
            WS_NFCE_SITUACAO: 'ws/nfestatusservico4.asmx',
            WS_NFCE_CADASTRO: 'ws/cadconsultacadastro4.asmx',
            WS_NFCE_RECEPCAO_EVENTO: 'ws/nferecepcaoevento4.asmx',
            WS_NFCE_QR_CODE: '',
        },
        NFCE_AMBIENTE_HOMOLOGACAO: {
            'servidor': 'homologacao.nfce.fazenda.sp.gov.br',
            WS_NFCE_AUTORIZACAO: 'ws/nfeautorizacao4.asmx',
            WS_NFCE_RET_AUTORIZACAO: 'ws/nferetautorizacao4.asmx',
            WS_NFCE_INUTILIZACAO: 'ws/nfeinutilizacao4.asmx',
            WS_NFCE_CONSULTA: 'ws/nfeconsulta4.asmx',
            WS_NFCE_SITUACAO: 'ws/nfestatusservico4.asmx',
            WS_NFCE_CADASTRO: 'ws/cadconsultacadastro4.asmx',
            WS_NFCE_RECEPCAO_EVENTO: 'ws/nferecepcaoevento4.asmx',
            WS_NFCE_QR_CODE: 'NFCEConsultaPublica/Paginas/ConstultaQRCode.aspx',
        }
    }
}


ESTADO_WS = {
    'AC': SVRS,
    'AL': SVRS,
    'AM': UFAM,
    'AP': SVRS,
    'BA': UFBA,
    'CE': UFCE,
    'DF': SVRS,
    'ES': SVRS,
    'GO': UFGO,
    'MA': SVAN,
    'MG': UFMG,
    'MS': UFMS,
    'MT': UFMT,
    'PA': SVAN,
    'PB': SVRS,
    'PE': UFPE,
    'PI': SVAN,
    'PR': UFPR,
    'RJ': SVRS,
    'RN': SVRS,
    'RO': SVRS,
    'RR': SVRS,
    'RS': UFRS,
    'SC': SVRS,
    'SE': SVRS,
    'SP': UFSP,
    'TO': SVRS,
}


#
# Informação obtida em
# http://www.nfe.fazenda.gov.br/portal/webServices.aspx
#  Última verificação: 15/08/2014 16:22
#
# Autorizadores em contingência:
# - UF que utilizam a SVC-AN - Sefaz Virtual de Contingência Ambiente Nacional:
#       AC, AL, AP, DF, ES, MG, PB, RJ, RN, RO, RR, RS, SC, SE, SP, TO
# - UF que utilizam a SVC-RS - Sefaz Virtual de Contingência Rio Grande do Sul:
#       AM, BA, CE, GO, MA, MS, MT, PA, PE, PI, PR
#

ESTADO_WS_CONTINGENCIA = {
    'AC': SVC_AN,
    'AL': SVC_AN,
    'AM': SVC_RS,
    'AP': SVC_AN,
    'BA': SVC_RS,
    'CE': SVC_RS,
    'DF': SVC_AN,
    'ES': SVC_AN,
    'GO': SVC_RS,
    'MA': SVC_RS,
    'MG': SVC_AN,
    'MS': SVC_RS,
    'MT': SVC_RS,
    'PA': SVC_RS,
    'PB': SVC_AN,
    'PE': SVC_RS,
    'PI': SVC_RS,
    'PR': SVC_RS,
    'RJ': SVC_AN,
    'RN': SVC_AN,
    'RO': SVC_AN,
    'RR': SVC_AN,
    'RS': SVC_AN,
    'SC': SVC_AN,
    'SE': SVC_AN,
    'SP': SVC_AN,
    'TO': SVC_AN,
}
