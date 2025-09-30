import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


def create_database():
    """Создание БД и таблиц (если их ещё нет)"""
    conn = psycopg2.connect(
        dbname="postgres", user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    conn.autocommit = True
    cur = conn.cursor()

    # Создаем новую БД, если её нет
    cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}';")
    exists = cur.fetchone()
    if not exists:
        cur.execute(f"CREATE DATABASE {DB_NAME};")
        print(f"База данных {DB_NAME} создана")

    cur.close()
    conn.close()

def create_tables():
    # Создаем таблицы
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS employers (
        employer_id INT PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS vacancies (
        vacancy_id INT PRIMARY KEY,
        employer_id INT REFERENCES employers(employer_id),
        title VARCHAR(255) NOT NULL,
        salary_from INT,
        salary_to INT,
        url TEXT
    );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Таблицы employers и vacancies готовы")
