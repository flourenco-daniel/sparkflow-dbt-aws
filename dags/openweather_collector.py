from socket import timeout
import requests
import json
import os
from airflow.decorators import dag, task
from datetime import datetime, timedelta
from airflow.sensors.base import PokeReturnValue
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.hooks.base import BaseHook
from data.open_weather.tasks import _get_s3_connection, _get_open_weather, _store_weather_data, BUCKET_NAME

