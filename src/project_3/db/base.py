from abc import ABC, abstractmethod


class AbstractDBManager(ABC):
    """Абстрактный класс для DBManager"""

    @abstractmethod
    def insert_employer(self, employer: dict):
        """Абстрактный метод для добавления работодателей"""
        pass

    @abstractmethod
    def insert_vacancy(self, vacancy: dict, employer_id: int):
        """Абстрактный метод для добавления вакансий"""
        pass
