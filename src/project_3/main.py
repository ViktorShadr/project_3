from config import LIST_OF_COMPANIES
from project_3.api.client import ApiClient

if __name__ == "__main__":
    client = ApiClient()
    companies = client.get_companies(LIST_OF_COMPANIES)

    print(companies)