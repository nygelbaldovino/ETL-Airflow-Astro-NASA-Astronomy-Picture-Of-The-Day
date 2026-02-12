from airflow import DAG
from airflow.providers.http.operators.http import HttpOperator
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import json

## Define the DAG
with DAG(
    dag_id = 'nasa_apod_postgres',
    start_date = datetime(2026, 2, 10),
    schedule = '@daily',
    catchup = False
) as dag:
    

    ## Task 1: Create a table if does not exist
    @task
    def create_table():
        ## Initialize Postgres Hook
        postgres_hook = PostgresHook(postgres_conn_id='my_postgres_connection')

        ## SQL query to create table
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS apod_data(
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            explanation TEXT,
            url TEXT,
            date DATE,
            media_type VARCHAR(50)
        );
        '''
        ## Execute the table query
        postgres_hook.run(create_table_query)


    ## Task 2: Extract the NASA API Data (APOD) [Extract Pipeline]
    ## https://api.nasa.gov/planetary/apod?api_key=VQP7F1ZI4wt4QtAXd6xeGIEMXCHk4EaPWqRxmfeA
    extract_apod = HttpOperator(
        task_id = 'extract_apod',
        http_conn_id = 'nasa_api', ## Will map to "api.nasa.gov" URL. Connection ID Defined in Airflow for NASA API
        endpoint = 'planetary/apod', ## End point from the URL before the ?api_key
        method = 'GET',
        data = {'api_key':'{{conn.nasa_api.extra_dejson.api_key}}'}, ## Using the API key from the connection
        response_filter = lambda response: response.json() ## Convert response to JSON
    )


    ## Task 3: Transform the data 
    @task
    def transform_apod_data(response):
        apod_data={
            'title' : response.get('title', ''), ## '' means if the key is not available it will give blank
            'explanation' : response.get('explanation', ''),
            'url' : response.get('url', ''),
            'date' : response.get('date', ''),
            'media_type' : response.get('media_type', '')
        }
        return apod_data


    ## Task 4: Load the data into Postgres
    @task
    def load_data_to_postgres(apod_data):
        ## Initialize the postgres
        postgres_hook = PostgresHook(postgres_conn_id='my_postgres_connection')

        ## Define the SQL query
        insert_query = '''
        INSERT INTO apod_data (title, explanation, url, date, media_type)
        VALUES (%s, %s, %s, %s, %s);
        '''

        ## Execute the SQL query
        ## Use Parameters to avoid SQL Injection Attacks
        postgres_hook.run(insert_query, parameters = (
            apod_data['title'],
            apod_data['explanation'],
            apod_data['url'],
            apod_data['date'],
            apod_data['media_type']
        ))


    ## Task 5: Verify the data DBViewer

    ## Task 6: Define the task dependencies
    ## Extract
    create_table() >> extract_apod ## Ensuring a table is created before extracting
    api_response = extract_apod.output ## HTTP operator will have an output where the entire response is available

    ## Transform (In real life you are extracting from different sources plus cleaning the data)
    transformed_data = transform_apod_data(api_response)

    ## Load
    load_data_to_postgres(transformed_data)