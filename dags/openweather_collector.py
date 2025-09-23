from socket import timeout
import requests
import json
import os
from airflow.decorators import dag, task
from datetime import datetime, timedelta
from airflow.sensors.base import PokeReturnValue
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.hooks.base import BaseHook
from open_weather_tasks.tasks import  _get_open_weather, _store_weather_data, BUCKET_NAME

@dag(
    start_date = datetime(2025, 9, 23),
    schedule='@daily',
    catchup=True,
    tags=['weather_api'],

)

def open_weather():
    @task.sensor(poke_interval=30, timeout=300, mode='poke')
    def is_api_available() -> PokeReturnValue:
        import requests

        api = BaseHook.get_connection('api_weather')
        url = f"{api.host}lat={api.extra_dejson['test']}&lon={api.extra_dejson['test']}&exclude={api.extra_dejson['exclude_test']}&appid={api.extra_dejson['api_key']}"
        print(url)
        response = requests.get(url)
        print(response)
        condition = response.status_code == 200
        return PokeReturnValue(is_done=condition, xcom_value=url)

    @task
    def _get_open_weather():
        return _get_open_weather("-19.30", "-43.61")

