from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "de_team",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": False,
}

with DAG(
    dag_id="product_pipeline",
    default_args=default_args,
    description="E-commerce batch + streaming pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="0 2 * * *",       # နေ့စဉ် မနက် ၂ နာရီ
    catchup=False,
    max_active_runs=1,
    tags=["ecommerce", "batch"],
) as dag:

    # 1. Batch pipeline (extract → bronze → silver)
    run_batch = BashOperator(
        task_id="run_batch_pipeline",
        bash_command=(
            "docker exec spark-master "
            "/opt/spark/bin/spark-submit "
            "/app/batch/run_batch.py"
        ),
    )

    # 2. Merge silver (batch + streaming)
    merge_silver = BashOperator(
        task_id="merge_silver",
        bash_command=(
            "docker exec spark-master "
            "/opt/spark/bin/spark-submit "
            "/app/spark/merge_silver.py"
        ),
    )

    # 3. Build gold
    build_gold = BashOperator(
        task_id="build_gold",
        bash_command=(
            "docker exec spark-master "
            "/opt/spark/bin/spark-submit "
            "/app/spark/build_gold.py"
        ),
    )

    # 4. Load to Postgres
    load_postgres = BashOperator(
        task_id="load_postgres",
        bash_command=(
            "docker exec spark-master "
            "/opt/spark/bin/spark-submit "
            "/app/src/postgres_loader.py"
        ),
    )

    # Dependencies
    run_batch >> merge_silver >> build_gold >> load_postgres