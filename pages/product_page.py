import time

from playwright.sync_api import Page, expect
from utils.logger import logger


class ProductPage:

    def __init__(self, page: Page):
        self.page = page

    def add_first_available_size_to_cart(self, product_name: str):

        # Boozt PDP stabilization wait
        time.sleep(5)

        add_to_cart = self.page.get_by_role("button", name="Add to cart")

        try:
            expect(add_to_cart).to_be_visible()
            expect(add_to_cart).to_be_enabled()

            logger.info("Add to cart button is visible and enabled")

        except AssertionError:
            logger.error(
                "Add to cart button is not available for product: %s",
                product_name
            )
            raise

        add_to_cart.scroll_into_view_if_needed()
        add_to_cart.click()

        logger.info("Clicked Add to cart")

        size_modal = self.page.locator("#sizePickerModal")

        try:
            expect(size_modal).to_be_visible()
            logger.info("Size picker modal opened")

        except AssertionError:
            logger.error(
                "Size picker modal did not open for product: %s",
                product_name
            )
            raise

        # Exclude sizes marked out-of-stock by Boozt
        available_sizes = size_modal.locator("button.size-picker-size:not(.size-picker-size--is-oos)")

        try:
            expect(available_sizes.first).to_be_visible()

        except AssertionError:
            logger.error(
                "No available sizes were displayed for product: %s",
                product_name
            )
            raise

        selected_size = None

        for i in range(available_sizes.count()):

            size_button = available_sizes.nth(i)

            if size_button.is_visible() and size_button.is_enabled():

                selected_size = size_button.inner_text().strip()
                size_button.click()
                break

        if selected_size is None:
            logger.error(
                "No available size could be selected for product: %s",
                product_name
            )

            raise AssertionError("No available size found")

        logger.info("Selected available size: %s", selected_size)

        time.sleep(1)

        # Confirm Add to cart after selecting size
        self.page.get_by_label("Add to cart").click()

        logger.info(
            "Product added to cart: %s | Size: %s",
            product_name,
            selected_size
        )

        time.sleep(1)

        return selected_size