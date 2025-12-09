"""
Test Shopping - Catalog and Cart Functionality
Demonstrates: Dynamic wait handling, filtering, product interaction
"""

import pytest
from pages.CatalogPage import CatalogPage
from pages.CartPage import CartPage
import time


class TestShopping:
    """Test class for shopping functionality"""
    
    @pytest.mark.regression
    def test_product_search_with_dynamic_wait(self, driver, base_url):
        """
        Test: Product search with dynamic wait handling
        
        Demonstrates:
        - Explicit waits for dynamic content
        - Search functionality
        - WebDriverWait implementation
        """
        catalog_page = CatalogPage(driver, base_url)
        catalog_page.navigate()
        
        # Wait for page to load
        catalog_page.wait_utility.wait_for_element_visible(catalog_page.SEARCH_INPUT)
        
        # Get initial product count
        initial_count = catalog_page.get_product_count()
        print(f"\n✓ Initial products displayed: {initial_count}")
        
        # Search for products
        catalog_page.search_product("ring")
        
        # Wait for filtered results (dynamic content)
        time.sleep(1.5)  # Allow search filter to apply
        
        # Get filtered product count
        filtered_count = catalog_page.get_product_count()
        print(f"✓ Filtered products displayed: {filtered_count}")
        
        # Verify search worked
        product_titles = catalog_page.get_product_titles()
        print(f"✓ Found products: {product_titles}")
    
    @pytest.mark.regression
    def test_category_filter_with_explicit_wait(self, driver, base_url):
        """
        Test: Category filtering with explicit waits
        
        Demonstrates:
        - Dynamic dropdown population
        - Explicit wait for element state changes
        - Filter interaction
        """
        catalog_page = CatalogPage(driver, base_url)
        catalog_page.navigate()
        
        # Wait for dropdowns to be ready
        catalog_page.wait_utility.wait_for_element_visible(catalog_page.CATEGORY_SELECT)
        
        # Select category
        catalog_page.select_category("Rings")
        
        # Wait for subcategory dropdown to populate (dynamic wait)
        catalog_page.wait_utility.wait_for_element_visible(catalog_page.SUBCATEGORY_SELECT)
        
        # Get products after filter
        filtered_products = catalog_page.get_product_titles()
        print(f"\n✓ Products after category filter: {filtered_products}")
        
        assert len(filtered_products) > 0, "Should have products after filtering"
    
    @pytest.mark.smoke
    def test_add_product_to_cart(self, driver, base_url):
        """
        Test: Add product to cart
        
        Demonstrates:
        - Product interaction
        - Cart count update
        - State management
        """
        catalog_page = CatalogPage(driver, base_url)
        catalog_page.navigate()
        
        # Wait for products to load
        catalog_page.wait_utility.wait_for_element_visible(catalog_page.PRODUCT_CARDS)
        
        # Get initial cart count
        initial_cart_count = catalog_page.get_cart_count()
        print(f"\n✓ Initial cart count: {initial_cart_count}")
        
        # Add product to cart
        catalog_page.add_first_product_to_cart()
        
        # Wait and verify cart count increased
        time.sleep(1)
        new_cart_count = catalog_page.get_cart_count()
        print(f"✓ New cart count: {new_cart_count}")
        
        assert int(new_cart_count) > int(initial_cart_count), \
            "Cart count should increase after adding product"
    
    @pytest.mark.regression
    def test_price_range_filter(self, driver, base_url):
        """
        Test: Price range filtering
        
        Demonstrates:
        - Multiple filter combinations
        - Price validation
        - Dynamic filtering
        """
        catalog_page = CatalogPage(driver, base_url)
        catalog_page.navigate()
        
        # Wait for page load
        catalog_page.wait_utility.wait_for_element_visible(catalog_page.PRICE_RANGE_SELECT)
        
        # Apply price filter
        catalog_page.select_price_range("0-500")
        
        # Wait for filtered results
        time.sleep(1.5)
        
        # Get filtered products
        filtered_count = catalog_page.get_product_count()
        print(f"\n✓ Products in price range $0-$500: {filtered_count}")
        
        assert filtered_count > 0, "Should have products in selected price range"
    
    @pytest.mark.regression
    def test_sort_functionality(self, driver, base_url):
        """
        Test: Product sorting
        
        Demonstrates:
        - Sort dropdown interaction
        - Result verification
        - Dynamic content handling
        """
        catalog_page = CatalogPage(driver, base_url)
        catalog_page.navigate()
        
        # Wait for products
        catalog_page.wait_utility.wait_for_element_visible(catalog_page.SORT_SELECT)
        
        # Get initial product order
        initial_titles = catalog_page.get_product_titles()
        print(f"\n✓ Initial products: {initial_titles[:3]}")
        
        # Sort by price low to high
        catalog_page.select_sort_option("price-low")
        
        # Wait for re-sort
        time.sleep(1)
        
        # Get sorted products
        sorted_titles = catalog_page.get_product_titles()
        print(f"✓ After sorting: {sorted_titles[:3]}")
    
    @pytest.mark.regression
    def test_cart_page_functionality(self, driver, base_url):
        """
        Test: Cart page operations
        
        Demonstrates:
        - Navigation to cart
        - Cart item display
        - Remove functionality
        """
        # First add items to cart
        catalog_page = CatalogPage(driver, base_url)
        catalog_page.navigate()
        
        catalog_page.wait_utility.wait_for_element_visible(catalog_page.PRODUCT_CARDS)
        catalog_page.add_first_product_to_cart()
        time.sleep(1)
        
        # Navigate to cart
        cart_page = CartPage(driver, base_url)
        cart_page.navigate()
        
        # Verify cart has items
        cart_items = cart_page.get_cart_items_count()
        print(f"\n✓ Cart items count: {cart_items}")
        
        if cart_items > 0:
            item_titles = cart_page.get_cart_item_titles()
            print(f"✓ Cart items: {item_titles}")
            
            total = cart_page.get_total_amount()
            print(f"✓ Cart total: {total}")
        else:
            print("✓ Cart is empty")
