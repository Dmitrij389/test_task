import pytest
from selenium.webdriver.common.by import By
from pages_with_footer import get_pages_with_footer

FOOTER_LOCATORS = {
    "start_project_button": (By.XPATH, "//button[contains(@class, 'StartProjectButton_root__')]"),
    "email_link": (By.XPATH, "//a[contains(@href, 'mailto:hello@only.digital')]"),
}

PAGES_TO_TEST = get_pages_with_footer()

@pytest.mark.parametrize("url", PAGES_TO_TEST)
def test_footer_elements_present(driver, url):
    print(f"\n[TEST] Checking footer on: {url}")
    driver.get(url)

    footer = driver.find_elements(By.TAG_NAME, "footer")
    assert footer, f"[FAIL] Footer not found on page: {url}"
    print(f"[PASS] Footer found on: {url}")

    for name, locator in FOOTER_LOCATORS.items():
        element = footer[0].find_elements(*locator)
        assert element, f"[FAIL] '{name}' not found in footer on page: {url}"
        print(f"[PASS] '{name}' found in footer on page: {url}")
