import time
from playwright.sync_api import Page
from utils.logger import logger


class CartPage:

    def __init__(self, page: Page):
        self.page = page

    def open_cart(self):

        self.page.get_by_role("button", name="Go to cart", exact=True).click()

        logger.info("Opened cart")

        time.sleep(2)

    def get_product(self, product_name: str):

        return self.page.get_by_text(product_name, exact=False).first

    def get_size(self, selected_size: str):

        return self.page.get_by_text(selected_size, exact=True).first