from project_3.api.client import ApiClient
from project_3.config import LIST_OF_COMPANIES
from project_3.db.db_init import create_database, create_tables
from project_3.db.db_manager import DBManager
from project_3.utils.helpers import main_menu, process_companies


def main():
    create_database()
    create_tables()

    api = ApiClient(list_of_companies=LIST_OF_COMPANIES)
    if not api.is_available():
        print("Сервис hh.ru недоступен. Попробуйте позже.")
        return

    db = DBManager()
    process_companies(api, db, LIST_OF_COMPANIES)
    main_menu(db)
    db.close()


if __name__ == "__main__":
    main()
