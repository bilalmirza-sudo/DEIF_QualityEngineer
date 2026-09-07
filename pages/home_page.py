import re
import time
from playwright.sync_api import Page, expect
from utils.logger import logger


class HomePage:

    def __init__(self, page: Page):
        self.page = page

    def search_product(self, search_term: str):

        logger.info("Opening search")

        # Short wait for Boozt client-side content
        time.sleep(3)

        self.page.get_by_role("button", name="Search").click()

        search_input = self.page.locator("#desktopSearch").get_by_placeholder("Search products or brands")

        try:
            expect(search_input).to_be_visible(timeout=10000)
            logger.info("Search input is visible")
        except AssertionError:
            logger.error("Search input did not become visible")
            raise

        search_input.fill(search_term)
        search_input.press("Enter")

        logger.info("Searched for: %s", search_term)

    def select_women(self):

        self.page.get_by_role("tab", name="Women").click()
        logger.info("Selected Women tab")

    def open_first_product(self):

        products = self.page.locator(".srp-products [role='article'][data-product-name]")

        try:
            expect(products.first).to_be_visible()
            logger.info("Search results are visible")
        except AssertionError:
            logger.error("No products were displayed in search results")
            raise

        product = products.first

        product_name = product.get_attribute("data-product-name")

        if product_name is None:
            logger.error("Product name could not be retrieved")
            raise AssertionError("Product name not found")

        logger.info("Selected product: %s", product_name)

        product.locator("a").first.click()

        logger.info("Opened product detail page")

        return product_name

    def select_men(self):

        logger.info("Selecting Men category")

        men_category = self.page.get_by_role("link", name="Men", exact=True)
        men_category.click()

        self.page.wait_for_load_state("load")

    def select_brands(self):

        logger.info("Selecting Brands")

        brand_select = self.page.get_by_role("link", name="Brands")
        brand_select.click()

    def select_adidas(self):

        logger.info("Selecting Adidas")

        self.page.get_by_role("link", name="adidas", exact=True).click()

        self.page.wait_for_load_state("load")
        time.sleep(3)

    def get_adidas_heading(self):

        return self.page.get_by_role(
            "heading",
            name=re.compile(r"^adidas for men$", re.IGNORECASE)
        )