"""
CartPage - Page Object Model for shopping cart page
"""

from selenium.webdriver.common.by import By
from pages.BasePage import BasePage
import time


class CartPage(BasePage):
    """Page Object for Cart Page"""
    
    # Locators (match website/cart.html and cart.js)
    CART_ITEMS = (By.CSS_SELECTOR, "#cart-items .cart-row")
    ITEM_TITLES = (By.CSS_SELECTOR, "#cart-items .cart-title")
    ITEM_PRICES = (By.CSS_SELECTOR, "#cart-items .cart-price")
    ITEM_QUANTITIES = (By.CSS_SELECTOR, "#cart-items .cart-qty input")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "#cart-items button.remove")
    TOTAL_AMOUNT = (By.CSS_SELECTOR, "#cart-total")
    # The checkout form is present on the page in cart.html
    CHECKOUT_FORM = (By.ID, "checkout-form")
    
    # Checkout form locators
    # Checkout form inputs (IDs used in cart.html)
    FULL_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    EMAIL_INPUT = (By.ID, "email")
    PHONE_INPUT = (By.ID, "phone")
    ADDRESS_INPUT = (By.ID, "address")
    CITY_INPUT = (By.ID, "city")
    STATE_INPUT = (By.ID, "state")
    ZIP_INPUT = (By.ID, "zip")
    CARD_NUMBER_INPUT = (By.ID, "card-number")
    CARD_NAME_INPUT = (By.ID, "card-name")
    EXPIRY_INPUT = (By.ID, "card-expiry")
    CVV_INPUT = (By.ID, "card-cvv")
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
        return [item.text.strip() for item in self.find_elements(self.ITEM_TITLES)]
    
    def get_total_amount(self):
        """Get total cart amount"""
        return self.get_text(self.TOTAL_AMOUNT)
    
    def is_cart_empty(self):
        """Check if cart is empty"""
        # cart.js renders a paragraph inside #cart-items when empty
        return self.get_cart_items_count() == 0
    
    def click_checkout_button(self):
        """Click checkout button"""
        # The checkout form is already present; ensure it's visible
        try:
            if self.is_element_visible(self.CHECKOUT_FORM, timeout=2):
                return
        except Exception:
            return
    
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
        # Split name into first/last when possible
        parts = name.split(None, 1)
        first = parts[0] if parts else ''
        last = parts[1] if len(parts) > 1 else ''
        self.type_text(self.FULL_NAME_INPUT, first)
        if hasattr(self, 'LAST_NAME_INPUT'):
            self.type_text(self.LAST_NAME_INPUT, last)
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
        # Use the page's JS flow functions to advance steps
        try:
            self.driver.execute_script('if(window.goToPayment) window.goToPayment();')
            time.sleep(0.5)
        except Exception:
            time.sleep(0.5)
    
    def click_previous_step(self):
        """Click previous step button in multi-step form"""
        try:
            self.driver.execute_script('if(window.goToShipping) window.goToShipping();')
            time.sleep(0.5)
        except Exception:
            time.sleep(0.5)
    
    def click_place_order(self):
        """Click place order button"""
        # Submit the checkout form
        try:
            self.driver.execute_script("document.getElementById('checkout-form') && document.getElementById('checkout-form').dispatchEvent(new Event('submit',{cancelable:true,bubbles:true}));")
            time.sleep(1)
        except Exception:
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
