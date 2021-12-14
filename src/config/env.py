from pydantic import BaseSettings


class Environments(BaseSettings):
    debug: bool = True
    app_title: str = 'Application Name'

    # postgres environment variables
    min_conn: int = 1
    max_conn: int = 1
    db_name: str = 'postgresql'
    db_host: str = '127.0.0.1'
    db_port: str = '5432'
    db_username: str = 'postgres'
    db_password: str = '0780887042'
    db_database: str = 'postgres'
    db_schema: str = 'ankaboot'


environments = Environments()
