import time

from playwright.sync_api import Page
from faker import Faker

faker = Faker()


class TestRegistrationFlow:

    CURRENT_EMAIL: str = None
    CURRENT_PW: str = faker.password(length=8, digits=True, lower_case=True, upper_case=True, special_chars=True)

    def test_registration_by_email(self, s_page: Page):
        s_page.set_default_timeout(timeout=10000)
        s_page.goto(url="https://tempail.com/ua/")
        self.CURRENT_EMAIL = s_page.get_attribute(selector="input#eposta_adres", name="data-clipboard-text")
        assert self.CURRENT_EMAIL

        s_page.goto(url="https://first.ua/")
        register_button = s_page.locator("a[href='/ua/auth/signup']")
        register_button.click()
        time.sleep(2)
        s_page.get_by_text(text="Е-пошта").click()
        breakpoint()
        email_field = s_page.locator("input[type=email]")
        pw_field = s_page.locator("input[type=password]")
        email_field.type(text=self.CURRENT_EMAIL, delay=100)
        pw_field.type(text=self.CURRENT_PW, delay=100)
        print(self.CURRENT_EMAIL)
        print(self.CURRENT_PW)
        breakpoint()