import requests
from faker import Faker
fake = Faker()


class BaseAPIClient:

    def __init__(self):
        self._client = requests.Session()
        self.email: str = fake.free_email()
        self.password: str = fake.password(length=6, upper_case=True, special_chars=True)
        self._headers_update(headers_dict=
                             {"Content-Type": "application/json; charset=utf-8"})

    def _headers_update(self, headers_dict: dict):
        self._client.headers.update(headers_dict)

    def _get(self, url: str):
        return self._client.get(url=url)

    def _post(self, url: str, json: dict):
        return self._client.post(url=url, json=json)