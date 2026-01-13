"""
ContactPage - Page Object Model for contact page
"""

from selenium.webdriver.common.by import By
from pages.BasePage import BasePage


class ContactPage(BasePage):
    """Page Object for Contact Page"""
    
    # Locators
    CONTACT_FORM = (By.TAG_NAME, "form")
    # contacto.html uses Spanish IDs
    NAME_INPUT = (By.ID, "nombre")
    EMAIL_INPUT = (By.ID, "email")
    MESSAGE_TEXTAREA = (By.ID, "mensaje")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    SUCCESS_MESSAGE = (By.CLASS_NAME, "success-message")
    GOOGLE_MAP_IFRAME = (By.TAG_NAME, "iframe")
    
    def __init__(self, driver, base_url):
        """
        Initialize ContactPage
        
        Args:
            driver: WebDriver instance
            base_url: Base URL of the application
        """
        super().__init__(driver)
        self.base_url = base_url
        self.url = f"{base_url}/website/contacto.html"
    
    def navigate(self):
        """Navigate to contact page"""
        self.navigate_to(self.url)
    
    def fill_contact_form(self, name, email, message):
        """
        Fill and submit contact form
        
        Args:
            name (str): Name
            email (str): Email
            message (str): Message
        """
        self.type_text(self.NAME_INPUT, name)
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.MESSAGE_TEXTAREA, message)
    
    def submit_form(self):
        """Submit contact form"""
        self.click(self.SUBMIT_BUTTON)
    
    def is_iframe_present(self):
        """Check if Google Maps iframe is present"""
        return self.is_element_present(self.GOOGLE_MAP_IFRAME)
    
    def interact_with_iframe(self):
        """
        Demonstrate iframe interaction
        Switch to iframe context and back
        """
        if self.is_iframe_present():
            # Switch to iframe
            self.switch_to_iframe(self.GOOGLE_MAP_IFRAME)
            
            # Perform actions inside iframe (e.g., check if map is loaded)
            # Note: Google Maps iframe may have restrictions
            
            # Switch back to default content
            self.switch_to_default_content()
            return True
        return False
