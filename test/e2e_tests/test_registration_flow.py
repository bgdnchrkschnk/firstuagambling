import time

import faker as faker
from playwright.sync_api import Page, expect
from exceptions.exceptions import EmailNotParsedError
from allure import title, description, suite, severity, severity_level, attach, attachment_type
from faker import Faker
faker = Faker()


class TestRegistrationFlow:
    TEMPMAIL_URL: str = "https://tempail.com/ua/"
    BASE_URL: str = "https://first.ua/"
    CURRENT_EMAIL: str = None
    CURRENT_PW: str = None

    @title("User registration by email")
    @description("Verify user is able to register by email")
    @severity(severity_level.CRITICAL)
    @suite("e2e")
    def test_registration_by_email(self, s_page: Page):
        s_page.set_default_timeout(timeout=30000)
        s_page.goto(url=self.TEMPMAIL_URL)
        self.__class__.CURRENT_EMAIL = s_page.get_attribute(selector="input#eposta_adres", name="data-clipboard-text")
        if not self.__class__.CURRENT_EMAIL:
            raise EmailNotParsedError
        self.__class__.CURRENT_PW = faker.password(length=8, digits=True, lower_case=True, upper_case=True, special_chars=True)
        s_page.goto(url=self.BASE_URL, wait_until="domcontentloaded")
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
        time.sleep(3)
        avatar_section = s_page.wait_for_selector("div.wheel")
        attach(s_page.screenshot(), name="Screenshot", attachment_type=attachment_type.JPG)
        assert avatar_section.is_visible(), "User transferring to private cabinet has failed"

    @title("User sign out")
    @description("Verify user is able to sign out from")
    @severity(severity_level.CRITICAL)
    @suite("e2e")
    def test_sign_out(self, s_page: Page):
        avatar_section = s_page.locator("div.wheel")
        avatar_section.click()
        sign_out_btn = s_page.wait_for_selector(selector="img[src='/assets/logout-50f91c22.png']")
        sign_out_btn.click()
        sign_in_btn = s_page.wait_for_selector("a[href='/ua/auth/login']")
        attach(s_page.screenshot(), name="Screenshot", attachment_type=attachment_type.JPG)
        assert sign_in_btn.is_visible(), "Signing out is failed"

    @title("User sign in")
    @description("Verify user is able to sign in with existing account")
    @severity(severity_level.CRITICAL)
    @suite("e2e")
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
        attach(s_page.screenshot(), name="Screenshot", attachment_type=attachment_type.JPG)
        assert avatar_section.is_visible(), f"Signing in system has failed"

    @title("Email confirmation")
    @description("Verify user is able to receive and confirm account with confirmation email")
    @severity(severity_level.CRITICAL)
    @suite("e2e")
    def test_email_confirm(self, s_page: Page):
        s_page.goto(url=self.BASE_URL + "profile/verification/mail", wait_until="domcontentloaded")
        send_mail_btn = s_page.locator("button[data-v-6d5837e6]")
        send_mail_btn.wait_for()
        time.sleep(2)
        send_mail_btn.click()
        expect(s_page.get_by_text("Будь ласка, перевірте вашу пошту та пройдіть верифікацію")).to_be_visible()
        s_page.goto(url=self.TEMPMAIL_URL, wait_until="domcontentloaded")
        email_to_open = s_page.wait_for_selector(selector="li.mail>a", timeout=30000)
        attach(s_page.screenshot(), name="Screenshot", attachment_type=attachment_type.JPG)
        assert email_to_open.is_visible(), "Confirmation email has not received"
        email_to_open.click()
        time.sleep(2)
        confirm_email_btn = s_page.frame_locator("#iframe").locator("a.es-button.es-button-1698392951487")
        confirm_email_btn.click()
        attach(s_page.screenshot(), name="Screenshot", attachment_type=attachment_type.JPG)
        assert "first.ua" in s_page.url, f"Email confirmation has failed"
