import pytest
import requests
from playwright.sync_api import Browser
from test.integration_tests.steps import APIClientSteps


@pytest.fixture(scope='module')
def s_page(browser: Browser):
    page = browser.new_page()
    yield page
    page.close()


@pytest.fixture(scope='session')
def client():
    client = APIClientSteps()
    yield client
    del client