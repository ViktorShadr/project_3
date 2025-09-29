from typing import Any, Optional, cast

import requests

from config import BASE_URL_HH_RU, LIST_OF_COMPANIES
from project_3.api.base import BaseApiClient


class ApiClient(BaseApiClient):
    """Класс для работы с API и проверки соединения."""

    def __init__(self, list_of_companies: list = LIST_OF_COMPANIES, base_url: str = BASE_URL_HH_RU) -> None:
        self.__base_url = base_url
        self.list_of_companies = list_of_companies

    def __check_connection(self) -> bool:
        """Приватный метод проверки соединения с API"""
        try:
            response = requests.get(f"{self.__base_url}/vacancies", params={"per_page": 1}, timeout=5)
            if response.status_code == 200:
                print("Соединение установлено")
                return True
            print(f"Сбой при подключении: {response.status_code}")
            return False
        except requests.RequestException as e:
            print(f"Сбой при подключении: {e}")
            return False

    def _check_connection(self) -> bool:
        """Вспомогательный метод для проверки соединения с сервисом"""
        return self.__check_connection()

    def is_available(self) -> bool:
        """Публичный метод для проверки доступности сервиса"""
        return self.__check_connection()

    def get(self, endpoint: str = "", params: Optional[dict[str, Any]] = None) -> Optional[dict[str, Any]]:
        """Выполняет GET-запрос к API"""

        if endpoint and not endpoint.startswith("/"):
            endpoint = "/" + endpoint

        url = f"{self.__base_url}{endpoint}"
        print(url)
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Ошибка GET-запроса: {e}")
            return None

    def get_companies(self, list_of_companies) -> list | None:
        """Получение списка компаний"""

        if not self.is_available():  # проверка соединения
            print("Ошибка соединения")
            return None

        all_info_companies = []
        for company in list_of_companies:
            data = self.get(
                endpoint="vacancies",
                params={"employer_id": company}
            )
            if not data:
                return None

            all_info_companies.append(data)
        return all_info_companies

