from playwright.sync_api import sync_playwright, expect

def test_open_boozt():
    with sync_playwright() as p:
        # Use Firefox instead of Chromium
        browser = p.firefox.launch(headless=False)
        page = browser.new_page()
        
        page.goto("https://www.boozt.com/")
        
        expect(page).to_have_url("https://www.boozt.com/")
        
        browser.close()

if __name__ == "__main__":
    test_open_boozt()