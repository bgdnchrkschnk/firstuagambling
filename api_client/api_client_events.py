from api_client.base_api_client import BaseAPIClient
import requests
from faker import Faker
fake = Faker()


class APIClientEvents(BaseAPIClient):

    BASE_API_V2_URL = "https://apiv2.first.ua"
    BASE_SOLITICS_URL = "https://api.solitics.com"

    def register(self) -> requests.Response:
        url = self.BASE_API_V2_URL + "/users/register"
        payload = {"type": "email",
                   "is_accept": True,
                   "email": self.email,
                   "password": self.password,
                   "phone": "",
                   "phone_code": "380",
                   "subscriptionAgreement": True
                   }
        response = self._post(url=url, json=payload)
        return response

    def get_profile_data(self, token: str) -> requests.Response:
        url = self.BASE_API_V2_URL + "/profile/info"
        self._headers_update({'Authorization': "Bearer " + token})
        response = self._get(url=url)
        return response

    def login_to_solitics(self, member_id: int) -> requests.Response:
        url = self.BASE_SOLITICS_URL + "/rest/integrations/login"
        payload = {
            "brand": "4eaa80b3-2609-47c0-9a4a-15e015bb9029",
            "memberId": member_id,
            "email": self.email,
            "transactionType": "LOGIN",
            "transactionAmount": 0,
            "customFields": "{\"page\":\"first.ua/ua\",\"fullUrl\":\"https://first.ua/ua\"}",
            "branch": "firstua"
        }
        response = self._post(url=url, json=payload)
        return response

    def get_dice_info(self) -> requests.Response:
        url = self.BASE_API_V2_URL + "/dices/info"
        response = self._get(url=url)
        return response

    def get_hotevents_list(self) -> requests.Response:
        url = self.BASE_API_V2_URL + "/hotevents/list"
        response = self._get(url=url)
        return response

    def get_loyalty_levels(self) -> requests.Response:
        url = self.BASE_API_V2_URL + "/loyalty/levels"
        response = self._get(url=url)
        return response

    def get_transactions(self) -> requests.Response:
        url = self.BASE_SOLITICS_URL + "/rest/integrations/transaction"
        response = self._post(url=url)
        return response

    def get_user_promotions_profile_all(self) -> requests.Response:
        url = self.BASE_API_V2_URL + "/user_promotions/list/profile-all"
        response = self._get(url=url)
        return response
