from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.subdag import SubDagOperator
from datetime import datetime
from subdags import subdag_parallel_dag

# args that must be common to all the tasks of the DAG
default_args = {
    'owner': 'cwoche',
    'start_date': datetime(2020,1,1)
}

with DAG(dag_id = 'parallel_dag_with_subdag',
         schedule_interval = '@daily',
         default_args = default_args,
         catchup = False) as dag:

        task_1 = BashOperator(
                task_id = 'task_1',
                bash_command = 'sleep 3'
                )

        processing = SubDagOperator(
                task_id = 'processing_tasks',
                subdag = subdag_parallel_dag(parent_dag_id = 'parallel_dag_with_subdag', child_dag_id ='processing_tasks', default_args = default_args )
        )

        task_4 = BashOperator(
                task_id = 'task_4',
                bash_command = 'sleep 3'
                )


        task_1 >> processing >> task_4

        