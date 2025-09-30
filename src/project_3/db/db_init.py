import psycopg2

from project_3.config import DB_PARAMS


def create_database():
    conn = psycopg2.connect(
        dbname="postgres",
        user=DB_PARAMS["user"],
        password=DB_PARAMS["password"],
        host=DB_PARAMS["host"],
        port=DB_PARAMS["port"],
    )
    conn.autocommit = True
    cur = conn.cursor()

    # Проверяем, существует ли БД
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (DB_PARAMS["dbname"],))
    exists = cur.fetchone()
    if not exists:
        cur.execute(f"CREATE DATABASE {DB_PARAMS['dbname']};")
        print(f"База данных {DB_PARAMS['dbname']} создана")

    cur.close()
    conn.close()


def create_tables():
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()

    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS employers (
        employer_id INT PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    );
    """
    )

    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS vacancies (
        vacancy_id INT PRIMARY KEY,
        employer_id INT REFERENCES employers(employer_id),
        title VARCHAR(255) NOT NULL,
        salary_from INT,
        salary_to INT,
        url TEXT
    );
    """
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Таблицы employers и vacancies готовы")
