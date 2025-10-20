from playwright.sync_api import Page, sync_playwright
import pytest

@pytest.fixture
def page():
    with sync_playwright() as p:
        # browser = p.firefox.launch(headless=False, slow_mo=5000)
        browser = p.firefox.launch(headless=False, slow_mo=2000)
        page = browser.new_page()
        yield page


# cookies confirmation test
def test_confirm_cookies(page: Page):
    page.goto("https://engeto.cz")
    cookies_button = page.locator("#cookiescript_accept")
    cookies_button.click()
    cookies_window = page.locator("#cookiescript_injected")
    page.wait_for_timeout(2000)
    assert cookies_window.is_visible() == False


# overview - educational courses
def test_show_overview(page: Page):
    page.goto("https://engeto.cz")
    page.locator("#cookiescript_accept").click()
    course_overview = page.locator("a[href='/prehled-kurzu/']").nth(0)
    course_overview.click()
    assert page.url == "https://engeto.cz/prehled-kurzu/"


# login test - Engeto learning portal
def test_educational_portal(page: Page):
    page.goto("https://engeto.cz")
    page.locator("#cookiescript_accept").click()
    page.locator("div.main-navigation a[href='https://portal.engeto.com/']:visible").click()
    page.locator('a[role="button"]').click()
    page.fill("#username", "test-username")
    page.fill("#password", "test-password")
    page.locator('button[type="submit"]').click()
    assert page.locator("#error-element-password").is_visible


# video launch test
def test_pop_up(page: Page):
    page.goto("https://engeto.cz")
    page.locator("#cookiescript_accept").click()
    page.locator("a[href='https://engeto.cz/prehled-kurzu/']:has-text('Kurzy')").hover()
    page.wait_for_timeout(1000)
    page.locator(".sub-menu a[href='https://www.engeto.cz/jak-zacit-v-it/']:has-text('Jak vybrat správný kurz')").click()
    page.locator("body > main > div.video-header.flex.flex-mobile-column.flex-ai-s.gap-64.gap-mobile-48 > div.right.video.flex.flex-row.radius-12.fullwidth > a > div").click()
    page.wait_for_timeout(2000)
    assert page.locator("div.ytp-cued-thumbnail-overlay").is_visible


# newsletter subscription test - invalid emailtest for 
def test_fill_invalid_email(page: Page):
    page.goto("https://engeto.cz")
    page.locator("#cookiescript_accept").click()
    page.fill("input[name='newsletter-form-email']", "invalid_email")
    page.locator("a[target='_self']:has-text('Odebírat')").click()
    assert page.locator("span.error-message")
