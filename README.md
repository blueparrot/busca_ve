# busca_ve
Este script realiza a análise de um banco de dados do **Sistema de Informação de Agravos de Notificação - SINAN**, em formato DBF, que tenha sido previamente geocodificado em um sistema de coordenadas UTM.
O objetivo é identificar casos suspeitos que tenham **vínculo epidemiológico** com casos confirmados por laboratório. Os critérios avaliados são a proximidade geográfica e a incidência em um mesmo intervalo de tempo, ambos configuráveis.

## Instalação no Windows
Este passo a passo pressupõe que o **Python 3** já esteja instalado no sistema. O script faz uso de alguns módulos externos que precisam ser baixados da internet. Isso é feito de forma "semi-automática" pela ferramenta **pip**, que faz parte do Python.

O processo pode ser ligeiramente diferente a dependar da distribuição do Python que estiver instalada (Anaconda, WinPython, etc), mas na versão básica é o seguinte:

1. Através da opção **Code > Download ZIP** (acima), baixar o arquivo com o conteúdo deste repositório

2. Extrair o arquivo ZIP na pasta de sua preferência

3. Navegar até esse local pelo **Explorador de Arquivos** do Windows

4. Com a pasta aberta, segure a tecla **shift** do teclado e clique em qualquer espaço da janela com o botão **direito** do mouse

5. No menu "pop up", selecione a opção **Abrir janela do PowerShell aqui** (ou **Abrir janela de comando aqui**, em versões mais antigas do Windows)

6. Checar se a linha de comando exibe o caminho da pasta correta. Opcionalmente, digite o comando **dir** (e tecle **Enter**) para se certificar de que o arquivo *requirements.txt* é listado

7. O ideal é que os módulos a serem baixados fiquem instalados em um *ambiente virtual* exclusivo deste script. Para criar esse ambiente, digite o comando: `python3 -m venv env` e tecle **Enter**

8. A depender da versão de terminal que estiver usando, digite um destes comandos para ativar o ambiente virtual:
    - **PowerShell:** `env\Scripts\activate.ps1`
    - **Prompt de Comando:** `env\Scripts\activate.bat`
    
    Atenção ao "S" maiúsculo.

9. Se o ambiente virtual foi ativado com sucesso, o indicador **(env)** vai aparecer antes da linha de comando. Isso feito, digite o comando `pip install -r requirements.txt` e tecle **Enter**

10. Os pacotes necessários serão instalados. Caso precise de informações mais detalhadas sobre ambientes virtuais, consulte as referências a seguir:
    - https://docs.python.org/pt-br/3/tutorial/venv.html
    - https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html

## Execução do programa
1. Navegar até a pasta do programa pelo **PowerShell** ou pelo **Prompt de Comando**, como descrito acima

2. Ativar o ambiente virtual:
    - **PowerShell:** `env\Scripts\activate.ps1`
    - **Prompt de Comando:** `env\Scripts\activate.bat`

3. Executar o comando: `python busca_ve.py`

**NOTA: Caso opte por instalar os pacotes na "raiz" do Python, sem o uso de ambiente virtual, os passos 7 e 8 da instalação e o passo 2 da execução podem ser ignorados.**

## Preferências
O arquivo **preferencias.ini** pode ser modificado com qualquer editor de texto. Através dele podem ser feitos ajustes a eventuais alterações nos "dicionários de dados" do SINAN ou nos parâmetros considerados para vínculo epidemiológico. Como padrão, estão configurados os seguintes critérios:
- Distância de casos confirmados laboratorialmente em **raio de 200 metros**
- Intervalo de **15 dias** antes ou depois de casos confirmados laboratorialmente

Caso seja editado, o arquivo **preferencias.ini** precisa ser salvo com a codificação **UTF-8**.
