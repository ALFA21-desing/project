
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.WaitUtility import WaitUtility


class BasePage:
    """Base class for all page objects"""
    
    def __init__(self, driver):
        """
        Initialize BasePage
        
        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.wait_utility = WaitUtility(driver)
    
    def navigate_to(self, url):
        """Navigate to a specific URL"""
        self.driver.get(url)
    
    def get_current_url(self):
        """Get current page URL"""
        return self.driver.current_url
    
    def get_page_title(self):
        """Get current page title"""
        return self.driver.title
    
    def find_element(self, locator):
        """
        Find a single element
        
        Args:
            locator (tuple): Locator tuple (By.METHOD, "value")
            
        Returns:
            WebElement: Found element
        """
        try:
            return self.driver.find_element(*locator)
        except NoSuchElementException:
            raise NoSuchElementException(f"Element not found: {locator}")
    
    def find_elements(self, locator):
        """
        Find multiple elements
        
        Args:
            locator (tuple): Locator tuple (By.METHOD, "value")
            
        Returns:
            list: List of WebElements
        """
        return self.driver.find_elements(*locator)
    
    def click(self, locator):
        """
        Click on an element
        
        Args:
            locator (tuple): Locator tuple (By.METHOD, "value")
        """
        element = self.wait_utility.wait_for_element_clickable(locator)
        element.click()
    
    def type_text(self, locator, text):
        """
        Type text into an input field
        
        Args:
            locator (tuple): Locator tuple (By.METHOD, "value")
            text (str): Text to type
        """
        element = self.wait_utility.wait_for_element_visible(locator)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator):
        """
        Get text from an element
        
        Args:
            locator (tuple): Locator tuple (By.METHOD, "value")
            
        Returns:
            str: Element text
        """
        element = self.wait_utility.wait_for_element_visible(locator)
        return element.text
    
    def is_element_visible(self, locator, timeout=5):
        """
        Check if element is visible
        
        Args:
            locator (tuple): Locator tuple (By.METHOD, "value")
            timeout (int): Wait timeout in seconds
            
        Returns:
            bool: True if visible, False otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, locator):
        """
        Check if element is present in DOM
        
        Args:
            locator (tuple): Locator tuple (By.METHOD, "value")
            
        Returns:
            bool: True if present, False otherwise
        """
        try:
            self.find_element(locator)
            return True
        except NoSuchElementException:
            return False
    
    def get_attribute(self, locator, attribute):
        """
        Get attribute value from element
        
        Args:
            locator (tuple): Locator tuple (By.METHOD, "value")
            attribute (str): Attribute name
            
        Returns:
            str: Attribute value
        """
        element = self.find_element(locator)
        return element.get_attribute(attribute)
    
    def switch_to_iframe(self, locator):
        """
        Switch to an iframe
        
        Args:
            locator (tuple): Locator tuple (By.METHOD, "value")
        """
        iframe = self.wait_utility.wait_for_element_presence(locator)
        self.driver.switch_to.frame(iframe)
    
    def switch_to_default_content(self):
        """Switch back to default content from iframe"""
        self.driver.switch_to.default_content()
    
    def execute_script(self, script, *args):
        """
        Execute JavaScript
        
        Args:
            script (str): JavaScript code to execute
            *args: Arguments for the script
            
        Returns:
            Any: Script return value
        """
        return self.driver.execute_script(script, *args)
    
    def scroll_to_element(self, locator):
        """
        Scroll to element
        
        Args:
            locator (tuple): Locator tuple (By.METHOD, "value")
        """
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
    
    def take_screenshot(self, filename):
        """
        Take a screenshot
        
        Args:
            filename (str): Screenshot filename
        """
        self.driver.save_screenshot(filename)
