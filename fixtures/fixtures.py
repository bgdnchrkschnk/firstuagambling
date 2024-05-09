import pytest
from playwright.sync_api import Browser
from api_client.api_client_events import APIClientEvents


@pytest.fixture(scope='module')
def s_page(browser: Browser):
    page = browser.new_page()
    yield page
    page.close()


@pytest.fixture(scope='session')
def client():
    client = APIClientEvents()
    yield client
    del client
