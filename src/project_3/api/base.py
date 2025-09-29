from abc import ABC, abstractmethod


class BaseApiClient(ABC):

    @abstractmethod
    def _check_connection(self) -> bool:
        """Вспомогательный абстрактный метод для проверки соединения с сервисом"""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Абстрактный публичный метод для проверки доступности сервиса"""
        pass
