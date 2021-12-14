import os
from contextlib import contextmanager
from psycopg2.extras import DictCursor
from config.env import environments as env
from psycopg2 import DatabaseError, connect


@contextmanager
def get_connection():
    try:
        conn = connect(
            database=os.getenv("db_database", env.db_database),
            user=os.getenv("db_username", env.db_username),
            password=os.getenv("db_password", env.db_password),
            host=os.getenv("db_host", env.db_host),
            port=os.getenv("db_port", env.db_port),
            options=f"-c search_path=dbo,{env.db_schema}"
        )
        if conn:
            print("Connection created successfully")

        cursor = conn.cursor(cursor_factory=DictCursor)
        yield cursor, conn

        cursor.close()
        conn.close()

    except DatabaseError as error:
        print("Error while connecting to PostgreSQL", error)
