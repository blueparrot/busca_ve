#! python3
import os
import csv
import json
import datetime
from configparser import ConfigParser

import numpy as np
from dbfread import DBF
from tqdm import tqdm

# Carrega o arquivo preferencias.ini e atribui variáveis globais
preferencias = ConfigParser()
preferencias.read('preferencias.ini', encoding='utf-8')
PERIODO_ANTES = int(preferencias['CRITERIOS_VE']['PERIODO_ANTES'])
PERIODO_DEPOIS = int(preferencias['CRITERIOS_VE']['PERIODO_DEPOIS'])
RAIO = int(preferencias['CRITERIOS_VE']['RAIO'])
COL_DTSIN = preferencias['BANCO']['COL_DTSIN']
COL_CLASSIFIN = preferencias['BANCO']['COL_CLASSIFIN']
COL_CRITERIO = preferencias['BANCO']['COL_CRITERIO']
COL_X = preferencias['BANCO']['COL_X']
COL_Y = preferencias['BANCO']['COL_Y']
CODEPAGE = preferencias['BANCO']['CODEPAGE']
CLASSIFIN_CONF = json.loads(preferencias['VALORES']['CLASSIFIN_CONF'])
CLASSIFIN_DESC = json.loads(preferencias['VALORES']['CLASSIFIN_DESC'])
CRITERIO_LAB = json.loads(preferencias['VALORES']['CRITERIO_LAB'])
TEXTO_CONF_LAB = preferencias['TEXTO_SAIDA']['TEXTO_CONF_LAB']
TEXTO_CONF_VE = preferencias['TEXTO_SAIDA']['TEXTO_CONF_VE']
TEXTO_SUSP_VE = preferencias['TEXTO_SAIDA']['TEXTO_SUSP_VE']
TEXTO_SUSP = preferencias['TEXTO_SAIDA']['TEXTO_SUSP']
TEXTO_DESCART = preferencias['TEXTO_SAIDA']['TEXTO_DESCART']
CODEPAGE_SAIDA = preferencias['TEXTO_SAIDA']['CODEPAGE_SAIDA']


def distancias_utm(caso, confirmados_periodo):
    '''
    Calcula distância em metros entre um caso e a seleção de casos confirmados
    que ocorreram no mesmo período
    '''
    confirmados_x = []
    confirmados_y =[]
    for c in confirmados_periodo:
        confirmados_x.append(c['X'])
        confirmados_y.append(c['Y'])
    dif_x = np.subtract(caso[COL_X],np.array(confirmados_x))
    dif_y = np.subtract(caso[COL_Y],np.array(confirmados_y))
    distancias = np.sqrt(np.power((dif_x),2)+np.power((dif_y),2))
    return distancias


def vinculo_epi(caso,confirmados_lab):
    '''
    Pesquisa o vínculo epidemiológico de um caso suspeito, considerando a lista
    de casos com confirmação laboratorial coletada previamente
    '''
    # Retorna ausência de vínculo epidemilógico se o caso não estiver geocodificado
    if caso[COL_X] < 1:
        return TEXTO_SUSP

    # Determina as datas limite do período de transmissão para o caso analisado
    dt_min = caso[COL_DTSIN] - datetime.timedelta(days=PERIODO_ANTES)
    dt_max = caso[COL_DTSIN] + datetime.timedelta(days=PERIODO_DEPOIS)

    # Coleta os casos confirmados com início dentro do período de transmissão
    confirmados_periodo = []
    for c in confirmados_lab:
        if (c['DTSIN'] >= dt_min) and (c['DTSIN'] <= dt_max):
            confirmados_periodo.append(c)

    # Retorna ausência de vínculo epidemilógico se não houver casos confirmados no período
    if len(confirmados_periodo) == 0:
        return TEXTO_SUSP
    
    # Calcula distância entre o caso suspeito e os casos confirmados do período
    distancias = distancias_utm(caso, confirmados_periodo)
    
    # Retorna presença de vínculo epidemiológico se houver casos confirmados próximos
    if True in np.less_equal(distancias, RAIO):
        return TEXTO_SUSP_VE
    else:
        return TEXTO_SUSP


def diagnostico(caso,confirmados_lab):
    '''
    Analisa o diagnóstico de um caso do banco de dados, considerando os dados de
    classificação final e critério de diagnóstico
    Para casos suspeitos, é acionada a busca por vínculos epidemiológicos  
    '''
    try:
        if int(caso[COL_CLASSIFIN]) in CLASSIFIN_DESC:
            return TEXTO_DESCART
        elif int(caso[COL_CLASSIFIN]) in CLASSIFIN_CONF:
            if int(caso[COL_CRITERIO]) in CRITERIO_LAB:
                return TEXTO_CONF_LAB
            else:
                return TEXTO_CONF_VE
        else:
            return vinculo_epi(caso,confirmados_lab)
    except:
        return vinculo_epi(caso,confirmados_lab)


def main():
    '''
    Função principal do script
    '''
    os.system('cls')

    # Valida a existência do arquivo DBF informado
    dbf_validado = False
    while dbf_validado == False:
        print('Favor digitar o nome do banco de dados DBF a ser analisado: ', end='')
        DBF_AGRAVO = input()
        if DBF_AGRAVO[-4:].upper() != '.DBF':
            print('O arquivo informado não tem a extensão .DBF.')
            print('(Para sair, digite CRTL + C)\n')
            continue
        if os.path.isfile(DBF_AGRAVO) == False:
            print('Arquivo não encontrado. Favor digitar o caminho completo ou copiar o DBF para a pasta do programa.')
            print('(Para sair, digite CRTL + C)\n')
            continue
        dbf_validado = True

    # Carrega DBF
    base_sinan = DBF(DBF_AGRAVO, encoding=CODEPAGE)

    # Coleta casos confirmados laboratorialmente
    confirmados_lab = []
    for r in tqdm(base_sinan, desc='Coletando casos confirmados por laboratório'):
        try:
            if (int(r[COL_CLASSIFIN]) in CLASSIFIN_CONF) and (int(r[COL_CRITERIO]) in CRITERIO_LAB):
                if int(r[COL_X]) < 1: # Elimina casos não geocodificados
                    continue
                confirmados_lab.append(
                    {
                        'DTSIN': r[COL_DTSIN],
                        'X': int(r[COL_X]),
                        'Y': int(r[COL_Y])
                    }
                )
        except:
            continue
    
    # Cria o arquivo CSV de saída
    RESULTADO = DBF_AGRAVO[:-4] + '.csv'
    with open(RESULTADO, 'w', newline='', encoding=CODEPAGE_SAIDA) as arquivo:
        writer = csv.writer(arquivo, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # Grava cabeçalho, acrescentando a coluna 'BUSCA_VE'
        writer.writerow(base_sinan.field_names + ['BUSCA_VE'])
        # Grava registros do DBF, acrescentando a coluna 'BUSCA_VE'
        for r in tqdm(base_sinan, desc='Analisando vínculos epidemiológicos'):
            try:
                d = [diagnostico(r,confirmados_lab)]
            except:
                d = ['ERRO']
            writer.writerow(list(r.values()) + d)
    
    # Sinaliza fim
    print(f'Resultado da análise salvo em {RESULTADO}')


if __name__ == "__main__":
    main()
