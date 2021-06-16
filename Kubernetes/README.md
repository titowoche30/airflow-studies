# Running Astronomer's Helm Chart for Apache Airflow

## Related links
[Git Repository](https://github.com/astronomer/airflow-chart)

[Helm Page](https://artifacthub.io/packages/helm/apache-airflow/airflow)

[Astronomer's Registry of Airflow tools](https://registry.astronomer.io/)

## About this settings

 The changes made in the [values.yaml](Kubernetes/values.yaml) of this repository are present in the fields: 

1. [defaultAirflowRepository](https://github.com/titowoche30/airflow-studies/blob/b0ad37e818d80d1ed02b9c10d00979a73d25dd14/Kubernetes/values.yaml#L37)
2. [defaultAirflowTag](https://github.com/titowoche30/airflow-studies/blob/b0ad37e818d80d1ed02b9c10d00979a73d25dd14/Kubernetes/values.yaml#L40)
3. [extraEnvFrom](https://github.com/titowoche30/airflow-studies/blob/b0ad37e818d80d1ed02b9c10d00979a73d25dd14/Kubernetes/values.yaml#L228)
4. [dags.GitSync.enabled](https://github.com/titowoche30/airflow-studies/blob/b0ad37e818d80d1ed02b9c10d00979a73d25dd14/Kubernetes/values.yaml#L955)
5. [dags.gitSync.repo](https://github.com/titowoche30/airflow-studies/blob/b0ad37e818d80d1ed02b9c10d00979a73d25dd14/Kubernetes/values.yaml#L962)
6. [dags.gitSync.branch](https://github.com/titowoche30/airflow-studies/blob/b0ad37e818d80d1ed02b9c10d00979a73d25dd14/Kubernetes/values.yaml#L963)
7. [dags.gitSync.subPath](https://github.com/titowoche30/airflow-studies/blob/b0ad37e818d80d1ed02b9c10d00979a73d25dd14/Kubernetes/values.yaml#L972)
   

To run the helm chart of this repository:

1. `$ kind create cluster --name airflow-cluster --config Kubernetes/kind-cluster.yaml`
   
2. `$ kubectl create namespace airflow`
   
3. `$ kubectl apply -f Kubernetes/variables.yaml`
   1. When you create environment variables you can't see them from UI neither the CLI, just with python code, but you can check them like this:
   
	    `$ kubectl exec --stdin --tty airflow-webserver-id-id -n airflow -- /bin/bash`

        `$ python`
        
        `from airflow.models import Variable`

        `from airflow.hooks.base_hook import BaseHook`

        `Variable.get("my_s3_bucket")`

        `BaseHook.get_connection('postgres_default')`


   
4. `$ docker build -t my-airflow-custom:1.0.0 Kubernetes/.`
   
5. `$ kind load docker-image my-airflow-custom:1.0.0 --name airflow-cluster`
   
6. `$ helm repo add apache-airflow https://airflow.apache.org`
   
7. `$ helm repo update`
   
8. `$ helm search repo airflow`
   
9.  `$ helm install airflow apache-airflow/airflow --namespace airflow -f Kubernetes/values.yaml --debug --timeout 10m0s`
   
10. To watch the pods going up: `$ kubectl get pods -n airflow -o wide -w`
   
11. To bind the airflow webserver to localhost:8080 `$ kubectl port-forward --namespace airflow svc/airflow-webserver 8080:8080`


## Useful comands
`$ kubectl describe pod/airflow-scheduler-id-id -n airflow` to see all of the containers in this pod.

`$ kubectl logs airflow-scheduler-id-id -n airflow -c git-sync -f` to see the logs of the git-sync container

`$ kubectl exec --stdin --tty airflow-scheduler-id-id -n airflow -- /bin/bash -c 'airflow info'` to check the available providers

`$ kubectl exec --stdin --tty airflow-scheduler-id-id -n airflow -- /bin/bash -c 'pip list'` to check the installed python libs

`$ helm show values apache-airflow/airflow > Kubernetes/values_original.yaml` to get the original values of the chart

`$ helm upgrade --install airflow apache-airflow/airflow -f Kubernetes/values.yaml -n airflow --debug` to upgrade the helm release after changes in the values.yaml

`$ helm list -n airflow` to get informations about the helm release

`$ helm rollback revision_number` to get back to a previous revision

#

**PS:** I was not able to make the gitSync work with a private repository, but if you want to give it a shot, here the steps:

1. Add a public ssh key to the Deploy Key of your git repository that contains the dags
   
2. In `dags.gitSync`, change the fields `enabled`, `repo`, `branch`, `subPath`
   
3. Create a K8S secret that will hold your private ssh key: `$ kubectl create secret generic airflow-ssh-git-secret --from-file=gitSshkey=path/id_rsa -n airflow`
   
4. In `dags.gitSync`, change the field `sshKeySecret`
   
5. Run `$ helm upgrade --install airflow apache-airflow/airflow -f Kubernetes/values.yaml -n airflow --debug`
