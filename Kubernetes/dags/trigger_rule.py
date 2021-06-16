from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

'''
Trigger Rules

[task_a_task_b] >> task_c

1. all_sucess (default behavior) = If task_a AND task_b succeeded => task_c will be executed
                If task_a OR task_b fails => task_c will be on upstream_failed status

2. all_failed = If task_a AND task_b failed => task_c will be executed
                If task_a OR task_b succeeded => task_c will be skiped

3. all_done = Executes task_c whetever the status of task_a and task_b (upstream tasks), as long as the upstream tasks get triggered, task_c will be triggered as well

4. one_success = Tigger task_c as soon as task_a OR task_b succeeded 

5. one_failed = Tigger task_c as soon as task_a OR task_b failed

6. none_failed = Tigger task_c as long as all upstream tasks have succeeded or have been skipped, all upstream tasks must either succeed or be skipped

7. none_failed_or_skipped = Tigger task_c as long as all upstream tasks haven't failed and a least one succeded     

'''


default_args = {
    'start_date': datetime(2020, 1, 1)
}

with DAG('trigger_rule', schedule_interval='@daily', default_args=default_args, catchup=False) as dag:

    task_1 = BashOperator(
        task_id = 'task_1',
        bash_command = 'exit 0',
        do_xcom_push = False
    )

    task_2 = BashOperator(
        task_id = 'task_2',
        bash_command = 'exit 1',
        do_xcom_push = False
    )

    task_3 = BashOperator(
        task_id = 'task_3',
        bash_command = 'exit 0',
        do_xcom_push = False,
        trigger_rule = 'one_failed'
    )

    [task_1, task_2] >> task_3


