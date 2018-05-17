# Dados Climáticos INMET
## Objetivo
O objetivo desse repositório é compartilhar leituras de dados climáticos de todas as estações automáticas do Brasil.  

## Fonte
Esses dados foram adiquiridos no [INMET - Istituto Nacional de Meteorologia](http://www.inmet.gov.br/portal/). Esses dados são abertos, caso seja necessário um outro período, é possível abrir uma solicitação diretamente no INMET via chamado (e se o fizer, sinta-se livre para fazer um pull request com os novos dados).

## Período
Os dados contidos nesse repositório são de 01/01/2010 até 31/12/2017.

## Parser
O fonte [data_parser.py](https://github.com/GuilhermeSpadaccia/dados_climaticos_inmet/blob/master/data_parser.py) faz a leitura do folder [Dados Climaticos](https://github.com/GuilhermeSpadaccia/dados_climaticos_inmet/tree/master/Dados%20Climaticos) e executa o parser dos arquivos gerando DataFrames com os dados. Esse arquivo deve ser alterado para salvar os DFs ou processa-los.

## Importante
Os dados estão zipados, para rodar o Parser é preciso descompactar os arquivos.
