import pytest
from requests import Response

from test.integration_tests.steps import APIClientSteps


class TestsIntegration:

    TOKEN: str = None
    MEMBER_ID: int = None

    @pytest.mark.integration
    def test_registration(self, client: APIClientSteps):
        response = client.register()
        assert response.ok, f"Status code is not as expected.\nExpected: 200\nActual: {response.status_code}"
        assert "token" in response.json()['user'], f"Failed to register. token not asserted in {response.json()}"
        self.__class__.TOKEN = response.json()['user']['token']

    def test_get_profile_info(self, client: APIClientSteps):
        response = client.get_profile_data(token=self.__class__.TOKEN)
        assert response.ok, f"Status code is not as expected.\nExpected: 200\nActual: {response.status_code}"
        assert "user" in response.json(), f"Failed to get profile data. Json schema is wrong in {response.json()}"
        self.__class__.MEMBER_ID = response.json()['user']['id']

    @pytest.mark.skip(reason="Needs to investigate with devs")
    def test_login_solitics(self, client: APIClientSteps):
        response = client.login_to_solitics(token=self.__class__.TOKEN, member_id=self.__class__.MEMBER_ID)
        assert response.ok, response.json()

    def test_get_dice_info(self, client: APIClientSteps):
        response = client.get_dice_info()
        assert response.ok, f"Status code is not as expected.\nExpected: 200\nActual: {response.status_code}"
        assert "dices" in response.json()

    def test_hotevents_list(self, client: APIClientSteps):
        response = client.get_hotevents_list()
        assert response.ok, f"Status code is not as expected.\nExpected: 200\nActual: {response.status_code}"
        assert "events" in response.json()

    @pytest.mark.skip(reason="Needs to investigate with devs")
    def test_transactions(self, client: APIClientSteps):
        response = client.get_loyalty_levels()
        assert response.ok, f"Status code is not as expected.\nExpected: 200\nActual: {response.status_code}"
        assert "levels" in response.json()

    def test_user_promotions_profile_all(self, client: APIClientSteps):
        response = client.get_user_promotions_profile_all()
        assert response.ok, f"Status code is not as expected.\nExpected: 200\nActual: {response.status_code}"
        assert "available" in response.json()