from pythonScripts.fredScrapper import run_fred_scrapper
from pythonScripts.fredProcessor import run_fred_processor
from pythonScripts.cpiScrapper import run_cpi_scrapper
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta



default_args = {
    'owner': 'Ascentris',
    'depends_on_past': False,
    'start_date': datetime(2023, 6, 7),
    'email': ['mike.remezo@ascentris.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
    
}
dag = DAG(
    'fred_dag',
    default_args=default_args,
    description='Ascentris Dashboard',
    schedule_interval=timedelta(days=1),
)

CPIdata_fetch=PythonOperator(
    task_id='CPI_Scrapping',
    python_callable= run_cpi_scrapper,
    dag=dag,
)

Freddata_fetch= PythonOperator(
    task_id='fred_Scrapping',
    python_callable= run_fred_scrapper,
    dag=dag,
)
data_processing= PythonOperator(
    task_id='fred_processing',
    python_callable= run_fred_processor,
    dag=dag,
)

CPIdata_fetch>> Freddata_fetch >> data_processing