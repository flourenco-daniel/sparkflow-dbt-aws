from airflow.decorators import dag, task
from datetime import datetime


@dag(
    start_date=datetime(2025, 1, 1),
    dag_id="hello_dag",
    schedule=None,
    catchup=False,
    tags=['test']
)

def hello_dag():
    @task
    def print_hello():
        print("Hello, World!")
        return 42
    
    print_hello()

hello_dag()