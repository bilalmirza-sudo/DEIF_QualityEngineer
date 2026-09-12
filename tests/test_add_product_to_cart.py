from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from utils.logger import logger


def test_add_product_to_cart(page: Page):

    logger.info("Starting add-to-cart test")

    home_page = HomePage(page)
    product_page = ProductPage(page)
    cart_page = CartPage(page)

    # Search product
    home_page.search_product("nike shoes")

    # Select Women
    home_page.select_women()

    # Select first dynamically available product
    product_name = home_page.open_first_product()

    # Select first available size and add product to cart
    selected_size = product_page.add_first_available_size_to_cart(product_name)

    # Open cart
    cart_page.open_cart()

    # Verify product
    try:
        expect(cart_page.get_product(product_name)).to_be_visible()

        logger.info(
            "Verified product in cart: %s",
            product_name
        )

    except AssertionError:
        logger.error(
            "Product verification failed. Product not found in cart: %s",
            product_name
        )
        raise

    # Verify selected size
    try:
        expect(cart_page.get_size(selected_size)).to_be_visible()

        logger.info(
            "Verified the size in cart: %s",
            selected_size
        )

    except AssertionError:
        logger.error(
            "Size verification failed. Expected size %s was not found for product: %s",
            selected_size,
            product_name
        )
        raise

    logger.info("Add-to-cart test completed successfully")