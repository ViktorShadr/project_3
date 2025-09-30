import psycopg2

from project_3.config import DB_PARAMS


class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(**DB_PARAMS)
        self.cur = self.conn.cursor()

    def insert_employer(self, employer: dict):
        """Добавление работодателей"""
        self.cur.execute(
            """
            INSERT INTO employers (employer_id, name)
            VALUES (%s, %s)
            ON CONFLICT (employer_id) DO NOTHING;
            """,
            (employer["id"], employer["name"]),
        )
        self.conn.commit()

    def insert_vacancy(self, vacancy: dict, employer_id: int):
        """Добавление вакансий"""
        salary = vacancy.get("salary") or {}
        salary_from = salary.get("from")
        salary_to = salary.get("to")

        self.cur.execute(
            """
            INSERT INTO vacancies (vacancy_id, employer_id, title, salary_from, salary_to, url)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (vacancy_id) DO NOTHING;
            """,
            (
                vacancy["id"],
                employer_id,
                vacancy["name"],
                salary_from,
                salary_to,
                vacancy["alternate_url"],
            ),
        )
        self.conn.commit()

    def get_companies_and_vacancies_count(self):
        """Получить список всех компаний и количество вакансий у каждой"""
        self.cur.execute(
            """
        SELECT e.name, COUNT(v.vacancy_id)
        FROM employers e
        LEFT JOIN vacancies v ON e.employer_id = v.employer_id
        GROUP BY e.name;
        """
        )
        return self.cur.fetchall()

    def get_all_vacancies(self):
        """Получить список всех вакансий"""
        self.cur.execute(
            """
        SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
        FROM vacancies v
        JOIN employers e ON v.employer_id = e.employer_id;
        """
        )
        return self.cur.fetchall()

    def get_avg_salary(self):
        """Средняя зарплата по вакансиям"""
        self.cur.execute(
            """SELECT AVG((salary_from + salary_to)/2.0) FROM vacancies WHERE salary_from IS NOT NULL AND
            salary_to IS NOT NULL;"""
        )
        return self.cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        """Вакансии с зарплатой выше средней"""
        self.cur.execute(
            """
        SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
        FROM vacancies v
        JOIN employers e ON v.employer_id = e.employer_id
        WHERE (v.salary_from + v.salary_to)/2.0 > (
            SELECT AVG((salary_from + salary_to)/2.0) FROM vacancies WHERE salary_from IS NOT NULL AND salary_to IS
            NOT NULL) ORDER BY (v.salary_from + v.salary_to)/2.0 DESC;
        """
        )
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str):
        """Вакансии по ключевому слову"""
        self.cur.execute(
            """
        SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
        FROM vacancies v
        JOIN employers e ON v.employer_id = e.employer_id
        WHERE v.title ILIKE %s;
        """,
            (f"%{keyword}%",),
        )
        return self.cur.fetchall()

    def close(self):
        self.cur.close()
        self.conn.close()
