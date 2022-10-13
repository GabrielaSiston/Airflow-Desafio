
# Desafio Airflow 

O Apache é uma plataforma para criar, agendar e monitorar fluxos de trabalho de forma programática. O Airflow é usado para criar fluxos de trabalho como gráficos acíclicos direcionados (DAGs) de tarefas. O scheduler do Airflow executa suas tasks em um array de workers enquanto segue as dependências especificadas. 

Neste desafio, o objetivo foi executar 4 tipos de tasks diferentes.

1ª Criar uma task que faz a leitura do campo "Order" do banco de dados Northwind_small.sqlit, exportando esse campo para um arquivo "output_orders.csv";

2ª Criar uma task que faz a leitura do campo "OrderDetail" do banco de dados Northwind_small.sqlit e faça um JOIN com o arquivo "output_orders.csv" exportado na tarefa anterior, calculando a quantidade de vendas ("Quantity" no banco) totais somente para a cidade do Rio de Janeiro (Informação disponível no campo "ShipCity" do banco de dados). E por fim, que exporte esse total em um arquivo "count.txt";

3ª Criação e adição de uma variável na interface do Airflow;

4ª Criar uma ordenação de execução das Tasks.

# 1. Instalação 
$ mkdir airflow-data

$ cd airflow-data 

### Crie um ambiente virtual em Python 
$ virtualenv venv -p python3

$ source venv/bin/activate

### Instale o airflow seguindo o guia da documentação

https://airflow.apache.org/docs/apache-airflow/stable/start.html

#### Observação 

O pip install deve ser executado dentro do seu ambiente virtual:

(venv)$ pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

Caso necessário, é preciso alterar caminhos relativos das DAGs para execução.
## 2. Execute o Airflow

Agora vamos inicializar a database, criar um usuário e startar todos os componentes para você


(venv)$ airflow standalone

Crie uma pasta chamada dags, em que vamos armazenar os fluxos implementados.

(venv)$ mkdir dags

## 3. Instale os "requirements"
(myvenv) $ python -m pip install -r requirements.txt


## 4. Features/Databases
Para a execução do projeto vamos precisar dos seguintes recursos:

Venv 

Airflow

Banco de Dados Northwind_small.sqlit

requirements.txt

## 5. Utilização do Airflow

Consultar documentação em: <https://airflow.apache.org/>

## 6. Sobre o autor

Mais informações em Linkedin 

 <https://www.linkedin.com/in/gabriela-siston-dos-santos-257479236/>




