In order to run script end to end please follow below main points:
- Create an env variable (check .env file included in this repo)
- Create virtual env. to isolate solution from other system modules/libraries.
- Execute script

Future TODOs
- Script can be inserted into apache airflow's DAG(Direct Acyclic Graph) and with a schedule it could be run on regular basis (as often as configuration details are needed)
References->https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/operators/postgres_operator_howto_guide.html
   