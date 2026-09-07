# DEIF_QualityEngineer

This repository includes UI test cases for boozt.com submitted as a technical task.

# Conftest.py

This file makes our testing easier. It contains the pytest setup that is required before executing the tests.
Pytest fixtures are defined which we use in our main test files as session or hooks.
They are used to:
- Launch the browser
- Create a fresh browser context for every test
- Open the targetted URL (Boozt.com)
From opening the page, accepting cookies and changinge language, every important prerequisite step is executed.
Logger is also defined which helps to track the test execution code with timestamp and sentences

# Pages

Page object Model (POM) approach is used. As this is UI test automation and there are multiple pages where the test performs certain actions, the actions require accessing the locators and these all are separated from main test files to get a better and easy to understand overview of the test steps.

# Tests
There are two test files:

- Add to cart
  
- Filter based on brand

# Installation


Create and activate a virtual environment if required:

python -m venv venv

source venv/bin/activate

Install the dependencies:

pip install -r requirements.txt

Install the Playwright browser:

playwright install chromium

# How to Run

Run all tests:

pytest

# Run only the Add to Cart test:

pytest tests/test_add_product_to_cart.py

# Run only the Brand Filter test:

pytest tests/test_filter_brand.py