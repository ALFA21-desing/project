"""
CatalogPage - Page Object Model for catalog page
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.BasePage import BasePage
import time


class CatalogPage(BasePage):
    """Page Object for Catalog Page"""
    
    # Locators
    SEARCH_INPUT = (By.ID, "search-input")
    CATEGORY_SELECT = (By.ID, "filter-category")
    SUBCATEGORY_SELECT = (By.ID, "filter-subcategory")
    PRICE_RANGE_SELECT = (By.ID, "filter-price")
    SORT_SELECT = (By.ID, "filter-sort")
    PRODUCT_CARDS = (By.CLASS_NAME, "product-card")
    PRODUCT_TITLES = (By.CSS_SELECTOR, ".product-card .product-title")
    PRODUCT_PRICES = (By.CSS_SELECTOR, ".product-card .product-price")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, ".product-card [data-add=\"true\"]")
    DATETIME_DISPLAY = (By.ID, "datetime-display")
    CART_COUNT = (By.ID, "cart-count")
    
    def __init__(self, driver, base_url):
        """
        Initialize CatalogPage
        
        Args:
            driver: WebDriver instance
            base_url: Base URL of the application
        """
        super().__init__(driver)
        self.base_url = base_url
        self.url = f"{base_url}/website/catalogo.html"
    
    def navigate(self):
        """Navigate to catalog page"""
        self.navigate_to(self.url)
    
    def search_product(self, search_term):
        """
        Search for a product
        
        Args:
            search_term (str): Search term
        """
        self.type_text(self.SEARCH_INPUT, search_term)
        time.sleep(1)  # Wait for search results to filter
    
    def select_category(self, category):
        """
        Select a category
        
        Args:
            category (str): Category name
        """
        category_element = self.wait_utility.wait_for_element_visible(self.CATEGORY_SELECT)
        select = Select(category_element)
        select.select_by_visible_text(category)
        time.sleep(1)  # Wait for subcategories to load
    
    def select_subcategory(self, subcategory):
        """
        Select a subcategory
        
        Args:
            subcategory (str): Subcategory name
        """
        subcategory_element = self.wait_utility.wait_for_element_visible(self.SUBCATEGORY_SELECT)
        select = Select(subcategory_element)
        select.select_by_visible_text(subcategory)
        time.sleep(1)
    
    def select_price_range(self, price_range):
        """
        Select a price range
        
        Args:
            price_range (str): Price range value
        """
        price_element = self.wait_utility.wait_for_element_visible(self.PRICE_RANGE_SELECT)
        select = Select(price_element)
        select.select_by_value(price_range)
        time.sleep(1)
    
    def select_sort_option(self, sort_option):
        """
        Select a sort option
        
        Args:
            sort_option (str): Sort option value
        """
        sort_element = self.wait_utility.wait_for_element_visible(self.SORT_SELECT)
        select = Select(sort_element)
        select.select_by_value(sort_option)
        time.sleep(1)
    
    def get_product_count(self):
        """Get number of visible products"""
        visible_products = [p for p in self.find_elements(self.PRODUCT_CARDS) 
                           if p.is_displayed()]
        return len(visible_products)
    
    def get_product_titles(self):
        """Get all visible product titles"""
        titles = []
        for title in self.find_elements(self.PRODUCT_TITLES):
            if title.is_displayed():
                titles.append(title.text)
        return titles
    
    def get_product_prices(self):
        """Get all visible product prices"""
        prices = []
        for price in self.find_elements(self.PRODUCT_PRICES):
            if price.is_displayed():
                prices.append(price.text)
        return prices
    
    def add_first_product_to_cart(self):
        """Add first visible product to cart"""
        buttons = self.find_elements(self.ADD_TO_CART_BUTTONS)
        for button in buttons:
            if button.is_displayed():
                button.click()
                time.sleep(0.5)
                break
    
    def add_product_to_cart_by_index(self, index):
        """
        Add product to cart by index
        
        Args:
            index (int): Product index (0-based)
        """
        buttons = self.find_elements(self.ADD_TO_CART_BUTTONS)
        visible_buttons = [b for b in buttons if b.is_displayed()]
        if index < len(visible_buttons):
            visible_buttons[index].click()
            time.sleep(0.5)
    
    def get_cart_count(self):
        """Get cart item count"""
        return self.get_text(self.CART_COUNT)
    
    def wait_for_products_to_load(self, expected_count=None, timeout=10):
        """
        Wait for products to load
        
        Args:
            expected_count (int): Expected number of products
            timeout (int): Timeout in seconds
        """
        if expected_count:
            self.wait_utility.wait_for_number_of_elements(self.PRODUCT_CARDS, expected_count)
        else:
            self.wait_utility.wait_for_element_visible(self.PRODUCT_CARDS)
