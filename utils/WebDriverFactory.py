"""
WebDriverFactory - Factory pattern for creating WebDriver instances
Supports Chrome and Firefox with configurable options
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


class WebDriverFactory:
    """Factory class to create and configure WebDriver instances"""
    
    @staticmethod
    def create_driver(browser="chrome", headless=False):
        """
        Create a WebDriver instance for the specified browser
        
        Args:
            browser (str): Browser name - 'chrome' or 'firefox'
            headless (bool): Run browser in headless mode
            
        Returns:
            WebDriver: Configured WebDriver instance
        """
        if browser.lower() == "chrome":
            return WebDriverFactory._create_chrome_driver(headless)
        elif browser.lower() == "firefox":
            return WebDriverFactory._create_firefox_driver(headless)
        else:
            raise ValueError(f"Unsupported browser: {browser}. Use 'chrome' or 'firefox'")
    
    @staticmethod
    def _create_chrome_driver(headless=False):
        """Create and configure Chrome WebDriver"""
        options = webdriver.ChromeOptions()
        
        if headless:
            options.add_argument("--headless")
        
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")
        options.add_argument("--ignore-certificate-errors")
        
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(10)
        
        return driver
    
    @staticmethod
    def _create_firefox_driver(headless=False):
        """Create and configure Firefox WebDriver"""
        options = webdriver.FirefoxOptions()
        
        if headless:
            options.add_argument("--headless")
        
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        driver.maximize_window()
        driver.implicitly_wait(10)
        
        return driver
