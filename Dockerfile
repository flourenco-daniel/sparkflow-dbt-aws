# Usamos a imagem oficial do Airflow
FROM apache/airflow:3.0.6


RUN pip install --no-cache-dir \
    dbt-core==1.9.0 \
    dbt-athena==1.9.0

