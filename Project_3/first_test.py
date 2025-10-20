from playwright.sync_api import Page, sync_playwright
import pytest

@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False, slow_mo=5000)
        page = browser.new_page()
        yield page

def try_test(page:Page):
    page.goto("https://engeto.cz")
    link = page.locator("a[href='/prehled-kurzu/']")
    link.click()
    assert page.url == "https://engeto.cz/prehled-kurzu"