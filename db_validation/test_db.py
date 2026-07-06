import pytest
import sqlite3
import os


@pytest.fixture()
def db_connection():
    db_path = os.path.join(os.path.dirname(__file__), "test_etl.db")
    conn = sqlite3.connect(db_path)
    yield conn
    conn.close()


def test_source_row_count(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM source_employees")
    result = cursor.fetchone()[0]
    assert result == 10, \
        f"Expected 10 source rows but got {result}"


def test_destination_row_count(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM dest_employees")
    result = cursor.fetchone()[0]
    assert result == 8, \
        f"Expected 8 destination rows but got {result}"


def test_only_activate_employees_loaded(db_connection):
    cursor = db_connection.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM source_employees WHERE status ='active'")
    active_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM dest_employees")
    dest_count = cursor.fetchone()[0]
    assert active_count == dest_count, \
        f"Expected {active_count} active employees in dest but got {dest_count}"


def test_salary_accuracy(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT salary FROM dest_employees WHERE id = 1")
    result = cursor.fetchone()[0]
    assert result == 95000, \
        f"Expected salary is 95000 but got {result}"


def test_bonus_calculation(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT annual_bonus FROM dest_employees WHERE id = 1")
    result = cursor.fetchone()[0]
    assert result == 9500.0, \
        f"Expected bonus 9500.0 but got {result}"
