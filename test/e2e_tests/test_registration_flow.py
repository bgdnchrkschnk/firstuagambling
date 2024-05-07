import time

from playwright.sync_api import Page, expect
from faker import Faker
from exceptions.exceptions import EmailNotParsedError

faker = Faker()


class TestRegistrationFlow:
    CURRENT_EMAIL: str = None
    CURRENT_PW: str = None

    def test_registration_by_email(self, s_page: Page):
        s_page.set_default_timeout(timeout=30000)
        s_page.goto(url="https://tempail.com/ua/")
        self.__class__.CURRENT_EMAIL = s_page.get_attribute(selector="input#eposta_adres", name="data-clipboard-text")
        if not self.__class__.CURRENT_EMAIL:
            raise EmailNotParsedError
        self.__class__.CURRENT_PW = faker.password(length=8, digits=True, lower_case=True, upper_case=True, special_chars=True)

        s_page.goto(url="https://first.ua/", wait_until="domcontentloaded")
        register_button = s_page.locator("a[href='/ua/auth/signup']")
        register_button.click()
        time.sleep(2)
        s_page.get_by_text(text="Е-пошта").click()
        email_field = s_page.locator("input[type=email]")
        pw_field = s_page.locator("input[type=password]")
        email_field.type(text=self.__class__.CURRENT_EMAIL, delay=100)
        pw_field.type(text=self.__class__.CURRENT_PW, delay=100)
        s_page.locator("button[data-v-e18269df][data-v-225103f9]").click()
        decline_bonus = s_page.get_by_text(text="Не хочу бонус")
        decline_bonus.wait_for(timeout=30000)
        decline_bonus.click()
        time.sleep(3)
        decline_payment = s_page.locator("a use")
        decline_payment.wait_for(timeout=10000)
        decline_payment.click()
        breakpoint()
        time.sleep(3)
        avatar_section = s_page.wait_for_selector("div.wheel")
        assert avatar_section.is_visible(), "User transferring to private cabinet has failed"

    def test_sign_out(self, s_page: Page):
        avatar_section = s_page.locator("div.wheel")
        avatar_section.click()
        sign_out_btn = s_page.wait_for_selector(selector="img[src='/assets/logout-50f91c22.png']")
        sign_out_btn.click()
        sign_in_btn = s_page.wait_for_selector("a[href='/ua/auth/login']")
        assert sign_in_btn.is_visible(), "Signing out is failed"

    def test_sign_in(self, s_page: Page):
        sign_in_btn = s_page.wait_for_selector("a[href='/ua/auth/login']")
        sign_in_btn.click()

        time.sleep(3)
        s_page.get_by_text(text="Е-пошта").click()
        email_field = s_page.locator("input[type=email]")
        pw_field = s_page.locator("input[type=password]")
        email_field.type(text=self.__class__.CURRENT_EMAIL, delay=100)
        pw_field.type(text=self.__class__.CURRENT_PW)
        log_in_btn = s_page.locator("button[data-v-5e7ea9e5]")
        log_in_btn.click()
        avatar_section = s_page.wait_for_selector("div.wheel")
        assert avatar_section.is_visible(), f"Signing in system has failed"

    def test_email_confirm(self, s_page: Page):
        s_page.goto(url="https://first.ua/ua/profile/verification/mail", wait_until="domcontentloaded")
        send_mail_btn = s_page.locator("button[data-v-6d5837e6]")
        send_mail_btn.wait_for()
        time.sleep(2)
        send_mail_btn.click()
        expect(s_page.get_by_text("Будь ласка, перевірте вашу пошту та пройдіть верифікацію")).to_be_visible()
        s_page.goto(url="https://tempail.com/ua/", wait_until="domcontentloaded")
        email_to_open = s_page.wait_for_selector(selector="li.mail>a", timeout=30000)
        assert email_to_open.is_visible(), "Confirmation email has not received"
        email_to_open.click()
        time.sleep(2)
        confirm_email_btn = s_page.frame_locator("#iframe").locator("a.es-button.es-button-1698392951487")
        confirm_email_btn.click()
        assert "first.ua" in s_page.url, f"Email confirmation has failed"
