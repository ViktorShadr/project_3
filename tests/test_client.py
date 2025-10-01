from unittest.mock import Mock, patch

import pytest
from requests.exceptions import RequestException

from project_3.api.client import ApiClient

BASE_URL = "https://api.hh.ru"
COMPANY_ID = 123


@pytest.fixture
def api_client():
    return ApiClient(list_of_companies=[COMPANY_ID], base_url=BASE_URL)


def test_check_connection_success(api_client):
    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        assert api_client.is_available() is True
        mock_get.assert_called_once_with(
            f"{BASE_URL}/vacancies", params={"per_page": 1}, timeout=5
        )


def test_check_connection_failure(api_client):
    with patch("requests.get", side_effect=RequestException("Connection error")):
        assert api_client.is_available() is False


def test_get_success(api_client):
    data = {"key": "value"}
    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = api_client.get("/test_endpoint")
        assert result == data
        mock_get.assert_called_once_with(
            f"{BASE_URL}/test_endpoint", params=None, timeout=10
        )


def test_get_failure(api_client):
    with patch("requests.get", side_effect=RequestException("Request failed")):
        result = api_client.get("/test_endpoint")
        assert result is None


def test_get_employer(api_client):
    with patch.object(
        ApiClient, "get", return_value={"id": COMPANY_ID, "name": "Test Co"}
    ):
        result = api_client.get_employer(COMPANY_ID)
        assert result["id"] == COMPANY_ID
        assert result["name"] == "Test Co"


def test_get_vacancies(api_client):
    vacancies_data = {"items": [{"id": 1, "name": "Dev"}]}
    with patch.object(ApiClient, "get", return_value=vacancies_data):
        result = api_client.get_vacancies(COMPANY_ID)
        assert isinstance(result, list)
        assert result[0]["name"] == "Dev"


def test_get_vacancies_empty(api_client):
    with patch.object(ApiClient, "get", return_value=None):
        result = api_client.get_vacancies(COMPANY_ID)
        assert result == []
