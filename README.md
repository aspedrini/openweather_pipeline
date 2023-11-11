# Open Weather Map API Data Pipelines

## Objetivo

O objetivo deste projeto é adquirir maior vivência com ferramentas, infraestrutura cloud e Linux, assim como conceitos de ciência da computação e engenharia de dados. Neste primeiro momento, o projeto está sendo construído de forma a evitar a utilização de ferramentas provisionadas por estes serviços, embora supram várias das necessidades encontradas, e buscando ao máximo tendo seus códigos escritos para realização do consumo, tratamento e entrega dos dados. 

## Inspiração

Após realizar projetos/tasks em ambiente de produção consumindo diretamente de bancos de dados e projetos pessoais utilizando datasets já tratados por outros usuários, percebi que seria necessário para fixar alguns conteúdos aprendidos a criação de um projeto end-to-end, abrangendo todas as etapas do processo, desde a obtenção dos dados crus até a disponibilização para um hipotético usuário final.

## Escopo

O projeto é baseado no consumo por hora da API pública (v2.5) do openweathermap.org, e tem como input vários conjuntos de latitude e longitude do município de Florianópolis, abrangendo a maioria de seus bairros com localizações dentro e fora da ilha. 

A cloud utilizada no projeto é a AWS.

### Divisão das etapas principais

A primeira etapa é referente ao consumo, armazenamento e orquestração do processo;

A segunda é referente ao tratamento dos dados em novas camadas;

A terceira diz respeito à criação de um data warehouse para armazenar os dados de maneira relacional;

E por fim a quarta é referente à disponibilização dos dados do data warehouse através da criação de uma API disponibilizada via Elastic Beanstalk.

## Estrutura do projeto

O consumo dos dados e orquestração na primeira etapa foi realizado utilizando Python e uma máquina provisionada via EC2 rodando Ubuntu 22.04, rodando Docker e um container com Airflow. O armazenamento dos arquivos json foi feito num bucket do S3 nomeado de "raw/", e para tal a DAG do Airflow utilizou o hook próprio do S3. A chave da API foi carregada via Variable na GUI do Airflow.

O tramento dos dados inicialmente foi escrito em Python, porém é de interesse utilizar o PySpark para tal.# openweather_pipeline
# openweather_pipeline
