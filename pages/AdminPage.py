"""
AdminPage - Page object for the administration dashboard
"""

from selenium.webdriver.common.by import By


class AdminPage:
    """Page object for the product admin dashboard."""

    PRODUCT_ROWS = (By.CSS_SELECTOR, "#productsTable tbody tr")
    LOGOUT_LINK = (By.ID, "logoutLink")

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url.rstrip('/')

    def navigate(self):
        self.driver.get(f"{self.base_url}/admin.html")

    def is_loaded(self):
        return self.driver.current_url.lower().endswith("/admin.html")

    def get_product_count(self):
        return len(self.driver.find_elements(*self.PRODUCT_ROWS))

    def logout(self):
        self.driver.find_element(*self.LOGOUT_LINK).click()
