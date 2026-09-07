from playwright.sync_api import Page, expect

from pages.home_page import HomePage
from utils.logger import logger
import re


def test_filter_brand(page: Page):

    logger.info("Starting brand filter test")

    home_page = HomePage(page)
    
    # Select Men
    home_page.select_men()

    # Open Brands
    home_page.select_brands()

    # Select Adidas
    home_page.select_adidas()

    # Verify Adidas heading
    try:
        expect(home_page.get_adidas_heading()).to_be_visible(timeout=10000)

        logger.info("Verified Adidas heading is visible")

    except AssertionError:
        logger.error(
            "Adidas heading was not visible after selecting the brand"
        )
        raise

    # Verify Adidas URL
    try:
        expect(page).to_have_url(
            re.compile(r"/adidas/men", re.IGNORECASE)
        )

        logger.info(
            "Verified Adidas brand in URL: %s",
            page.url
        )

    except AssertionError:
        logger.error(
            "Expected Adidas URL but current URL is: %s",
            page.url
        )
        raise

    logger.info("Brand filter test completed successfully")