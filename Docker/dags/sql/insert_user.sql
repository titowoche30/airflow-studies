INSERT INTO users VALUES (
    '{{ ti.xcom_pull(task_ids = ['loading_processed_user'])[0]['firstname'] }}',
    '{{ ti.xcom_pull(task_ids = ['loading_processed_user'])[0]['lastname'] }}',
    '{{ ti.xcom_pull(task_ids = ['loading_processed_user'])[0]['country'] }}',
    '{{ ti.xcom_pull(task_ids = ['loading_processed_user'])[0]['username'] }}',
    '{{ ti.xcom_pull(task_ids = ['loading_processed_user'])[0]['password'] }}',
    '{{ ti.xcom_pull(task_ids = ['loading_processed_user'])[0]['email'] }}'
);
