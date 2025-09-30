from project_3.api.client import ApiClient
from project_3.config import LIST_OF_COMPANIES
from project_3.db.db_init import create_database, create_tables
from project_3.db.db_manager import DBManager


def main():
    # Создание базы и таблиц
    create_database()
    create_tables()

    # Проверка доступности API
    api = ApiClient(list_of_companies=LIST_OF_COMPANIES)
    if not api.is_available():
        print("Сервис hh.ru недоступен. Попробуйте позже.")
        return

    # Получение данных и запись в БД
    db = DBManager()
    for employer_id in LIST_OF_COMPANIES:
        employer = api.get_employer(employer_id)
        if employer:
            db.insert_employer(employer)
            vacancies = api.get_vacancies(employer_id)
            for vacancy in vacancies:
                db.insert_vacancy(vacancy, employer_id)

    # Интерфейс для пользователя
    while True:
        print("\n Выберите действие:")
        print("1 - Список всех компаний и количество вакансий")
        print("2 - Список всех вакансий")
        print("3 - Средняя зарплата по вакансиям")
        print("4 - Вакансии с зарплатой выше средней")
        print("5 - Поиск вакансий по ключевому слову")
        print("0 - Выход")

        choice = input("Ваш выбор: ")

        if choice == "1":
            for row in db.get_companies_and_vacancies_count():
                print(f"{row[0]} — {row[1]} вакансий")

        elif choice == "2":
            for row in db.get_all_vacancies():
                print(f"{row[0]} | {row[1]} | {row[2]} - {row[3]} | {row[4]}")

        elif choice == "3":
            avg_salary = db.get_avg_salary()
            print(
                f"Средняя зарплата: {avg_salary:.2f}"
                if avg_salary
                else "Нет данных по зарплатам"
            )

        elif choice == "4":
            for row in db.get_vacancies_with_higher_salary():
                print(f"{row[0]} | {row[1]} | {row[2]} - {row[3]} | {row[4]}")

        elif choice == "5":
            keyword = input("Введите ключевое слово: ")
            for row in db.get_vacancies_with_keyword(keyword):
                print(f"{row[0]} | {row[1]} | {row[2]} - {row[3]} | {row[4]}")

        elif choice == "0":
            print("Выход из программы")
            break

        else:
            print("Неверный ввод!")

    db.close()


if __name__ == "__main__":
    main()
