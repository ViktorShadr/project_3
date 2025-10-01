from unittest.mock import MagicMock, patch

import pytest

from project_3.db.db_manager import DBManager


# Фикстура для мокнутого подключения
@pytest.fixture
def mock_db():
    with patch("project_3.db.db_manager.psycopg2.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        yield mock_conn, mock_cursor


def test_insert_employer(mock_db):
    mock_conn, mock_cursor = mock_db
    db = DBManager()
    employer = {"id": 1, "name": "Test Company"}
    db.insert_employer(employer)

    mock_cursor.execute.assert_called_with(
        """
            INSERT INTO employers (employer_id, name)
            VALUES (%s, %s)
            ON CONFLICT (employer_id) DO NOTHING;
            """,
        (employer["id"], employer["name"]),
    )
    mock_conn.commit.assert_called_once()


def test_insert_vacancy(mock_db):
    mock_conn, mock_cursor = mock_db
    db = DBManager()
    vacancy = {
        "id": 10,
        "name": "Python Developer",
        "salary": {"from": 100000, "to": 150000},
        "alternate_url": "http://example.com",
    }
    db.insert_vacancy(vacancy, employer_id=1)

    mock_cursor.execute.assert_called_with(
        """
            INSERT INTO vacancies (vacancy_id, employer_id, title, salary_from, salary_to, url)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (vacancy_id) DO NOTHING;
            """,
        (
            vacancy["id"],
            1,
            vacancy["name"],
            100000,
            150000,
            vacancy["alternate_url"],
        ),
    )
    mock_conn.commit.assert_called_once()


def test_get_companies_and_vacancies_count(mock_db):
    _, mock_cursor = mock_db
    mock_cursor.fetchall.return_value = [("Test Company", 5)]
    db = DBManager()
    result = db.get_companies_and_vacancies_count()
    mock_cursor.execute.assert_called_once()
    assert result == [("Test Company", 5)]


def test_get_all_vacancies(mock_db):
    _, mock_cursor = mock_db
    mock_cursor.fetchall.return_value = [
        ("Test Company", "Python Dev", 100000, 150000, "url")
    ]
    db = DBManager()
    result = db.get_all_vacancies()
    mock_cursor.execute.assert_called_once()
    assert result == [("Test Company", "Python Dev", 100000, 150000, "url")]


def test_get_avg_salary(mock_db):
    _, mock_cursor = mock_db
    mock_cursor.fetchone.return_value = [125000]
    db = DBManager()
    result = db.get_avg_salary()
    mock_cursor.execute.assert_called_once()
    assert result == 125000


def test_get_vacancies_with_higher_salary(mock_db):
    _, mock_cursor = mock_db
    mock_cursor.fetchall.return_value = [
        ("Test Company", "Senior Dev", 200000, 250000, "url")
    ]
    db = DBManager()
    result = db.get_vacancies_with_higher_salary()
    mock_cursor.execute.assert_called_once()
    assert result == [("Test Company", "Senior Dev", 200000, 250000, "url")]


def test_get_vacancies_with_keyword(mock_db):
    _, mock_cursor = mock_db
    mock_cursor.fetchall.return_value = [
        ("Test Company", "Python Dev", 100000, 150000, "url")
    ]
    db = DBManager()
    result = db.get_vacancies_with_keyword("Python")
    mock_cursor.execute.assert_called_once_with(
        """
        SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
        FROM vacancies v
        JOIN employers e ON v.employer_id = e.employer_id
        WHERE v.title ILIKE %s;
        """,
        ("%Python%",),
    )
    assert result == [("Test Company", "Python Dev", 100000, 150000, "url")]
