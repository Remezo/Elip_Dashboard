from fred_scrapper import run_fred_scrapper
from EDAv2 import run_fred_processor
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta


default_args = {
    'owner': 'Ascentris',
    'depends_on_past': False,
    'start_date': datetime(2023, 6, 7),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
    
}
dag = DAG(
    'fred_dag',
    default_args=default_args,
    description='Our first DAG with ETL process!',
    schedule_interval=timedelta(days=1),
)

data_fetch= PythonOperator(
    task_id='data_Scrapping'
    python_callable= run_fred_scrapper
    dag=dag
)
data_processing= PythonOperator(
    task_id='data_processing'
    python_callable= run_fred_scrapper
    dag=dag
)