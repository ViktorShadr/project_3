import unittest
from unittest.mock import MagicMock, patch

from project_3.utils.helpers import process_companies, display_companies, display_vacancies


class TestUtils(unittest.TestCase):

    def setUp(self):
        # Мокаем API и DB
        self.api_mock = MagicMock()
        self.db_mock = MagicMock()
        self.list_of_companies = ["123", "456"]

    def test_process_companies_success(self):
        # Настраиваем возврат данных от API
        self.api_mock.get_employer.side_effect = [
            {"id": "123", "name": "Company A"},
            {"id": "456", "name": "Company B"}
        ]
        self.api_mock.get_vacancies.side_effect = [
            [{"id": "v1"}, {"id": "v2"}],
            [{"id": "v3"}]
        ]

        process_companies(self.api_mock, self.db_mock, self.list_of_companies)

        # Проверяем, что вставка работодателей и вакансий была вызвана
        self.assertEqual(self.db_mock.insert_employer.call_count, 2)
        self.assertEqual(self.db_mock.insert_vacancy.call_count, 3)

    def test_process_companies_api_fail(self):
        # Первый работодатель не вернёт данные
        self.api_mock.get_employer.side_effect = [None, {"id": "456", "name": "Company B"}]
        self.api_mock.get_vacancies.return_value = []

        process_companies(self.api_mock, self.db_mock, self.list_of_companies)

        # Проверяем, что первый работодатель не был добавлен
        self.assertEqual(self.db_mock.insert_employer.call_count, 1)
        self.assertEqual(self.db_mock.insert_vacancy.call_count, 0)

    @patch("builtins.print")
    def test_display_companies(self, mock_print):
        # Мокаем метод DB
        self.db_mock.get_companies_and_vacancies_count.return_value = [
            ("Company A", 2),
            ("Company B", 1)
        ]
        display_companies(self.db_mock)
        mock_print.assert_any_call("Company A — 2 вакансий")
        mock_print.assert_any_call("Company B — 1 вакансий")

    @patch("builtins.print")
    def test_display_vacancies(self, mock_print):
        # Мокаем метод DB
        self.db_mock.get_all_vacancies.return_value = [
            ("Company A", "Job 1", "Dev", 100000, "Moscow")
        ]
        display_vacancies(self.db_mock)
        mock_print.assert_called_with("Company A | Job 1 | Dev - 100000 | Moscow")


if __name__ == "__main__":
    unittest.main()
