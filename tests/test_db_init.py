from unittest.mock import patch, MagicMock

from project_3.config import DB_PARAMS
from project_3.db.db_init import create_database, create_tables


# Тест create_database
@patch("project_3.db.db_init.psycopg2.connect")
def test_create_database_already_exists(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    # Симулируем, что база уже существует
    mock_cursor.fetchone.return_value = (1,)

    create_database()

    mock_cursor.execute.assert_any_call(
        "SELECT 1 FROM pg_database WHERE datname = %s;", (DB_PARAMS["dbname"],)
    )
    # CREATE DATABASE не должен вызываться
    mock_cursor.execute.assert_called_with(
        "SELECT 1 FROM pg_database WHERE datname = %s;", (DB_PARAMS["dbname"],)
    )
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch("project_3.db.db_init.psycopg2.connect")
def test_create_database_new(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    # Симулируем, что база не существует
    mock_cursor.fetchone.return_value = None

    create_database()

    # Проверяем, что CREATE DATABASE вызван
    mock_cursor.execute.assert_any_call(f"CREATE DATABASE {DB_PARAMS['dbname']};")
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


# Тест create_tables
@patch("project_3.db.db_init.psycopg2.connect")
def test_create_tables(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    create_tables()

    # Проверяем, что CREATE TABLE вызван для обеих таблиц
    assert any("CREATE TABLE IF NOT EXISTS employers" in call[0][0] for call in mock_cursor.execute.call_args_list)
    assert any("CREATE TABLE IF NOT EXISTS vacancies" in call[0][0] for call in mock_cursor.execute.call_args_list)
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()
