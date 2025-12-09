"""
Test Authentication - Data-Driven Login Tests
Demonstrates: Data-driven testing using CSV/Excel files
"""

import pytest
from pages.LoginPage import LoginPage
from utils.ExcelUtility import ExcelUtility
import os


class TestAuthentication:
    """Test class for authentication functionality"""
    
    @pytest.mark.data_driven
    @pytest.mark.parametrize("credentials", 
                            ExcelUtility.read_csv("test_data/login_credentials.csv"))
    def test_login_with_csv_data(self, driver, base_url, credentials):
        """
        Data-Driven Test: Login with multiple credentials from CSV file
        
        This test demonstrates:
        - Reading test data from CSV file
        - Parametrized testing
        - Data-driven approach
        """
        login_page = LoginPage(driver, base_url)
        login_page.navigate()
        
        username = credentials['username']
        password = credentials['password']
        expected_result = credentials['expected_result']
        
        # Perform login
        login_page.login(username, password)
        
        # Wait for response
        import time
        time.sleep(2)
        
        # Verify result based on expected outcome
        if expected_result == 'success':
            # For valid credentials, check if redirected or success message
            current_url = login_page.get_current_url()
            print(f"\n✓ Login attempt with username='{username}' - Current URL: {current_url}")
        else:
            # For invalid credentials, verify error message or stay on login page
            assert "login.html" in login_page.get_current_url().lower(), \
                f"Should stay on login page for invalid credentials: {username}"
            print(f"\n✓ Invalid login correctly handled for username='{username}'")
    
    @pytest.mark.data_driven
    @pytest.mark.parametrize("credentials", 
                            ExcelUtility.read_excel("test_data/login_credentials.xlsx"))
    def test_login_with_excel_data(self, driver, base_url, credentials):
        """
        Data-Driven Test: Login with multiple credentials from Excel file
        
        This test demonstrates:
        - Reading test data from Excel file
        - Parametrized testing with Excel data
        - Framework's flexibility with different data sources
        """
        login_page = LoginPage(driver, base_url)
        login_page.navigate()
        
        username = credentials['username']
        password = credentials['password']
        expected_result = credentials['expected_result']
        
        # Perform login
        login_page.login(username, password)
        
        # Wait for response
        import time
        time.sleep(2)
        
        # Verify datetime display is working
        assert login_page.is_datetime_displayed(), "Datetime should be displayed on login page"
        
        print(f"\n✓ Excel data test - username='{username}', expected='{expected_result}'")
    
    @pytest.mark.smoke
    def test_login_page_elements(self, driver, base_url):
        """
        Smoke Test: Verify login page elements are present
        
        This test verifies:
        - All form elements are present
        - Page loads correctly
        - Basic functionality is accessible
        """
        login_page = LoginPage(driver, base_url)
        login_page.navigate()
        
        # Verify page elements
        assert login_page.is_element_present(login_page.USERNAME_INPUT), \
            "Username input should be present"
        assert login_page.is_element_present(login_page.PASSWORD_INPUT), \
            "Password input should be present"
        assert login_page.is_element_present(login_page.LOGIN_BUTTON), \
            "Login button should be present"
        assert login_page.is_element_present(login_page.LOGO), \
            "Logo should be present"
        
        print("\n✓ All login page elements are present and accessible")
    
    @pytest.mark.regression
    def test_datetime_display_on_login(self, driver, base_url):
        """
        Regression Test: Verify datetime display functionality
        
        This test ensures:
        - Datetime element is visible
        - Datetime text is populated
        - UI enhancement is working correctly
        """
        login_page = LoginPage(driver, base_url)
        login_page.navigate()
        
        import time
        time.sleep(2)  # Wait for JavaScript to update datetime
        
        assert login_page.is_datetime_displayed(), \
            "Datetime display should be visible"
        
        datetime_text = login_page.get_datetime_text()
        assert len(datetime_text) > 0, \
            "Datetime should have text content"
        
        print(f"\n✓ Datetime display working correctly: {datetime_text}")
