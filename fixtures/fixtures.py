import pytest
from playwright.sync_api import Browser


@pytest.fixture(scope='module')
def s_page(browser: Browser):
    page = browser.new_page()
    yield page
    page.close()