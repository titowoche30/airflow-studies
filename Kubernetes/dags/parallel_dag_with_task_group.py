from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime

# args that must be common to all the tasks of the DAG
default_args = {
    'owner': 'cwoche',
    'start_date': datetime(2020,1,1)
}

with DAG(dag_id = 'parallel_dag_with_task_group',
         schedule_interval = '@daily',
         default_args = default_args,
         catchup = False) as dag:
         
         task_1 = BashOperator(
             task_id = 'task_1',
             bash_command = 'sleep 3'
             )
             
         with TaskGroup('processing_tasks') as processing_tasks:
             task_2 = BashOperator(
                 task_id = 'task_2',
                 bash_command = 'sleep 3'
                 )
            
             with TaskGroup('spark_tasks') as spark_tasks:
                 task_3 = BashOperator(
                     task_id = 'task_3',
                     bash_command = 'sleep 3'
                     )

             with TaskGroup('flink_tasks') as flink_tasks:
                 task_3 = BashOperator(
                     task_id = 'task_3',
                     bash_command = 'sleep 3'
                     )


         task_4 = BashOperator(
             task_id = 'task_4',
             bash_command = 'sleep 3'
             )
         
         task_1 >> processing_tasks >> task_4
