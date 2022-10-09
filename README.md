# busca_ve
Este script realiza a análise de um banco de dados do Sistema de Informação de Agravos de Notificação - SINAN, em formato DBF.
O objetivo é identificar casos suspeitos que tenham **vínculo epidemiológico** com casos confirmados por laboratório.
## Instalação no Windows 10 (sem comandos GIT)
1. Através da opção **Code > Download ZIP** (acima), baixar o arquivo com o conteúdo deste repositório
2. Extrair o arquivo ZIP na pasta de sua preferência
3. Navegar até sua pasta pelo **Explorador de Arquivos** do Windows
4. Com a pasta aberta, segure a tecla **shift** do teclado e clique na janela com o botão **direito** do mouse
5. No menu, selecione a opção "Abrir janela do PowerShell aqui"
6. Na janela do PowerShell, digite o comando `pip install -r requirements.txt` (certifique-se de estar na mesma pasta onde extraiu os arquivos)
## Utilização
O arquivo DBF a ser analisado deve ser copiado para a pasta do script. Para realizar a análise, abra a janela do PowerShell nessa pasta e digite o comando:

`python busca_ve.py ARQUIVO.DBF` (substitua *ARQUIVO.DBF* pelo nome do arquivo a ser analisado)

O resultado da análise será salvo no mesmo local do arquivo **DBF**, mas com a extensão **CSV**.
## Preferências
O arquivo **preferencias.ini** pode ser modificado com qualquer editor de texto. Através dele podem ser feitos ajustes a eventuais alterações nas nomenclaturas adotadas nos bancos de dados ou nos parâmetros considerados para vínculo epidemiológico. Como padrão, estão configurados os seguintes critérios:
- Distância de casos confirmados laboratorialmente em **raio de 200 metros**
- Intervalo de **15 dias** antes ou depois de casos confirmados laboratorialmente

Caso seja editado, esse arquivo precisa ser salvo com a codificação **UTF-8**.
