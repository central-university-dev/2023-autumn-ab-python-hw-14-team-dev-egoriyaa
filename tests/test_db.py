import pytest
from abc.db import DataBase
import os

db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")
table_name = os.getenv("POSTGRES_TABLE")
db_host = os.getenv("DB_HOST")
db_port = int(os.getenv("DB_PORT"))


def test_connect_db():
    db = DataBase(db_name=db_name, db_user=db_user, db_password=db_password)
    db.connection.close()


def test_create_db():
    db = DataBase(db_name=db_name, db_user=db_user, db_password=db_password)
    db.create_db()
    db.execute_query(f"DROP DATABASE {db_name}")
    db.connection.close()


def test_create_table():
    db = DataBase(db_name=db_name, db_user=db_user, db_password=db_password)
    db.create_db()
    db.create_table()
    db.execute_query(f"DROP TABLE {table_name}")
    db.execute_query(f"DROP DATABASE {db_name}")
    db.connection.close()


def test_insert_data_into_table():
    db = DataBase(db_name=db_name, db_user=db_user, db_password=db_password)
    db.create_db()
    db.create_table()
    db.insert_label_into_table('123', '1')
    query = f"SELECT * FROM {table_name}"
    result = db.execute_read_query(query)
    assert result == [('123', '1')]
    db.execute_query(f"DROP TABLE {table_name}")
    db.execute_query(f"DROP DATABASE {db_name}")
    db.connection.close()


@pytest.mark.parametrize('image_hash, expected_result', [('123', '1'), ("1234", False)])
def test_insert_data_into_table(image_hash, expected_result):
    db = DataBase(db_name=db_name, db_user=db_user, db_password=db_password)
    db.create_db()
    db.create_table()
    db.insert_label_into_table('123', '1')
    result = db.find_picture_in_table(image_hash)
    assert result == expected_result
    db.execute_query(f"DROP TABLE {table_name}")
    db.execute_query(f"DROP DATABASE {db_name}")
    db.connection.close()
