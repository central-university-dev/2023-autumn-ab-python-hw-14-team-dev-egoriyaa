import pytest
from aic.db import DataBase
import os
from typing import List

db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")
table_name = os.getenv("POSTGRES_TABLE")
db_host = os.getenv("DB_HOST")
db_port = int(os.getenv("DB_PORT"))
query_drop_table = f"DROP TABLE IF EXISTS {table_name}"


def test_connect_db():
    db = DataBase(
        db_name=db_name,
        db_user=db_user,
        db_password=db_password,
        db_host=db_host,
        db_port=db_port,
    )
    db.connection.close()


def test_create_table():
    db = DataBase(
        db_name=db_name,
        db_user=db_user,
        db_password=db_password,
        db_host=db_host,
        db_port=db_port,
    )
    db.execute_query(query_drop_table)
    db.create_table()
    db.connection.close()


def test_insert_data_into_table():
    expected_result: List = [("123", "1")]
    db = DataBase(
        db_name=db_name,
        db_user=db_user,
        db_password=db_password,
        db_host=db_host,
        db_port=db_port,
    )
    db.execute_query(query_drop_table)
    db.create_table()
    db.insert_label_into_table("123", "1")
    query = f"SELECT * FROM {table_name}"
    result = db.execute_read_query(query)
    assert result == expected_result
    db.connection.close()


@pytest.mark.parametrize("image_hash, expected_result", [("123", "1"), ("1234", False)])
def test_find_picture_in_table(image_hash, expected_result):
    db = DataBase(
        db_name=db_name,
        db_user=db_user,
        db_password=db_password,
        db_host=db_host,
        db_port=db_port,
    )
    db.execute_query(query_drop_table)
    db.create_table()
    db.insert_label_into_table("123", "1")
    result = db.find_picture_in_table(image_hash)
    assert result == expected_result
    db.connection.close()
