# Selenium Test Automation Framework
## Jewelry Obelisco E-commerce Website

###  Project Overview
This is a comprehensive Selenium test automation framework built using Python, demonstrating advanced testing concepts, design patterns, and best practices for automated web testing.

###  Framework Architecture

#### **Page Object Model (POM) Structure**
```
project/
├── pages/                      # Page Object Models
│   ├── BasePage.py            # Base class with common methods
│   ├── LoginPage.py           # Login page objects
│   ├── CatalogPage.py         # Catalog/Product page objects
│   ├── CartPage.py            # Shopping cart page objects
│   └── ContactPage.py         # Contact page objects
│
├── tests/                      # Test suites
│   ├── test_authentication.py # Data-driven login tests
│   ├── test_shopping.py       # Shopping functionality tests
│   ├── test_e2e_checkout.py   # End-to-end workflow tests
│   ├── test_cross_browser.py  # Cross-browser compatibility tests
│   └── test_iframe_interaction.py # Iframe handling tests
│
├── utils/                      # Utility classes
│   ├── WebDriverFactory.py    # WebDriver factory pattern
│   ├── ExcelUtility.py        # Data reading utilities
│   └── WaitUtility.py         # Advanced wait utilities
│
├── test_data/                  # Test data files
│   ├── login_credentials.csv  # CSV test data
│   └── login_credentials.xlsx # Excel test data
│
├── test_results/              # Test execution results
│   ├── screenshots/           # Failure screenshots
│   ├── report.html           # HTML test report
│   └── test_execution.log    # Execution logs
│
├── conftest.py               # Pytest configuration & fixtures
├── pytest.ini                # Pytest settings
└── README.md                # This file
```

### Setup Instructions

#### **1. Install Dependencies**
```powershell
# Install required Python packages
python -m pip install selenium pytest pytest-html openpyxl webdriver-manager
```

#### **2. Verify Installation**
```powershell
# Check Selenium
python -c "import selenium; print('Selenium version:', selenium.__version__)"

# Check Pytest
pytest --version
```

###  Running Tests

#### **Run All Tests**
```powershell
# Run complete test suite
pytest

# Run with verbose output
pytest -v

# Run with HTML report
pytest --html=test_results/report.html
```

#### **Run Specific Test Categories**
```powershell
# Run smoke tests only
pytest -m smoke

# Run data-driven tests
pytest -m data_driven

# Run E2E tests
pytest -m e2e

# Run cross-browser tests
pytest -m cross_browser

# Run iframe tests
pytest -m iframe
```

#### **Run Specific Test Files**
```powershell
# Run authentication tests
pytest tests/test_authentication.py

# Run shopping tests
pytest tests/test_shopping.py

# Run E2E checkout tests
pytest tests/test_e2e_checkout.py
```

#### **Cross-Browser Testing**
```powershell
# Run on Chrome (default)
pytest --browser=chrome

# Run on Firefox
pytest --browser=firefox

# Run in headless mode
pytest --headless
```

#### **Custom Base URL**
```powershell
# Use custom URL
pytest --base-url="http://localhost:8000"
```

###  Test Coverage

#### **1. Data-Driven Login Tests** (`test_authentication.py`)
- **CSV Data Source**: Reads credentials from CSV file
- **Excel Data Source**: Reads credentials from Excel file
- **Parametrized Testing**: Multiple test iterations with different data
- **Validation**: Success/failure scenarios

**Key Features:**
- ExcelUtility for data management
- Parametrized test execution
- Multiple data source support

#### **2. Shopping & Catalog Tests** (`test_shopping.py`)
- **Dynamic Wait Handling**: WebDriverWait for loading elements
- **Search Functionality**: Product search with filters
- **Category Filtering**: Dynamic dropdown interaction
- **Price Range Filtering**: Advanced filter combinations
- **Sort Operations**: Product sorting validation

**Key Features:**
- Explicit waits (WebDriverWait)
- Dynamic content handling
- Filter validation

#### **3. End-to-End Checkout** (`test_e2e_checkout.py`)
- **Complete User Journey**: Login → Search → Add to Cart → Checkout
- **Multi-Step Form**: Personal info → Shipping → Payment
- **Sequential Dependencies**: State management across pages
- **Order Confirmation**: Final verification

**Workflow Steps:**
1. Login authentication
2. Product catalog navigation
3. Search and filter
4. Add items to cart
5. Cart review
6. Multi-step checkout form
7. Order completion

#### **4. Cross-Browser Testing** (`test_cross_browser.py`)
- **Browser Support**: Chrome and Firefox
- **Parametrized Browsers**: Easy browser switching
- **Responsive Testing**: Multiple screen sizes
- **Compatibility Validation**: Feature parity across browsers

**Test Scenarios:**
- Login page on multiple browsers
- Catalog search across browsers
- Responsive layout testing

#### **5. Iframe Interaction** (`test_iframe_interaction.py`)
- **Context Switching**: Switch to iframe and back
- **Google Maps Iframe**: Real-world iframe example
- **Multiple Switches**: Stability testing
- **Form Interaction**: Post-iframe functionality

**Demonstrations:**
- switch_to.frame()
- switch_to.default_content()
- Iframe element location
- Context isolation

###  Framework Features

#### **Design Patterns**
-  **Page Object Model (POM)**: Separation of page logic and tests
-  **Factory Pattern**: WebDriverFactory for browser creation
-  **Singleton Pattern**: Configuration management
-  **Inheritance**: BasePage for code reuse

#### **Advanced Selenium Techniques**
- **Explicit Waits**: WebDriverWait with custom conditions
-  **Dynamic Element Handling**: Wait for element states
-  **Iframe Management**: Context switching
-  **JavaScript Execution**: Enhanced interactions
-  **Screenshot Capture**: Automatic on failure

#### **Test Management**
-  **Pytest Fixtures**: Setup/teardown automation
-  **Parametrization**: Data-driven testing
-  **Markers**: Test categorization
-  **HTML Reports**: pytest-html integration
-  **Logging**: Comprehensive execution logs

#### **Data Management**
-  **CSV Support**: Read test data from CSV
-  **Excel Support**: Read test data from Excel
-  **Utility Classes**: ExcelUtility for data operations
-  **Test Data Separation**: External data files

###  Test Execution Example

```powershell
# Run complete test suite with HTML report
pytest -v --html=test_results/report.html --self-contained-html

# Expected output:
# tests/test_authentication.py::TestAuthentication::test_login_with_csv_data[credentials0] PASSED
# tests/test_authentication.py::TestAuthentication::test_login_with_csv_data[credentials1] PASSED
# tests/test_shopping.py::TestShopping::test_product_search_with_dynamic_wait PASSED
# tests/test_shopping.py::TestShopping::test_add_product_to_cart PASSED
# tests/test_e2e_checkout.py::TestE2ECheckout::test_complete_checkout_workflow PASSED
# tests/test_cross_browser.py::TestCrossBrowser::test_login_page_on_multiple_browsers[chrome] PASSED
# tests/test_cross_browser.py::TestCrossBrowser::test_login_page_on_multiple_browsers[firefox] PASSED
# tests/test_iframe_interaction.py::TestIframeInteraction::test_iframe_interaction_on_contact_page PASSED
```

###  Key Highlights

#### **1. Framework Design**
- Robust POM implementation
- Reusable utility classes
- Clear separation of concerns
- Maintainable and scalable structure

#### **2. Selenium Expertise**
- Advanced wait strategies
- Cross-browser compatibility
- Iframe and modal handling
- Dynamic content interaction
- JavaScript execution

#### **3. Pytest Integration**
- Custom fixtures
- Parametrized tests
- Test markers
- HTML reporting
- Automatic screenshots on failure

#### **4. Data-Driven Testing**
- Multiple data sources (CSV/Excel)
- ExcelUtility for data management
- Parametrized test execution
- External test data management

#### **5. Real-World Scenarios**
- Complete E2E workflows
- Multi-step form handling
- Shopping cart operations
- Authentication flows
- Cross-browser validation

###  Test Markers Reference

| Marker | Description | Usage |
|--------|-------------|-------|
| `smoke` | Critical functionality tests | `pytest -m smoke` |
| `regression` | Full regression suite | `pytest -m regression` |
| `data_driven` | Data-driven tests | `pytest -m data_driven` |
| `e2e` | End-to-end workflows | `pytest -m e2e` |
| `cross_browser` | Cross-browser tests | `pytest -m cross_browser` |
| `iframe` | Iframe interaction tests | `pytest -m iframe` |
| `slow` | Long-running tests | `pytest -m slow` |

###  Configuration

#### **pytest.ini Settings**
- Test discovery patterns
- HTML report generation
- Console output formatting
- Log levels and file paths
- Custom markers

#### **conftest.py Fixtures**
- `driver`: Function-scoped WebDriver
- `base_url`: Base URL configuration
- `driver_class`: Class-scoped WebDriver
- Screenshot capture on failure
- Test results directory creation

###  Reporting

#### **HTML Report**
```powershell
pytest --html=test_results/report.html --self-contained-html
```
- Test execution summary
- Pass/fail statistics
- Execution time
- Error details
- Screenshots (on failure)

#### **Console Logs**
- Real-time test execution
- Detailed assertions
- Custom print statements
- Progress indicators

#### **Log Files**
- `test_results/test_execution.log`: Detailed execution log
- `test_results/screenshots/`: Failure screenshots

###  Best Practices Demonstrated

1. **Page Object Model**: Clean separation of test logic and page interactions
2. **DRY Principle**: Reusable methods in BasePage
3. **Explicit Waits**: Reliable dynamic content handling
4. **Data-Driven Testing**: External test data management
5. **Factory Pattern**: Flexible WebDriver creation
6. **Error Handling**: Try-except blocks with proper cleanup
7. **Logging**: Comprehensive test execution tracking
8. **Screenshot Capture**: Automatic failure documentation
9. **Code Organization**: Clear directory structure
10. **Documentation**: Comprehensive docstrings and comments

###  Running Quick Tests

```powershell
# Quick smoke test (2-3 minutes)
pytest -m smoke -v

# Quick data-driven test
pytest tests/test_authentication.py::TestAuthentication::test_login_with_csv_data -v

# Quick E2E test
pytest tests/test_e2e_checkout.py::TestE2ECheckout::test_complete_checkout_workflow -v
```

###  Additional Resources

- **Selenium Documentation**: https://www.selenium.dev/documentation/
- **Pytest Documentation**: https://docs.pytest.org/
- **Page Object Model**: https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/

###  Framework Validation

This framework demonstrates:
-  Strong coding skills (Python, OOP, design patterns)
-  Framework design expertise (POM, utilities, fixtures)
-  Advanced Selenium knowledge (waits, iframes, cross-browser)
-  Test automation best practices (data-driven, E2E, reporting)
-  Professional project structure (modular, maintainable, documented)

---

**Author**: Test Automation Framework  
**Purpose**: University Project - Selenium Testing Demonstration  
**Date**: December 2025
