from airflow.hooks.base import BaseHook
import json
import os
import boto3
from dotenv import load_dotenv
from io import BytesIO
from botocore.exceptions import ClientError

load_dotenv()


BUCKET_NAME= "open-mobility-etl-demo"

def _get_s3_connection():
    conn = BaseHook.get_connection("aws_default")

    s3 = boto3.client("s3",
    aws_access_key_id=conn.login,
    aws_secret_access_key=conn.password,
    region_name=conn.extra_dejson['region_name']
    )
    return s3

def _get_open_weather(lat, lon):
    import requests

    api = BaseHook.get_connection('api_weather')
    api_key= api.extra_dejson['api_key']
    url = "https://api.openweathermap.org/data/3.0/onecall"
    exclude = "minutely,daily"

    url = f"{url}?lat={lat}&lon={lon}&exclude{exclude}&appid={api_key}"
    response = requests.get(url)
    return json.dumps(response.json())

def _store_weather_data(weather_data):
    client = _get_s3_connection()

    try:
        client.head_bucket(Bucket=BUCKET_NAME)
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            client.create_bucket(Bucket=BUCKET_NAME)

    weather_data = json.loads(weather_data)
    location = weather_data.get('lat', 'lon')
    data = json.dumps(weather_data, ensure_ascii=False).encode('utf8')

    objw = client.put_object(
        Bucket=BUCKET_NAME,
        object_name=f'raw/weather/{location}/weather_data.json',
        data=BytesIO(data),
        length=len(data)
    )

    return f"{objw.Bucket}/{location}"