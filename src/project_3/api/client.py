from typing import Any, Optional, cast

import requests

from config import BASE_URL_HH_RU
from project_3.api.base import BaseApiClient


class ApiClient(BaseApiClient):
    """Класс для работы с API и проверки соединения."""

    def __init__(self, search_query: str, per_page: int, base_url: str = BASE_URL_HH_RU) -> None:
        self.__base_url = base_url
        self.__search_query = search_query
        self.__per_page = per_page

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
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return cast(dict[str, Any], response.json())
        except requests.RequestException as e:
            print(f"Ошибка GET-запроса: {e}")
            return None

    def get_vacancy(self, pages: int = 0, area: int = 113) -> list | None:
        """Получение списка вакансий по ключевому слову"""

        if not self.is_available():  # проверка соединения
            print("Ошибка соединения")
            return None

        data = self.get(
            endpoint="vacancies",
            params={"text": self.__search_query, "area": area, "per_page": self.__per_page, "page": pages},
        )

        if not data:
            return None

        results = []
        for item in data.get("items", []):
            vacancy = Vacancy.from_dict(item)
            results.append(vacancy)

        return results
