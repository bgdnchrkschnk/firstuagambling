import requests



class APIClientSteps:

    def __init__(self):
        from faker import Faker
        faker = Faker()
        self._client = requests.Session()
        self.email: str = faker.free_email()
        self.password: str = faker.password(length=6, upper_case=True, special_chars=True)

    @property
    def client(self):
        return self._client

    def register(self) -> requests.Response:
        url = "https://apiv2.first.ua/users/register"
        self.client.headers.update({"Content-Type": "application/json; charset=utf-8"})
        payload = {"type": "email",
                   "is_accept": True,
                   "email": self.email,
                   "password": self.password,
                   "phone": "",
                   "phone_code": "380",
                   "subscriptionAgreement": True
                   }
        response = self.client.post(url=url, json=payload)
        return response

    def get_profile_data(self, token: str) -> requests.Response:
        url = "https://apiv2.first.ua/profile/info"
        self.client.headers.update({'Authorization': "Bearer " + token})
        response = self.client.get(url=url)
        return response

    def login_to_solitics(self, member_id: int) -> requests.Response:
        url = "https://api.solitics.com/rest/integrations/login"
        payload = {
            "brand": "4eaa80b3-2609-47c0-9a4a-15e015bb9029",
            "memberId": member_id,
            "email": self.email,
            "transactionType": "LOGIN",
            "transactionAmount": 0,
            "customFields": "{\"page\":\"first.ua/ua\",\"fullUrl\":\"https://first.ua/ua\"}",
            "branch": "firstua"
        }
        response = self.client.post(url=url, json=payload)
        return response

    def get_dice_info(self) -> requests.Response:
        url = "https://apiv2.first.ua/dices/info"
        response = self.client.get(url=url)
        return response

    def get_hotevents_list(self) -> requests.Response:
        url = "https://apiv2.first.ua/hotevents/list"
        response = self.client.get(url=url)
        return response

    def get_loyalty_levels(self) -> requests.Response:
        url = "https://apiv2.first.ua/loyalty/levels"
        response = self.client.get(url=url)
        return response

    def get_transactions(self) -> requests.Response:
        url = "https://api.solitics.com/rest/integrations/transaction"
        response = self.client.post(url=url)
        return response

    def get_user_promotions_profile_all(self) -> requests.Response:
        url = "https://apiv2.first.ua/user_promotions/list/profile-all"
        response = self.client.get(url=url)
        return response
