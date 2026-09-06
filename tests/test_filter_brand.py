import re
import time

from playwright.sync_api import Page, expect
from utils.logger import logger


def test_filter_brand(page: Page):

    logger.info("Starting brand filter test")

    # Select Men category
    logger.info("Selecting Men category")
    men_category = page.get_by_role("link", name="Men", exact=True)
    men_category.click()

    page.wait_for_load_state("load")
    time.sleep(3)

    # Open Brands
    logger.info("Selecting Brands")
    brand_select = page.get_by_role("link", name="Brands")
    brand_select.click()

    # Select Adidas
    logger.info("Selecting Adidas")
    page.get_by_role("link", name="adidas", exact=True).click()

    page.wait_for_load_state("load")
    time.sleep(3)

    # Verify Adidas page heading
    try:
        adidas_heading = page.get_by_role("heading", name=re.compile(r"^adidas for men$", re.IGNORECASE))
        expect(adidas_heading).to_be_visible(timeout=10000)

        logger.info("Verified Adidas heading is visible")

    except AssertionError:
        logger.error("Adidas heading was not visible after selecting the brand")
        raise

    # Verify Adidas is also present in the URL
    try:
        expect(page).to_have_url(re.compile(r"/adidas/men", re.IGNORECASE))

        logger.info("Verified Adidas brand in URL: %s", page.url)

    except AssertionError:
        logger.error("Expected Adidas URL but current URL is: %s", page.url)
        raise

    logger.info("Brand filter test completed successfully")