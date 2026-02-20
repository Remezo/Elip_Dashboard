import sys
import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

# Add the project root to the path so we can import pythonScripts
sys.path.insert(0, "/opt/airflow/app")


def run_cpi_task(**kwargs):
    from pythonScripts.cpiScrapper import run_cpi_scrapper
    run_cpi_scrapper()


def run_fred_scrapper_task(**kwargs):
    from pythonScripts.fredScrapper import run_fred_scrapper
    run_fred_scrapper()


def run_fred_processor_task(**kwargs):
    from pythonScripts.fredProcessor import run_fred_processor
    run_fred_processor()


default_args = {
    "owner": "ascentris",
    "depends_on_past": False,
    "start_date": datetime(2024, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="elip_dashboard_etl",
    default_args=default_args,
    description="Pull FRED/BLS CPI data, process, and load to PostgreSQL",
    schedule_interval="0 11 * * *",  # 6am EST = 11am UTC
    catchup=False,
    tags=["elip", "etl", "fred", "cpi"],
) as dag:

    cpi_scrapping = PythonOperator(
        task_id="cpi_scrapping",
        python_callable=run_cpi_task,
    )

    fred_scrapping = PythonOperator(
        task_id="fred_scrapping",
        python_callable=run_fred_scrapper_task,
    )

    fred_processing = PythonOperator(
        task_id="fred_processing",
        python_callable=run_fred_processor_task,
    )

    # CPI and FRED scrapping run in parallel, then processing runs after FRED
    cpi_scrapping >> fred_scrapping >> fred_processing
