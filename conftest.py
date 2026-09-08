import pytest
from playwright.sync_api import Browser, expect, sync_playwright
from utils.logger import logger
import time
BASE_URL = "https://www.boozt.com/en"


@pytest.fixture(scope="session")
def browser():

    logger.info("Launching Chromium browser")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False,slow_mo=300)

        yield browser

        logger.info("Closing Chromium browser")
        browser.close()


@pytest.fixture(scope="session")
def page(browser):
   
    logger.info("Creating new browser context")

    context = browser.new_context()
    page = context.new_page()

    try:
        # Open Boozt
        logger.info("Opening Boozt: %s", BASE_URL)
        page.goto(BASE_URL, wait_until="domcontentloaded")

        # Accept cookies if displayed
        try:
            cookie_btn = page.locator("#didomi-notice-agree-button")
            cookie_btn.wait_for(state="visible", timeout=5000)
            cookie_btn.click()

            logger.info("Cookie banner accepted")

        except Exception:
            logger.info("Cookie banner was not displayed")

        time.sleep(2)
        # Language selectors
        english_selector = page.get_by_role("button", name="EN, Choose your language", exact=True)
        german_selector = page.get_by_role("button", name="DE, Wählen Sie Ihre Sprache", exact=True)

        # Wait until the language selector has loaded
        language_selector = page.locator(
            'button[aria-label="EN, Choose your language"], '
            'button[aria-label="DE, Wählen Sie Ihre Sprache"]'
        )

        expect(language_selector.first).to_be_visible(timeout=10000)

        # Check current language
        if english_selector.is_visible():
            logger.info("Website is already in English")

        else:
            logger.info("Website is currently in German - changing to English")

            expect(german_selector).to_be_visible(timeout=5000)
            german_selector.click()

            english_lang = page.get_by_role("button", name="English", exact=True)
            expect(english_lang).to_be_visible(timeout=5000)
            english_lang.click()

            # Verify that language changed
            expect(english_selector).to_be_visible(timeout=10000)

            logger.info("Language successfully changed to English")

        logger.info("Boozt setup completed")

        # Give the prepared page to the test
        yield page

    finally:
        logger.info("Closing browser context")
        context.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    # Automatically write test results and failures to the log file
    # This helps to catch failures automatically

    outcome = yield
    report = outcome.get_result()

    if report.failed:
        logger.error(
            "TEST FAILED | %s | phase=%s\n%s",
            item.nodeid,
            report.when,
            report.longreprtext
        )

    elif report.when == "call" and report.passed:
        logger.info("TEST PASSED | %s", item.nodeid)

    elif report.when == "call" and report.skipped:
        logger.warning("TEST SKIPPED | %s", item.nodeid)