"""
WaitUtility - Advanced wait utilities for handling dynamic content
Implements explicit waits and custom wait conditions
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class WaitUtility:
    """Utility class for advanced wait operations"""
    
    def __init__(self, driver, timeout=15):
        """
        Initialize WaitUtility
        
        Args:
            driver: WebDriver instance
            timeout (int): Default timeout in seconds
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    def wait_for_element_visible(self, locator):
        """
        Wait for element to be visible
        
        Args:
            locator (tuple): Locator tuple (By.METHOD, "value")
            
        Returns:
            WebElement: The visible element
        """
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            raise TimeoutException(f"Element not visible: {locator}")
    
    def wait_for_element_clickable(self, locator):
        """
        Wait for element to be clickable
        
        Args:
            locator (tuple): Locator tuple (By.METHOD, "value")
            
        Returns:
            WebElement: The clickable element
        """
        try:
            return self.wait.until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            raise TimeoutException(f"Element not clickable: {locator}")
    
    def wait_for_element_presence(self, locator):
        """
        Wait for element to be present in DOM
        
        Args:
            locator (tuple): Locator tuple (By.METHOD, "value")
            
        Returns:
            WebElement: The present element
        """
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            raise TimeoutException(f"Element not present: {locator}")
    
    def wait_for_text_in_element(self, locator, text):
        """
        Wait for specific text to appear in element
        
        Args:
            locator (tuple): Locator tuple (By.METHOD, "value")
            text (str): Expected text
            
        Returns:
            bool: True if text is found
        """
        try:
            return self.wait.until(EC.text_to_be_present_in_element(locator, text))
        except TimeoutException:
            raise TimeoutException(f"Text '{text}' not found in element: {locator}")
    
    def wait_for_url_contains(self, url_fragment):
        """
        Wait for URL to contain specific text
        
        Args:
            url_fragment (str): Expected URL fragment
            
        Returns:
            bool: True if URL contains the fragment
        """
        try:
            return self.wait.until(EC.url_contains(url_fragment))
        except TimeoutException:
            raise TimeoutException(f"URL does not contain: {url_fragment}")
    
    def wait_for_element_invisible(self, locator):
        """
        Wait for element to become invisible
        
        Args:
            locator (tuple): Locator tuple (By.METHOD, "value")
            
        Returns:
            bool: True if element is invisible
        """
        try:
            return self.wait.until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            raise TimeoutException(f"Element still visible: {locator}")
    
    def wait_for_number_of_elements(self, locator, count):
        """
        Wait for specific number of elements
        
        Args:
            locator (tuple): Locator tuple (By.METHOD, "value")
            count (int): Expected number of elements
            
        Returns:
            list: List of WebElements
        """
        def check_count(driver):
            elements = driver.find_elements(*locator)
            return elements if len(elements) == count else False
        
        try:
            return self.wait.until(check_count)
        except TimeoutException:
            raise TimeoutException(f"Expected {count} elements, found different count: {locator}")
    
    def wait_for_alert_present(self):
        """
        Wait for alert to be present
        
        Returns:
            Alert: The alert object
        """
        try:
            return self.wait.until(EC.alert_is_present())
        except TimeoutException:
            raise TimeoutException("Alert not present")
