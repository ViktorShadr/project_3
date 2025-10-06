from unittest.mock import MagicMock, patch

from project_3.utils.helpers import (display_companies, display_vacancies,
                                     main, main_menu, process_companies)


def test_process_companies_calls_api_and_db():
    api = MagicMock()
    db = MagicMock()
    list_of_companies = [1]

    api.get_employer.return_value = {"id": 1, "name": "Test Company"}
    api.get_vacancies.return_value = [{"id": 101, "title": "Python Dev"}]

    process_companies(api, db, list_of_companies)

    api.get_employer.assert_called_once_with(1)
    api.get_vacancies.assert_called_once_with(1)
    db.insert_employer.assert_called_once_with({"id": 1, "name": "Test Company"})
    db.insert_vacancy.assert_called_once_with({"id": 101, "title": "Python Dev"}, 1)


def test_process_companies_skips_if_no_employer():
    api = MagicMock()
    db = MagicMock()
    list_of_companies = [1]

    api.get_employer.return_value = None

    process_companies(api, db, list_of_companies)

    api.get_vacancies.assert_not_called()
    db.insert_employer.assert_not_called()
    db.insert_vacancy.assert_not_called()


def test_display_companies_prints(capsys):
    db = MagicMock()
    db.get_companies_and_vacancies_count.return_value = [
        ("Company A", 5),
        ("Company B", 2),
    ]

    display_companies(db)

    captured = capsys.readouterr()
    assert "Company A — 5 вакансий" in captured.out
    assert "Company B — 2 вакансий" in captured.out


def test_display_vacancies_prints_default(capsys):
    db = MagicMock()
    db.get_all_vacancies.return_value = [
        ("Company A", "Python Dev", 100000, 150000, "Москва"),
    ]

    display_vacancies(db)

    captured = capsys.readouterr()
    assert "Company A | Python Dev | 100000 - 150000 | Москва" in captured.out


def test_main_api_unavailable(capsys):
    with patch("project_3.utils.helpers.create_database"), patch(
        "project_3.utils.helpers.create_tables"
    ), patch("project_3.utils.helpers.ApiClient") as mock_api, patch(
        "project_3.utils.helpers.DBManager"
    ) as _, patch(
        "builtins.input", return_value="0"
    ):
        mock_api.return_value.is_available.return_value = False

        main()

    captured = capsys.readouterr()
    assert "Сервис hh.ru недоступен" in captured.out


def test_main_api_available():
    with patch("project_3.utils.helpers.create_database"), patch(
        "project_3.utils.helpers.create_tables"
    ), patch("project_3.utils.helpers.ApiClient") as mock_api, patch(
        "project_3.utils.helpers.DBManager"
    ) as mock_db, patch(
        "project_3.utils.helpers.process_companies"
    ) as mock_process, patch(
        "project_3.utils.helpers.main_menu"
    ) as mock_menu:
        mock_api.return_value.is_available.return_value = True
        db_instance = mock_db.return_value

        main()

        mock_process.assert_called_once()
        mock_menu.assert_called_once_with(db_instance)


def test_main_menu_option_1(capsys):
    db = MagicMock()
    with patch("builtins.input", side_effect=["1", "0"]), patch(
        "project_3.utils.helpers.display_companies"
    ) as mock_display:
        main_menu(db)
        mock_display.assert_called_once_with(db)

    captured = capsys.readouterr()
    assert "Выход из программы" in captured.out


def test_main_menu_option_2():
    db = MagicMock()
    with patch("builtins.input", side_effect=["2", "0"]), patch(
        "project_3.utils.helpers.display_vacancies"
    ) as mock_display:
        main_menu(db)
        mock_display.assert_any_call(db)


def test_main_menu_option_3(capsys):
    db = MagicMock()
    db.get_avg_salary.return_value = 50000
    with patch("builtins.input", side_effect=["3", "0"]):
        main_menu(db)

    captured = capsys.readouterr()
    assert "Средняя зарплата: 50000.00" in captured.out


def test_main_menu_option_4():
    db = MagicMock()
    with patch("builtins.input", side_effect=["4", "0"]), patch(
        "project_3.utils.helpers.display_vacancies"
    ) as mock_display:
        main_menu(db)
        mock_display.assert_called_once_with(db, db.get_vacancies_with_higher_salary())


def test_main_menu_option_5():
    db = MagicMock()
    with patch("builtins.input", side_effect=["5", "Python", "0"]), patch(
        "project_3.utils.helpers.display_vacancies"
    ) as mock_display:
        main_menu(db)
        mock_display.assert_called_once_with(
            db, db.get_vacancies_with_keyword("Python")
        )


def test_main_menu_invalid_choice(capsys):
    db = MagicMock()
    with patch("builtins.input", side_effect=["999", "0"]):
        main_menu(db)

    captured = capsys.readouterr()
    assert "Неверный ввод!" in captured.out
