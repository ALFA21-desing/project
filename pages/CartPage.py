"""
CartPage - Page Object Model for shopping cart page
"""

from selenium.webdriver.common.by import By
from pages.BasePage import BasePage
import time


class CartPage(BasePage):
    """Page Object for Cart Page"""
    
    # Locators
    CART_ITEMS = (By.CSS_SELECTOR, ".cart-item")
    ITEM_TITLES = (By.CSS_SELECTOR, ".cart-item h3")
    ITEM_PRICES = (By.CSS_SELECTOR, ".cart-item .price")
    ITEM_QUANTITIES = (By.CSS_SELECTOR, ".cart-item .quantity")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, ".cart-item .remove-btn")
    TOTAL_AMOUNT = (By.CLASS_NAME, "total-amount")
    CHECKOUT_BUTTON = (By.ID, "checkout-btn")
    EMPTY_CART_MESSAGE = (By.CLASS_NAME, "empty-cart")
    
    # Checkout form locators
    CHECKOUT_FORM = (By.ID, "checkout-form")
    FULL_NAME_INPUT = (By.ID, "fullName")
    EMAIL_INPUT = (By.ID, "email")
    PHONE_INPUT = (By.ID, "phone")
    ADDRESS_INPUT = (By.ID, "address")
    CITY_INPUT = (By.ID, "city")
    STATE_INPUT = (By.ID, "state")
    ZIP_INPUT = (By.ID, "zipCode")
    CARD_NUMBER_INPUT = (By.ID, "cardNumber")
    CARD_NAME_INPUT = (By.ID, "cardName")
    EXPIRY_INPUT = (By.ID, "expiryDate")
    CVV_INPUT = (By.ID, "cvv")
    PLACE_ORDER_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    
    # Multi-step form navigation
    NEXT_STEP_BUTTON = (By.CLASS_NAME, "next-step")
    PREV_STEP_BUTTON = (By.CLASS_NAME, "prev-step")
    FORM_STEPS = (By.CLASS_NAME, "form-step")
    
    def __init__(self, driver, base_url):
        """
        Initialize CartPage
        
        Args:
            driver: WebDriver instance
            base_url: Base URL of the application
        """
        super().__init__(driver)
        self.base_url = base_url
        self.url = f"{base_url}/website/cart.html"
    
    def navigate(self):
        """Navigate to cart page"""
        self.navigate_to(self.url)
    
    def get_cart_items_count(self):
        """Get number of items in cart"""
        return len(self.find_elements(self.CART_ITEMS))
    
    def get_cart_item_titles(self):
        """Get all cart item titles"""
        return [item.text for item in self.find_elements(self.ITEM_TITLES)]
    
    def get_total_amount(self):
        """Get total cart amount"""
        return self.get_text(self.TOTAL_AMOUNT)
    
    def is_cart_empty(self):
        """Check if cart is empty"""
        return self.is_element_visible(self.EMPTY_CART_MESSAGE, timeout=3)
    
    def click_checkout_button(self):
        """Click checkout button"""
        self.click(self.CHECKOUT_BUTTON)
        time.sleep(1)
    
    def remove_first_item(self):
        """Remove first item from cart"""
        buttons = self.find_elements(self.REMOVE_BUTTONS)
        if buttons:
            buttons[0].click()
            time.sleep(0.5)
    
    # Checkout form methods
    def fill_personal_info(self, name, email, phone):
        """
        Fill personal information
        
        Args:
            name (str): Full name
            email (str): Email address
            phone (str): Phone number
        """
        self.type_text(self.FULL_NAME_INPUT, name)
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.PHONE_INPUT, phone)
    
    def fill_shipping_address(self, address, city, state, zip_code):
        """
        Fill shipping address
        
        Args:
            address (str): Street address
            city (str): City
            state (str): State
            zip_code (str): ZIP code
        """
        self.type_text(self.ADDRESS_INPUT, address)
        self.type_text(self.CITY_INPUT, city)
        self.type_text(self.STATE_INPUT, state)
        self.type_text(self.ZIP_INPUT, zip_code)
    
    def fill_payment_info(self, card_number, card_name, expiry, cvv):
        """
        Fill payment information
        
        Args:
            card_number (str): Card number
            card_name (str): Name on card
            expiry (str): Expiry date
            cvv (str): CVV code
        """
        self.type_text(self.CARD_NUMBER_INPUT, card_number)
        self.type_text(self.CARD_NAME_INPUT, card_name)
        self.type_text(self.EXPIRY_INPUT, expiry)
        self.type_text(self.CVV_INPUT, cvv)
    
    def click_next_step(self):
        """Click next step button in multi-step form"""
        self.click(self.NEXT_STEP_BUTTON)
        time.sleep(0.5)
    
    def click_previous_step(self):
        """Click previous step button in multi-step form"""
        self.click(self.PREV_STEP_BUTTON)
        time.sleep(0.5)
    
    def click_place_order(self):
        """Click place order button"""
        self.click(self.PLACE_ORDER_BUTTON)
        time.sleep(1)
    
    def complete_checkout(self, personal_info, shipping_info, payment_info):
        """
        Complete entire checkout process
        
        Args:
            personal_info (dict): Personal information
            shipping_info (dict): Shipping information
            payment_info (dict): Payment information
        """
        self.click_checkout_button()
        
        # Step 1: Personal Info
        self.fill_personal_info(
            personal_info['name'],
            personal_info['email'],
            personal_info['phone']
        )
        self.click_next_step()
        
        # Step 2: Shipping Address
        self.fill_shipping_address(
            shipping_info['address'],
            shipping_info['city'],
            shipping_info['state'],
            shipping_info['zip']
        )
        self.click_next_step()
        
        # Step 3: Payment Info
        self.fill_payment_info(
            payment_info['card_number'],
            payment_info['card_name'],
            payment_info['expiry'],
            payment_info['cvv']
        )
        self.click_place_order()
