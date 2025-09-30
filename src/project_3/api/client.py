from abc import abstractmethod
from typing import Any, Optional
import requests

from config import BASE_URL_HH_RU, LIST_OF_COMPANIES
from project_3.api.base import BaseApiClient


class ApiClient(BaseApiClient):
    """Класс для работы с API hh.ru и проверки соединения."""

    def __init__(self, list_of_companies: list[int] = LIST_OF_COMPANIES, base_url: str = BASE_URL_HH_RU) -> None:
        self.__base_url = base_url
        self.list_of_companies = list_of_companies

    @abstractmethod
    def __check_connection(self) -> bool:
        """Приватный метод проверки соединения с API"""
        try:
            response = requests.get(f"{self.__base_url}/vacancies", params={"per_page": 1}, timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    @abstractmethod
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
            return response.json()
        except requests.RequestException as e:
            print(f"Ошибка GET-запроса: {e}")
            return None

    def get_employer(self, employer_id: int) -> Optional[dict]:
        """Получить данные о конкретном работодателе"""
        return self.get(f"/employers/{employer_id}")

    def get_vacancies(self, employer_id: int) -> list[dict]:
        """Получить список вакансий работодателя"""
        data = self.get("/vacancies", params={"employer_id": employer_id})
        return data.get("items", []) if data else []
