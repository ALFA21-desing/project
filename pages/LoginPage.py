"""
LoginPage - Page Object Model for login page
"""

from selenium.webdriver.common.by import By
from pages.BasePage import BasePage


class LoginPage(BasePage):
    """Page Object for Login Page"""
    
    # Locators
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    LOGIN_MESSAGE = (By.ID, "loginMessage")
    REGISTER_LINK = (By.LINK_TEXT, "Register")
    CART_LINK = (By.LINK_TEXT, "Cart")
    LOGO = (By.CLASS_NAME, "logo")
    DATETIME_DISPLAY = (By.ID, "datetime-display")
    
    def __init__(self, driver, base_url):
        """
        Initialize LoginPage
        
        Args:
            driver: WebDriver instance
            base_url: Base URL of the application
        """
        super().__init__(driver)
        self.base_url = base_url
        self.url = f"{base_url}/website/login.html"
    
    def navigate(self):
        """Navigate to login page"""
        self.navigate_to(self.url)
    
    def enter_username(self, username):
        """Enter username"""
        self.type_text(self.USERNAME_INPUT, username)
    
    def enter_password(self, password):
        """Enter password"""
        self.type_text(self.PASSWORD_INPUT, password)
    
    def click_login_button(self):
        """Click login button"""
        self.click(self.LOGIN_BUTTON)
    
    def login(self, username, password):
        """
        Perform login action
        
        Args:
            username (str): Username
            password (str): Password
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
    
    def get_login_message(self):
        """Get login message text"""
        return self.get_text(self.LOGIN_MESSAGE)
    
    def is_login_message_visible(self):
        """Check if login message is visible"""
        return self.is_element_visible(self.LOGIN_MESSAGE)
    
    def click_register_link(self):
        """Click register link"""
        self.click(self.REGISTER_LINK)
    
    def is_datetime_displayed(self):
        """Check if datetime display is visible"""
        return self.is_element_visible(self.DATETIME_DISPLAY)
    
    def get_datetime_text(self):
        """Get datetime display text"""
        return self.get_text(self.DATETIME_DISPLAY)
