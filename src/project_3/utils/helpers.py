from project_3.api.client import ApiClient
from project_3.db.db_init import create_database, create_tables
from project_3.db.db_manager import DBManager


def process_companies(api, db, list_of_companies):
    for employer_id in list_of_companies:
        print(f"\nПолучаем данные о работодателе {employer_id}...")
        employer = api.get_employer(employer_id)
        if not employer:
            print(f"❌ Не удалось получить данные о работодателе {employer_id}")
            continue

        db.insert_employer(employer)
        vacancies = api.get_vacancies(employer_id)
        print(f"Получаем вакансии для {employer['name']} ({len(vacancies)} шт.)...")

        for vacancy in vacancies:
            db.insert_vacancy(vacancy, employer_id)

        print(f"✅ Вакансии для {employer['name']} обработаны")


def display_companies(db):
    for row in db.get_companies_and_vacancies_count():
        print(f"{row[0]} — {row[1]} вакансий")


def display_vacancies(db, vacancies=None):
    if vacancies is None:
        vacancies = db.get_all_vacancies()
    for row in vacancies:
        print(f"{row[0]} | {row[1]} | {row[2]} - {row[3]} | {row[4]}")


def main_menu(db):
    while True:
        print("\nВыберите действие:")
        print("1 - Список всех компаний и количество вакансий")
        print("2 - Список всех вакансий")
        print("3 - Средняя зарплата по вакансиям")
        print("4 - Вакансии с зарплатой выше средней")
        print("5 - Поиск вакансий по ключевому слову")
        print("0 - Выход")

        choice = input("Ваш выбор: ")

        if choice == "1":
            display_companies(db)

        elif choice == "2":
            display_vacancies(db)

        elif choice == "3":
            avg_salary = db.get_avg_salary()
            print(
                f"Средняя зарплата: {avg_salary:.2f}"
                if avg_salary
                else "Нет данных по зарплатам"
            )

        elif choice == "4":
            display_vacancies(db, db.get_vacancies_with_higher_salary())

        elif choice == "5":
            keyword = input("Введите ключевое слово: ")
            display_vacancies(db, db.get_vacancies_with_keyword(keyword))

        elif choice == "0":
            print("Выход из программы")
            break

        else:
            print("Неверный ввод!")


def main():
    create_database()
    create_tables()

    api = ApiClient(list_of_companies=LIST_OF_COMPANIES)
    if not api.is_available():
        print("Сервис hh.ru недоступен. Попробуйте позже.")
        return

    db = DBManager()
    process_companies(api, db)
    main_menu(db)
    db.close()


if __name__ == "__main__":
    main()
