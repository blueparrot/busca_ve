#! python3
import os
import csv
import datetime

import colorama as color
import numpy as np
from dbfread import DBF
from tqdm import tqdm

import cli
import config
import file_parsing as fp

PASTA_RAIZ = os.path.dirname(__file__)
PASTA_ENTRADA = os.path.join(PASTA_RAIZ, "entrada")
PASTA_RESULTADO = os.path.join(PASTA_RAIZ, "resultado")
pastas = [PASTA_ENTRADA, PASTA_RESULTADO]
for pasta in pastas:
    if not os.path.exists(pasta):
        os.makedirs(pasta)


def distancias_utm(caso, confirmados_periodo):
    """
    Calcula distância em metros entre um caso e a seleção de casos confirmados que ocorreram no mesmo período
    """
    confirmados_x = []
    confirmados_y = []
    for c in confirmados_periodo:
        confirmados_x.append(c[config.COL_X])
        confirmados_y.append(c[config.COL_Y])
    dif_x = np.subtract(int(caso[config.COL_X]), np.array(confirmados_x))
    dif_y = np.subtract(int(caso[config.COL_Y]), np.array(confirmados_y))
    distancias = np.sqrt(np.power((dif_x), 2) + np.power((dif_y), 2))
    return distancias


def vinculo_epi(caso, confirmados_lab):
    """
    Pesquisa o vínculo epidemiológico de um caso suspeito, considerando a lista de casos com confirmação laboratorial coletada previamente
    """
    # Retorna ausência de vínculo epidemilógico se o caso não estiver geocodificado
    try:
        if int(caso[config.COL_X]) < 1:
            return config.TEXTO_SUSP
    except:
        return config.TEXTO_SUSP

    # Determina as datas limite do período de transmissão para o caso analisado
    dt_sint = caso[config.COL_DTSIN]
    dt_sint = datetime.date.fromisoformat(dt_sint) if type(dt_sint) == str else dt_sint
    dt_min = dt_sint - datetime.timedelta(days=config.PERIODO_ANTES)
    dt_max = dt_sint + datetime.timedelta(days=config.PERIODO_DEPOIS)

    # Coleta os casos confirmados com início dentro do período de transmissão
    confirmados_periodo = []
    for c in confirmados_lab:
        dt_sint_conf = c[config.COL_DTSIN]
        dt_sint_conf = datetime.date.fromisoformat(dt_sint_conf) if type(dt_sint_conf) == str else dt_sint_conf
        if (dt_sint_conf >= dt_min) and (dt_sint_conf <= dt_max):
            confirmados_periodo.append(c)

    # Retorna ausência de vínculo epidemilógico se não houver casos confirmados no período
    if len(confirmados_periodo) == 0:
        return config.TEXTO_SUSP

    # Calcula distância entre o caso suspeito e os casos confirmados do período
    distancias = distancias_utm(caso, confirmados_periodo)

    # Retorna presença de vínculo epidemiológico se houver casos confirmados próximos
    if True in np.less_equal(distancias, config.RAIO):
        return config.TEXTO_SUSP_VE
    else:
        return config.TEXTO_SUSP


def diagnostico(caso, confirmados_lab):
    """
    Analisa o diagnóstico de um caso do banco de dados, considerando os dados de classificação final e critério de diagnóstico
    Para casos suspeitos, é acionada a busca por vínculos epidemiológicos
    """
    try:
        if int(caso[config.COL_CLASSIFIN]) in config.CLASSIFIN_DESC:
            return config.TEXTO_DESCART
        elif int(caso[config.COL_CLASSIFIN]) in config.CLASSIFIN_CONF:
            if int(caso[config.COL_CRITERIO]) in config.CRITERIO_LAB:
                return config.TEXTO_CONF_LAB
            else:
                return config.TEXTO_CONF_VE
        else:
            return vinculo_epi(caso, confirmados_lab)
    except:
        return vinculo_epi(caso, confirmados_lab)


def busca_ve():
    """
    Função principal do script
    """
    # Interface de seleção de arquivo
    while True:
        cli.clear_screen()
        cli.print_title("BUSCA VE", color_back=color.Back.YELLOW)

        print(
            "Favor selecionar o arquivo CSV ou DBF a ser processado e pressionar <ENTER>\n"
        )
        print(
            "Para que os arquivos sejam exibidos entre as opções abaixo, é necessário\ncopiá-los para a pasta:\n"
        )
        cli.print_title(
            f"{PASTA_ENTRADA}",
            color_back=color.Back.RESET,
            color_fore=color.Fore.YELLOW,
        )
        arquivo = cli.file_selector(PASTA_ENTRADA, "CSV", "DBF")
        if arquivo == "*** Atualizar lista de arquivos ***":
            continue
        if arquivo == "<<<      Sair do programa       <<<":
            quit()
        caminho_arquivo = os.path.join(PASTA_ENTRADA, arquivo)

        break

    cli.clear_screen()
    cli.print_title("BUSCA VE", color_back=color.Back.YELLOW)
    print("")

    # Carrega os dados
    len_dados = len(list(fp.file_streamer(caminho_arquivo)))
    stream_dados_1 = fp.file_streamer(caminho_arquivo)
    stream_dados_2 = fp.file_streamer(caminho_arquivo)

    # Coleta casos confirmados laboratorialmente
    confirmados_lab = []
    print("Coletando casos confirmados por laboratório:")
    for r in tqdm(stream_dados_1, desc=color.Fore.YELLOW + "", total=len_dados):
        try:
            if (int(r[config.COL_CLASSIFIN]) in config.CLASSIFIN_CONF) and (
                int(r[config.COL_CRITERIO]) in config.CRITERIO_LAB
            ):
                if float(r[config.COL_X]) < 1:  # Elimina casos não geocodificados
                    continue
                confirmados_lab.append(
                    {
                        config.COL_DTSIN: r[config.COL_DTSIN],
                        config.COL_X: float(r[config.COL_X]),
                        config.COL_Y: float(r[config.COL_Y]),
                    }
                )
        except:
            continue
    print("")

    # Cria o arquivo CSV de saída
    resultado, _ = os.path.splitext(arquivo)
    resultado = os.path.join(PASTA_RESULTADO, resultado + ".csv")

    # Identifica casos com vínculo e salva no resultado
    with open(resultado, "w", newline="", encoding=config.CODEPAGE_SAIDA) as arquivo:
        writer = csv.writer(
            arquivo, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )

        # Grava cabeçalho, acrescentando a coluna 'BUSCA_VE'
        writer.writerow(fp.get_columns(caminho_arquivo) + ["BUSCA_VE"])

        # Grava registros, acrescentando a coluna 'BUSCA_VE'
        print("Analisando vínculos epidemiológicos:")
        for r in tqdm(stream_dados_2, desc=color.Fore.YELLOW + "", total=len_dados):
            try:
                col_ve = [diagnostico(r, confirmados_lab)]
            except:
                col_ve = ["ERRO"]
            writer.writerow(list(r.values()) + col_ve)

    # Sinaliza fim
    print("\n\nAnálise concluída com sucesso! Resultado salvo em:\n")
    cli.print_title(
        f"{resultado}", color_back=color.Back.BLACK, color_fore=color.Fore.YELLOW
    )

    # Opção de repetir
    print("Processar mais um arquivo?")
    repetir = cli.options("Sim", "Fechar programa")
    if repetir == "Sim":
        busca_ve()


def main():
    color.init(autoreset=True)
    busca_ve()
    color.deinit()


if __name__ == "__main__":
    main()
