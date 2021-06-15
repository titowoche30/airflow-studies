from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

# args that must be common to all the tasks of the DAG
default_args = {
    'owner': 'cwoche',
    'start_date': datetime(2020,1,1)
}

with DAG(dag_id = 'parallel_dag',
         schedule_interval = '@daily',
         default_args = default_args,
         catchup = False) as dag:

        task_1 = BashOperator(
                task_id = 'task_1',
                bash_command = 'sleep 3'
                )

        task_2 = BashOperator(
                task_id = 'task_2',
                bash_command = 'sleep 3'
                )

        task_3 = BashOperator(
                task_id = 'task_3',
                bash_command = 'sleep 3'
                )

        task_4 = BashOperator(
                task_id = 'task_4',
                bash_command = 'sleep 3'
                )

        #------THIS------
        task_1 >> [task_2, task_3] >> task_4

        #------OR THIS------

        # for i in [2,3]:
        #     task = BashOperator(
        #         task_id = f'task_{i}',
        #         bash_command = 'sleep 3'
        #         )
        #     task_1 >> task >> task_4

        #------OR THIS------

        
        # task_1 >> task_2 >> task_4
        # task_1 >> task_3 >> task_4

        