# busca_ve
Este script realiza a análise de um banco de dados do **Sistema de Informação de Agravos de Notificação - SINAN** que tenha sido previamente geocodificado em um sistema de coordenadas UTM.
O objetivo é identificar casos suspeitos que tenham **vínculo epidemiológico** com casos confirmados por laboratório.
## Instalação no Windows (sem comandos GIT)
Este passo a passo pressupõe que o **Python 3** já esteja instalado no sistema e também que tenha sido adicionado ao "PATH" do Windows.
1. Através da opção **Code > Download ZIP** (acima), baixar o arquivo com o conteúdo deste repositório
![Screenshot](https://github.com/blueparrot/busca_ve/blob/main/screenshot.png)
2. Extrair o arquivo ZIP na pasta de sua preferência
3. Navegar até sua pasta pelo **Explorador de Arquivos** do Windows
4. Com a pasta aberta, segure a tecla **shift** do teclado e clique na janela com o botão **direito** do mouse
5. No menu, selecione a opção "Abrir janela do PowerShell aqui"
6. Na janela do PowerShell, digite o comando `pip install -r requirements.txt` (certifique-se de estar na mesma pasta onde extraiu os arquivos)
## Utilização
O arquivo DBF a ser analisado deve ser copiado para a pasta do script. Para realizar a análise, abra a janela do PowerShell nesse local (como nos passos 3, 4 e 5 da instalação) e digite o comando:

`python busca_ve.py`

Durante a execução, o script vai solicitar que seja digitado o nome do arquivo DBF. O resultado da análise será salvo na mesma pasta, mas com a extensão **CSV**.
## Preferências
O arquivo **preferencias.ini** pode ser modificado com qualquer editor de texto. Através dele podem ser feitos ajustes a eventuais alterações nos "dicionários de dados" do SINAN ou nos parâmetros considerados para vínculo epidemiológico. Como padrão, estão configurados os seguintes critérios:
- Distância de casos confirmados laboratorialmente em **raio de 200 metros**
- Intervalo de **15 dias** antes ou depois de casos confirmados laboratorialmente

Caso seja editado, o arquivo **preferencias.ini** precisa ser salvo com a codificação **UTF-8**.
