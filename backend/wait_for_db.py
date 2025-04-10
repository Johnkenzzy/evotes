import time
import psycopg
from psycopg.errors import OperationalError

while True:
    try:
        conn = psycopg.connect(
            dbname="evotes_dev_db",
            user="evotes_dev",
            password="evotes_dev_pwd",
            host="db",
            port="5432",
        )
        conn.close()
        break
    except OperationalError:
        print("Waiting for database to be ready...")
        time.sleep(1)
