from airflow.utils.edgemodifier import Label
from datetime import datetime, timedelta
from textwrap import dedent
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow import DAG
from airflow.models import Variable
import pandas as pd
import sqlite3 as sql 

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['gabriela.siston@indicium.tech'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


## Do not change the code below this line ---------------------!!#
def export_final_answer():
    import base64

    # Import count
    with open('count.txt') as f:
        count = f.readlines()[0]

    my_email = Variable.get("my_email")
    message = my_email+count
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')

    with open("final_output.txt","w") as f:
        f.write(base64_message)
    return None
## Do not change the code above this line-----------------------##

with DAG(
    'DesafioAirflow',
    default_args=default_args,
    description='Desafio de Airflow da Indicium',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['example'],
) as dag:
    dag.doc_md = """
        Esse é o desafio de Airflow da Indicium.
    """

    #Definindo a função py
    def sqlite_csv():
        #Conectando ao banco de dados
        conexao = sql.connect('./Northwind_small.sqlite', isolation_level=None,
        detect_types=sql.PARSE_COLNAMES)
        #Fazendo a consulta do campo "Order"
        sql_conection = """
        SELECT * FROM "Order"
        """
        #Armazena a consulta em um dataframe
        db_df = pd.read_sql_query(sql_conection, conexao)
        #Cria um arquivo csv com o resultado da consulta
        db_df.to_csv('./output_orders.csv', index=False)
    
    #Declarando o PyOperator para exportar o csv
    export_csv = PythonOperator(
        task_id='sqlite_csv',
        python_callable=sqlite_csv,
        provide_context=True
    )
    
    #Definindo a função py
    def count_to_txt():
        #Conectando ao bando de dados
        conexao = sql.connect('./Northwind_small.sqlite', isolation_level=None,
        detect_types=sql.PARSE_COLNAMES)
        #Consulta a tabela "OrderDetail"
        sql_conection = """
            SELECT * FROM OrderDetail
        """
        #Armazena a consulta em um dataframe
        orderdetails_df = pd.read_sql_query(sql_conection, conexao)
        #Armazena as informações do csv em um dataframe
        orders_df = pd.read_csv('./output_orders.csv')
        #Utilizando a função merge para fundir (join) as informações do database com os dados do csv
        df_join = pd.merge(orderdetails_df, orders_df, how='inner', left_on = 'OrderId', right_on = 'Id')
        #Fazendo a soma do total de pedidos, somente para a cidade do Rio de Janeiro
        df_query = df_join.query('(ShipCity == "Rio de Janeiro")')['Quantity'].sum()
        #Criando o arquivo txt com o resultado da consulta
        txt = open("count.txt", "a")
        #Transformando o resultado inteiro do df para string
        df_query_string = df_query.astype(str)
        #Escrevendo o txt com string
        txt.write(df_query_string)

    #Declarando o PyOperator do count_txt
    export_txt = PythonOperator(
        task_id='count_to_txt',
        python_callable=count_to_txt,
        provide_context=True
    )

    #Declarando o PyOperator do final_output.txt 
    export_final_output = PythonOperator(
        task_id='export_output',
        python_callable=export_final_answer,
        provide_context=True
    )

    #Ordenando a execução de tasks
    export_csv >> export_txt >> export_final_output