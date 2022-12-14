# ==============================================================================
#
#             CONFIGURAÇÃO DE PREFERÊNCIAS DO SCRIPT "busca_ve.py"
#
#   IMPORTANTE: Este arquivo deve ser salvo com a codificação de texto UTF-8
#
# ==============================================================================
#
#                    CRITÉRIOS PARA VÍNCULO EPIDEMIOLÓGICO
#
# PERIODO: Número de DIAS, antes e após o início dos sintomas, em que
#          se considera o vínculo epidemiológico com um caso confirmado
# RAIO: Distância em METROS em que se considera o vínculo epidemiológico
#
PERIODO_ANTES = 15
PERIODO_DEPOIS = 15
RAIO = 200
# ==============================================================================
#
#                   PARÂMETROS DO BANCO DE DADOS DE ENTRADA
#
# COL_DTSIN: Coluna que contém a data de início dos sintomas
# COL_CLASSIFIN: Coluna que contém a classificação final do caso
#                (confirmado, suspeito ou descartado)
# COL_CRITERIO: Coluna que contém o critério de confirmação
#               (laboratorial ou por vínculo epidemiológico)
# COL_X: Coluna que contém a coordenada X (UTM)
# COL_Y: Coluna que contém a coordenada Y (UTM)
# CODEPAGE: "Code Page" usada no banco de dados
#
COL_DTSIN = "DT_SIN_PRI"
COL_CLASSIFIN = "CLASSI_FIN"
COL_CRITERIO = "CRITERIO"
COL_X = "X"
COL_Y = "Y"
# ==============================================================================
#
#                        DICIONÁRIO DE DADOS DO SINAN
#
# CLASSIFIN_CONF: Valores interpretados como casos CONFIRMADOS
# CLASSIFIN_DESC: Valores interpretados como casos DESCARTADOS
# CRITERIO_LAB: Valores interpretados como CONFIRMAÇÃO LABORATORIAL
#
# OBSERVAÇÕES:
# 1) Os valores devem ser listados entre colchetes [] e, quando houver
#    mais de um, devem estar separados por vírgula
# 2) Para a coluna de classificação final, outros valores não listados
#    abaixo ou dados ausentes serão interpretados como casos SUSPEITOS
# 3) Para a coluna de critério de confirmação, outros valores não listados
#    abaixo ou dados ausentes serão interpretados como confirmação por
#    VÍNCULO EPIDEMIOLÓGICO (se aplica apenas a casos confirmados)
#
CLASSIFIN_CONF = [10, 11, 12]
CLASSIFIN_DESC = [5]
CRITERIO_LAB = [1]
# ==============================================================================
#
#                      PREFERÊNCIAS DO ARQUIVO DE SAÍDA
#
# TEXTO_CONF_LAB: Registro para casos confirmados laboratorialmente
# TEXTO_CONF_VE: Registro para casos confirmados por vínculo epidemiológico
# TEXTO_SUSP_VE: Registro para casos suspeitos COM vínculo epidemiológico
# TEXTO_SUSP: Registro para casos suspeitos SEM vínculo epidemiológico
# TEXTO_DESCART: Registro para casos descartados
# CODEPAGE_SAIDA: "Code Page" usada no CSV de saída
#
TEXTO_CONF_LAB = "Confirmado LAB"
TEXTO_CONF_VE = "Confirmado VE"
TEXTO_SUSP_VE = "Suspeito com VE"
TEXTO_SUSP = "Suspeito"
TEXTO_DESCART = "Descartado"
CODEPAGE_SAIDA = "cp1252"
