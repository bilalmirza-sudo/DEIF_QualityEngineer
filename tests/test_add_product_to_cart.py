import time
from playwright.sync_api import Page, expect
from utils.logger import logger


def test_add_product_to_cart(page: Page):

    logger.info("Starting add-to-cart test")

    # Search for Nike shoes
    logger.info("Opening search")
    time.sleep(5)
    
    search_button = page.get_by_role("button", name="Search", exact=True)
    expect(search_button).to_be_visible(timeout=10000)
    search_button.click()

    search_input = page.locator("#desktopSearch").get_by_placeholder("Search products or brands")
    expect(search_input).to_be_visible(timeout=10000)

    logger.info("Search input is visible")

    search_input.fill("nike shoes")
    search_input.press("Enter")

    logger.info("Searched for Nike shoes")

    # Select Women
    page.get_by_role("tab", name="Women").click()
    logger.info("Selected Women tab")

    # Get first displayed product
    products = page.locator(".srp-products [role='article'][data-product-name]")

    try:
        expect(products.first).to_be_visible()
        logger.info("Search results are visible")
    except AssertionError:
        logger.error("No products were displayed in the search results")
        raise

    product = products.first

    # Store product name
    product_name = product.get_attribute("data-product-name")

    if product_name is None:
        logger.error("Product name could not be retrieved")
        raise AssertionError("Product name not found")

    logger.info(f"Selected product: {product_name}")

    # Open product
    product.locator("a").first.click()
    logger.info("Opened product detail page")

    # wait here as the page content takes some time to load
    time.sleep(5)

    # Locate Add to cart button
    add_to_cart = page.get_by_role("button", name="Add to cart")

    try:
        expect(add_to_cart).to_be_visible()
        expect(add_to_cart).to_be_enabled()
        logger.info("Add to cart button is visible and enabled")
    except AssertionError:
        logger.error("Add to cart button is not available for product: %s", product_name)
        raise

    add_to_cart.scroll_into_view_if_needed()
    add_to_cart.click()

    logger.info("Clicked Add to cart")

    # Size picker modal should open
    size_modal = page.locator("#sizePickerModal")

    try:
        expect(size_modal).to_be_visible()
        logger.info("Size picker modal opened")
    except AssertionError:
        logger.error("Size picker modal did not open for product: %s", product_name)
        raise

    # Get all size buttons inside modal
    size_buttons = size_modal.locator("button.size-picker-size")

    try:
        expect(size_buttons.first).to_be_visible()
    except AssertionError:
        logger.error("No size options were displayed for product: %s", product_name)
        raise

    selected_size = None

    # Select first available size
    for i in range(size_buttons.count()):
        size_button = size_buttons.nth(i)

        if size_button.is_visible() and size_button.is_enabled():
            selected_size = size_button.inner_text().strip()
            size_button.click()
            break

    if selected_size is None:
        logger.error("No available size found for product: %s", product_name)
        raise AssertionError("No available size found")

    logger.info("Selected size: %s", selected_size)

    time.sleep(1)

    # Add to cart
    page.get_by_label("Add to cart").click()

    logger.info(
        "Product added to cart: %s | Size: %s",
        product_name,
        selected_size
    )

    time.sleep(1)

    # Open cart
    page.get_by_role("button", name="Go to cart", exact=True).click()
    logger.info("Opened cart")

    time.sleep(2)

    # Verify product
    try:
        expect(page.get_by_text(product_name, exact=False).first).to_be_visible()
        logger.info("Verified product in cart: %s", product_name)
    except AssertionError:
        logger.error("Product verification failed. Product not found in cart: %s", product_name)
        raise

    # Verify size
    try:
        expect(page.get_by_text(selected_size, exact=True).first).to_be_visible()
        logger.info("Verified size in cart: %s", selected_size)
    except AssertionError:
        logger.error(
            "Size verification failed. Expected size %s was not found in cart for product: %s",
            selected_size,
            product_name
        )
        raise

    logger.info("Add-to-cart test completed successfully")