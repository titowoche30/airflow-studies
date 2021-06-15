from airflow.models import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
import json


# args that must be common to all the tasks of the DAG
default_args = {
    'owner': 'cwoche',
    'start_date': datetime(2020,1,1)
}

def _processing_user(task_instance, file_path = '/tmp/processed_user.json'):
    # This task_instance is the current task instance and the .xcom_pull fetches the data from the airflow DB (postgres)
    users = task_instance.xcom_pull(task_ids = ['extracting_user'])
    if not len(users) or 'results' not in users[0]:
        raise ValueError('User is empty')
    
    user = users[0]['results'][0]
    processed_user = {
        'firstname': user['name']['first'],
        'lastname': user['name']['last'],
        'country': user['location']['country'],
        'username': user['login']['username'],
        'password': user['login']['password'],
        'email': user['email']
    }

    with open(file_path, "w+", encoding='utf-8') as outfile: 
        json.dump(processed_user, outfile, ensure_ascii=False)

def _loading_processed_user(file_path = '/tmp/processed_user.json'):
    processed_user = []
    try:
        with open(file_path,"r",encoding='utf-8') as user:
            processed_user = json.load(user)
    except Exception as e:
        print(e)
        raise ValueError('File does not exists')

    return processed_user


with DAG(dag_id = 'user_processing',
         schedule_interval = '@daily',
         default_args = default_args,
         catchup = False) as dag:
         
        creating_table =  PostgresOperator(
            task_id = 'creating_table',
            postgres_conn_id = 'postgres_default',
            sql='sql/users_schema.sql'
        )

        is_api_availabe = HttpSensor(
            task_id = 'is_api_available',
            http_conn_id = 'user_api',
            endpoint = 'api/'
        )

        extracting_user = SimpleHttpOperator(
            task_id = 'extracting_user',
            http_conn_id = 'user_api',
            endpoint = 'api/',
            method = 'GET',
            response_filter = lambda response: json.loads(response.text),
            log_response = True
        )

        processing_user = PythonOperator(
            task_id = 'processing_user',
            python_callable = _processing_user
        )

        loading_processed_user = PythonOperator(
            task_id = 'loading_processed_user',
            python_callable = _loading_processed_user
        )

        storing_user = PostgresOperator(
            task_id = "storing_user",
            postgres_conn_id = "postgres_default",
            sql = 'sql/insert_user.sql'
        )

        creating_table >> is_api_availabe >> extracting_user >> processing_user >> loading_processed_user >> storing_user