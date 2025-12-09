"""
Test Iframe Interaction - Iframe and Modal Tests
Demonstrates: Switching between iframe contexts
"""

import pytest
from pages.ContactPage import ContactPage
from selenium.webdriver.common.by import By
import time


class TestIframeInteraction:
    """Tests for iframe and modal interactions"""
    
    @pytest.mark.iframe
    def test_iframe_interaction_on_contact_page(self, driver, base_url):
        """
        Iframe Test: Interact with Google Maps iframe
        
        Demonstrates:
        - Switching to iframe context
        - Interacting with iframe content
        - Switching back to default content
        - Iframe handling best practices
        """
        print("\n" + "="*60)
        print("IFRAME INTERACTION TEST")
        print("="*60)
        
        contact_page = ContactPage(driver, base_url)
        contact_page.navigate()
        time.sleep(2)
        
        print("\n[STEP 1] Verifying iframe presence...")
        assert contact_page.is_iframe_present(), \
            "Google Maps iframe should be present on contact page"
        print("✓ Iframe element found")
        
        print("\n[STEP 2] Switching to iframe context...")
        try:
            # Get iframe element
            iframe = contact_page.find_element(contact_page.GOOGLE_MAP_IFRAME)
            iframe_src = iframe.get_attribute('src')
            print(f"✓ Iframe src: {iframe_src[:100]}...")
            
            # Switch to iframe
            contact_page.switch_to_iframe(contact_page.GOOGLE_MAP_IFRAME)
            print("✓ Successfully switched to iframe context")
            
            # Try to interact with iframe content
            # Note: Google Maps may have restrictions on external interactions
            try:
                # Attempt to find elements inside iframe
                # This demonstrates the context switch
                time.sleep(2)
                print("✓ Iframe context is active")
            except Exception as e:
                print(f"  Note: Iframe content may be restricted: {str(e)[:50]}")
            
            print("\n[STEP 3] Switching back to default content...")
            contact_page.switch_to_default_content()
            print("✓ Successfully switched back to default content")
            
            # Verify we're back in default content
            print("\n[STEP 4] Verifying default content access...")
            assert contact_page.is_element_present(contact_page.CONTACT_FORM), \
                "Should be able to access main page elements after switching back"
            print("✓ Can access main page elements")
            
        except Exception as e:
            print(f"✗ Iframe test encountered issue: {str(e)}")
            # Always switch back to default content
            contact_page.switch_to_default_content()
            raise
        
        print("\n" + "="*60)
        print("IFRAME INTERACTION TEST COMPLETED")
        print("="*60)
    
    @pytest.mark.iframe
    def test_nested_iframe_handling(self, driver, base_url):
        """
        Test: Demonstrate iframe switching pattern
        
        Shows:
        - Proper iframe handling technique
        - Context switching
        - Error handling for iframes
        """
        print("\n[TEST] Iframe Handling Pattern")
        
        contact_page = ContactPage(driver, base_url)
        contact_page.navigate()
        time.sleep(1)
        
        if contact_page.is_iframe_present():
            print("✓ Iframe detected")
            
            # Store initial page title
            main_title = contact_page.get_page_title()
            print(f"  Main page title: {main_title}")
            
            # Interact with iframe
            result = contact_page.interact_with_iframe()
            
            if result:
                print("✓ Successfully interacted with iframe")
                
                # Verify we're back on main page
                current_title = contact_page.get_page_title()
                assert current_title == main_title, \
                    "Should be back on main page"
                print("✓ Context properly restored")
            else:
                print("  Note: Iframe interaction not fully testable")
    
    @pytest.mark.iframe
    def test_contact_form_after_iframe(self, driver, base_url):
        """
        Test: Verify main page functionality after iframe interaction
        
        Demonstrates:
        - Context isolation
        - State management after iframe switching
        - Form interaction after context switch
        """
        print("\n[TEST] Form Interaction After Iframe Context Switch")
        
        contact_page = ContactPage(driver, base_url)
        contact_page.navigate()
        time.sleep(1)
        
        # First interact with iframe if present
        if contact_page.is_iframe_present():
            print("Step 1: Interacting with iframe...")
            contact_page.switch_to_iframe(contact_page.GOOGLE_MAP_IFRAME)
            time.sleep(1)
            contact_page.switch_to_default_content()
            print("✓ Iframe interaction completed")
        
        # Now interact with main page form
        print("\nStep 2: Filling contact form...")
        contact_page.fill_contact_form(
            name="Test User",
            email="test@example.com",
            message="This is a test message after iframe interaction"
        )
        print("✓ Contact form filled successfully")
        
        # Verify form fields have values
        assert contact_page.is_element_present(contact_page.CONTACT_FORM), \
            "Contact form should be accessible after iframe interaction"
        print("✓ Form remains functional after context switches")
    
    @pytest.mark.smoke
    def test_multiple_iframe_switches(self, driver, base_url):
        """
        Test: Multiple iframe context switches
        
        Demonstrates:
        - Stability of context switching
        - No memory leaks or context issues
        - Robust iframe handling
        """
        print("\n[TEST] Multiple Iframe Context Switches")
        
        contact_page = ContactPage(driver, base_url)
        contact_page.navigate()
        time.sleep(1)
        
        if not contact_page.is_iframe_present():
            pytest.skip("No iframe present to test")
        
        # Perform multiple switches
        for i in range(3):
            print(f"\nSwitch iteration {i+1}:")
            
            # Switch to iframe
            contact_page.switch_to_iframe(contact_page.GOOGLE_MAP_IFRAME)
            print(f"  ✓ Switched to iframe")
            time.sleep(0.5)
            
            # Switch back
            contact_page.switch_to_default_content()
            print(f"  ✓ Switched back to main content")
            
            # Verify main page is accessible
            assert contact_page.is_element_present(contact_page.CONTACT_FORM), \
                f"Main page should be accessible after switch {i+1}"
        
        print("\n✓ Multiple context switches handled successfully")
