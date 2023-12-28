import logging
import os
import random

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from psycopg2 import OperationalError, ProgrammingError, connect

random.seed(42)

db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")
table_name = os.getenv("POSTGRES_TABLE")
db_host = os.getenv("DB_HOST")
db_port = int(os.getenv("DB_PORT"))

app = FastAPI()


def create_connection(
    db_name: str,
    db_user: str,
    db_password: str,
    db_host: str = "127.0.0.1",
    db_port: int = 5432,
):
    """Create connection to a Postgres database.

    Args:
        db_name (str): database name
        db_user (str): database user
        db_password (str): database password
        db_host (str, optional): database host. Defaults to '127.0.0.1'.
        db_port (int, optional): database port. Defaults to 5432.

    Returns:
        connection: psycopg2 connection instance
    """
    connection = connect(
        database=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
    )
    print("Connection to PostgreSQL DB successful")
    return connection


@app.get("/")
def check_connection_to_db():
    """Check db connectivity.

    Raises:
        HTTPException: some error happened

    Returns:
        PlainTextResponse or HTTPException
    """
    connection = create_connection(db_name, db_user, db_password, db_host, db_port)
    try:
        with connection.cursor():
            return PlainTextResponse(
                content="Successfully connected to db", status_code=200
            )

    except (OperationalError, ProgrammingError) as e:
        logging.warning(f"""The error '{e}' occurred""")
        raise HTTPException(status_code=400) from e

    finally:
        connection.close()


@app.get("/health")
def read_health():
    """Check service health.

    Returns:
        JSONResponse: OK response
    """
    return JSONResponse(content={"status": "OK"}, status_code=200)