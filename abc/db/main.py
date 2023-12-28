from psycopg2 import connect
from typing import List, Tuple, Optional


class DataBase:
    """
    DataBase is the class to handle database for bird classification application.
    """

    def __init__(
        self,
        db_name: str,
        db_user: str,
        db_password: str,
        db_host: str = "127.0.0.1",
        db_port: int = 5432,
    ):
        """Init DataBase.
        Args:
            db_name (str): database name
            db_user (str): database user
            db_password (str): database password
            db_host (str, optional): database host. Defaults to '127.0.0.1'.
            db_port (int, optional): database port. Defaults to 5432.
        Returns:
            : psycopg2 connection instance
        """
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port

        self.connection = self._create_connection(
            db_name, db_user, db_password, db_host, db_port
        )

    def create_db(self):
        """Create database for bird classification application."""
        self.connection.autocommit = True
        cursor = self.connection.cursor()
        cursor.execute(f"CREATE DATABASE {self.db_name}")
        print("Query executed successfully")

    def create_table(self):
        """Create table to store information about pictures."""
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {self.} (
                image_hash TEXT PRIMARY KEY,
                label TEXT NOT NULL,
            )
        """
        self.execute_query(create_table_query)

    def execute_query(self, query: str, autocommit: bool = True):
        """Execute sql query without returning data.
        Args:
            query (str): sql query to execute
            autocommit (bool): whether to save state of connection automatically
        """
        if autocommit:
            self.connection.autocommit = autocommit
        cursor = self.connection.cursor()
        cursor.execute(query)
        print("Query executed successfully")
        if not autocommit:
            self.connection.commit()

    def execute_read_query(self, query: str) -> List[Tuple]:
        """Execute sql query with returning data.
        Args:
            query (str): sql query to execute
        Returns:
            : result of sql query execution
        """
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def find_picture_in_table(self, image_hash: str) -> Optional[str]:
        """Check whether image hash is already in database
        Args:
            image_hash (str): image hash
        Returns:
            : bird class for picture with image_hash if image_hash in table else False
        """
        query = f"SELECT label FROM abc WHERE image_hash = {image_hash}"
        result = self.execute_read_query(query)
        return result[0][0] if result else False

    def insert_label_into_table(self, image_hash: str, label: str):
        """Insert image_hash and label into table.
        Args:
            image_hash (str): image_hash
            label (str): bird class
        """
        data = (image_hash, label)
        insert_query = "INSERT INTO abc (image_hash, label) VALUES %s"
        self.connection.autocommit = True
        cursor = self.connection.cursor()
        cursor.execute(insert_query, data)
        self.connection.autocommit = False

    @staticmethod
    def _create_connection(
        db_name: str, db_user: str, db_password: str, db_host: str, db_port: int
    ):
        """Create connection with database.
        Args:
            db_name (str): database name
            db_user (str): database user
            db_password (str): database password
            db_host (str): database host
            db_port (int): database port
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
