from psycopg2 import connect
from PIL import Image


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


def is_valid_image(path: str) -> bool:
    """Verify that the provided file is an image.

    Args:
        [path] (str): path to the file

    Returns:
        bool: whether a provided file is image or not.
    """
    try:
        img = Image.open(path)
        img.verify()
        return True
    except Exception:
        return False
