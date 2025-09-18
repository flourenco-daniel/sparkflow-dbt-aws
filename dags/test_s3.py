from airflow.decorators import dag, task
from datetime import datetime
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

@dag(
    start_date=datetime(2025, 1, 1),
    dag_id="test_s3",
    schedule=None,
    catchup=False,
    tags=['test']
)
def test_s3():
    @task
    def test_s3_task():
        hook = S3Hook(aws_conn_id="aws_default")
        hook.load_file(
            filename="/opt/airflow/data/test.txt",
            key="test.txt",
            bucket_name="open-mobility-etl-demo"
        )
        return "Uploaded!"
    
    test_s3_task()

test_s3()