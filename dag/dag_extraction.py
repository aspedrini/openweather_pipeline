import requests
import json
from datetime import datetime
import logging
import time
import tempfile
import pytz
import os
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow import DAG
from airflow.models import Variable


bucket = "weather-forecast-data-project"
s3_conn_id = "my_aws_conn"

weather_api = {
        "api_string":"http://api.openweathermap.org/data/2.5/weather?",
        "api_key" : Variable.get("weather_secret"),
        }

loc_dict = {
        "canasvieiras":["-27.432474", "-48.458959"],
        "jurere_internacional":["-27.440111","-48.500411"],
        "daniela":["-27.448554","-48.528955"],
        "ingleses":["-27.437205", "-48.397074"],
        "ingleses_rio_vermelho":["-27.452365", "-48.404403"],
        "santinho":["-27.451854", "-48.380068"],
        "rio_vermelho":["-27.491521", "-48.419974"],
        "mocambique":["-27.523353", "-48.422368"],
        "barra_lagoa":["-27.573298", "-48.430036"],
        "vargem_grande":["-27.455094", "-48.451343"],
        "ratones":["-27.507444", "-48.489221"],
        "sambaqui":["-27.488873", "-48.530391"],
        "santo_antonio_lisboa":["-27.511404", "-48.514606"],
        "saco_grande":["-27.540534", "-48.505196"],
        "monte_verde":["-27.557358","-48.496941"],
        "joao_paulo":["-27.558264", "-48.513296"],
        "lagoa_conceicao":["-27.602038", "-48.469327"],
        "joaquina":["-27.627852", "-48.447848"],
        "itacorubi":["-27.593051", "-48.493413"],
        "corrego_grande":["-27.592178", "-48.503699"],
        "carvoeira":["-27.603718", "-48.524888"],
        "carianos":["-27.663648", "-48.535611"],
        "agronomica":["-27.574227", "-48.534164"],
        "centro":["-27.592196", "-48.552793"],
        "rio_tavares":["-27.643884", "-48.475808"],
        "campeche":["-27.676458", "-48.486942"],
        "tapera":["-27.693425", "-48.550285"],
        "ribeirao_ilha":["-27.713703", "-48.561288"],
        "armacao":["-27.751185", "-48.510064"],
        "pantano_sul":["-27.779205", "-48.509324"],
        "estreito":["-27.591386", "-48.576051"],
        "capoeiras":["-27.599920", "-48.592338"],
        "jardim_atlantico":["-27.580980", "-48.595838"]
        }


def api_call(request_string: str) -> json:
        
        try:
            response = requests.get(request_string)
            response.raise_for_status()
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Error: {e}")
            raise SystemExit(e)
        
        response_json = response.json()
        json_object = json.dumps(response_json)
        return json_object


def s3_store(name: str, json_object: json):

    br_timezone = pytz.timezone("America/Sao_Paulo")
    timestamp = datetime.now(br_timezone)

    full_key = f"raw/{timestamp.strftime('%Y-%m-%d')}/hour/{timestamp.strftime('%H')}/{name}.json"

    try:
        s3_hook = S3Hook(s3_conn_id)
        s3_hook.load_string(
            string_data=json_object,
            key=full_key,
            bucket_name=bucket,
            replace=True)
        logging.info(f"File '{name}.json' was stored succesfully")
    except Exception as e:
        logging.info(f"Error: {e}") 


def process():

    logging.info("Process started - Data extraction and S3 storing")

    try:
        for key, value in loc_dict.items():
            request_string = f"{weather_api['api_string']}&appid={weather_api['api_key']}&lat={value[0]}&lon={value[1]}"
            json_obj = api_call(request_string)
            s3_store(name=key, json_object=json_obj)
    except Exception as e:
        logging.error(f"Error: {e}")        
        
    logging.info("Process ended - Data extraction and S3 storing")


with DAG(
    dag_id="weather_api",
    start_date=datetime(2023, 10, 21),
    catchup=False,
    schedule="@hourly",
    tags=["api extraction", "s3 store"],
    ) as dag:

    task1 = PythonOperator(
        task_id="api_to_s3",
        python_callable=process,
    
    )

task1