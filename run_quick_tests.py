"""
Quick Test Runner - Run sample tests to demonstrate framework
"""

import subprocess
import sys


def run_command(command, description):
    """Run a command and print results"""
    print("\n" + "="*70)
    print(f"  {description}")
    print("="*70)
    
    result = subprocess.run(command, shell=True, capture_output=False, text=True)
    return result.returncode == 0


def main():
    """Run quick test demonstrations"""
    print("\n" + "="*70)
    print("  SELENIUM TEST AUTOMATION FRAMEWORK")
    print("  Quick Test Runner")
    print("="*70)
    
    tests = [
        {
            "command": "pytest tests/test_authentication.py::TestAuthentication::test_login_page_elements -v",
            "description": "1. Smoke Test - Login Page Elements"
        },
        {
            "command": "pytest tests/test_authentication.py::TestAuthentication::test_login_with_csv_data -v -k 'credentials0 or credentials1'",
            "description": "2. Data-Driven Test - CSV Login (2 samples)"
        },
        {
            "command": "pytest tests/test_shopping.py::TestShopping::test_add_product_to_cart -v",
            "description": "3. Shopping Test - Add to Cart"
        },
        {
            "command": "pytest tests/test_shopping.py::TestShopping::test_product_search_with_dynamic_wait -v",
            "description": "4. Dynamic Wait Test - Product Search"
        },
        {
            "command": "pytest tests/test_iframe_interaction.py::TestIframeInteraction::test_iframe_interaction_on_contact_page -v",
            "description": "5. Iframe Test - Context Switching"
        }
    ]
    
    print("\nThis script will run 5 sample tests to demonstrate the framework capabilities.")
    print("Each test will open a Chrome browser and execute automatically.\n")
    
    choice = input("Do you want to continue? (y/n): ")
    
    if choice.lower() != 'y':
        print("Test execution cancelled.")
        return
    
    results = []
    for test in tests:
        success = run_command(test["command"], test["description"])
        results.append((test["description"], success))
    
    # Print summary
    print("\n" + "="*70)
    print("  TEST EXECUTION SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for description, success in results:
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"{status}: {description}")
    
    print("\n" + "="*70)
    print(f"  Results: {passed}/{total} tests passed")
    print("="*70)
    
    print("\nTo run ALL tests, use:")
    print("  pytest -v")
    print("\nTo run with HTML report:")
    print("  pytest --html=test_results/report.html --self-contained-html")
    print("\nTo run specific test categories:")
    print("  pytest -m smoke")
    print("  pytest -m e2e")
    print("  pytest -m cross_browser")


if __name__ == "__main__":
    main()
