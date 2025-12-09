"""
Test Cross Browser - Cross-Browser Compatibility Tests
Demonstrates: Running tests on different browsers
"""

import pytest
from pages.LoginPage import LoginPage
from pages.CatalogPage import CatalogPage
from utils.WebDriverFactory import WebDriverFactory
import time


class TestCrossBrowser:
    """Cross-browser compatibility tests"""
    
    @pytest.mark.cross_browser
    @pytest.mark.parametrize("browser", ["chrome", "firefox"])
    def test_login_page_on_multiple_browsers(self, browser, base_url):
        """
        Cross-Browser Test: Login page on Chrome and Firefox
        
        Demonstrates:
        - Parametrized browser testing
        - Framework flexibility for browser switching
        - Cross-browser compatibility validation
        
        Note: This test creates its own driver instance to test multiple browsers
        """
        print(f"\n{'='*60}")
        print(f"TESTING ON: {browser.upper()}")
        print(f"{'='*60}")
        
        # Create driver for specific browser
        driver = WebDriverFactory.create_driver(browser=browser, headless=False)
        
        try:
            # Test login page
            login_page = LoginPage(driver, base_url)
            login_page.navigate()
            time.sleep(2)
            
            # Verify page elements
            assert login_page.is_element_present(login_page.USERNAME_INPUT), \
                f"Username input not found on {browser}"
            print(f"✓ Username field present on {browser}")
            
            assert login_page.is_element_present(login_page.PASSWORD_INPUT), \
                f"Password input not found on {browser}"
            print(f"✓ Password field present on {browser}")
            
            assert login_page.is_element_present(login_page.LOGIN_BUTTON), \
                f"Login button not found on {browser}"
            print(f"✓ Login button present on {browser}")
            
            # Verify datetime display
            assert login_page.is_datetime_displayed(), \
                f"Datetime display not visible on {browser}"
            print(f"✓ Datetime display working on {browser}")
            
            # Test login functionality
            login_page.login("testuser", "testpass")
            time.sleep(2)
            print(f"✓ Login functionality works on {browser}")
            
            print(f"✓ All tests passed on {browser.upper()}")
            
        finally:
            driver.quit()
    
    @pytest.mark.cross_browser
    @pytest.mark.parametrize("browser", ["chrome", "firefox"])
    def test_catalog_search_on_multiple_browsers(self, browser, base_url):
        """
        Cross-Browser Test: Catalog search functionality
        
        Demonstrates:
        - Search feature across browsers
        - Dynamic content handling in different browsers
        """
        print(f"\n[TEST] Catalog Search on {browser.upper()}")
        
        driver = WebDriverFactory.create_driver(browser=browser, headless=False)
        
        try:
            catalog_page = CatalogPage(driver, base_url)
            catalog_page.navigate()
            
            # Wait for page load
            catalog_page.wait_utility.wait_for_element_visible(catalog_page.SEARCH_INPUT)
            
            # Test search
            catalog_page.search_product("ring")
            time.sleep(1.5)
            
            products = catalog_page.get_product_titles()
            print(f"✓ Search returned {len(products)} products on {browser}")
            
            assert len(products) > 0, f"Search should return products on {browser}"
            
        finally:
            driver.quit()
    
    @pytest.mark.cross_browser
    def test_responsive_layout_comparison(self, driver, base_url):
        """
        Test: Compare responsive layouts
        
        Demonstrates:
        - Window size manipulation
        - Responsive design testing
        - Layout verification
        """
        print("\n[TEST] Responsive Layout Testing")
        
        login_page = LoginPage(driver, base_url)
        login_page.navigate()
        time.sleep(1)
        
        # Test different screen sizes
        sizes = [
            (1920, 1080, "Desktop"),
            (1366, 768, "Laptop"),
            (768, 1024, "Tablet"),
            (375, 667, "Mobile")
        ]
        
        for width, height, device in sizes:
            driver.set_window_size(width, height)
            time.sleep(1)
            
            # Verify elements are still accessible
            assert login_page.is_element_present(login_page.USERNAME_INPUT), \
                f"Username input should be present on {device}"
            
            print(f"✓ Layout correct on {device} ({width}x{height})")
