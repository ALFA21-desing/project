# Quick Start Guide - Selenium Test Framework

##  Quick Setup (5 minutes)

### 1. Install Dependencies
```powershell
python -m pip install -r requirements.txt
```

### 2. Run Quick Demo Tests
```powershell
python run_quick_tests.py
```

### 3. Run Full Test Suite
```powershell
pytest -v
```

### 4. Generate HTML Report
```powershell
pytest --html=test_results/report.html --self-contained-html
```

## Quick Test Commands

### Run by Test Type
```powershell
# Smoke tests (fastest - 2-3 min)
pytest -m smoke -v

# Data-driven tests
pytest -m data_driven -v

# End-to-end tests
pytest -m e2e -v

# Cross-browser tests
pytest -m cross_browser -v

# Iframe tests
pytest -m iframe -v
```

### Run Specific Test Files
```powershell
pytest tests/test_authentication.py -v
pytest tests/test_shopping.py -v
pytest tests/test_e2e_checkout.py -v
```

### Cross-Browser Testing
```powershell
# Chrome (default)
pytest --browser=chrome -v

# Firefox
pytest --browser=firefox -v

# Headless mode
pytest --headless -v
```

##  Important Files

- **TEST_FRAMEWORK_README.md** - Complete documentation
- **requirements.txt** - Python dependencies
- **pytest.ini** - Pytest configuration
- **conftest.py** - Test fixtures and setup

##  Framework Structure

```
├── pages/          - Page Object Models
├── tests/          - Test cases
├── utils/          - Utility classes
├── test_data/      - CSV and Excel test data
└── test_results/   - Reports and screenshots
```

##  What This Framework Demonstrates

1. **Data-Driven Testing** - CSV and Excel data sources
2. **Page Object Model** - Clean, maintainable structure
3. **Dynamic Waits** - WebDriverWait for reliable tests
4. **E2E Workflows** - Complete user journeys
5. **Cross-Browser** - Chrome and Firefox support
6. **Iframe Handling** - Context switching demos
7. **Advanced Selenium** - JavaScript, screenshots, waits

##  Expected Test Results

- **Total Tests**: ~20-25 test cases
- **Execution Time**: 5-10 minutes (all tests)
- **Success Rate**: Should be 90%+ (some tests depend on page structure)

##  Troubleshooting

**Browser doesn't open:**
```powershell
# Reinstall webdriver-manager
python -m pip install --upgrade webdriver-manager
```

**Import errors:**
```powershell
# Reinstall dependencies
python -m pip install -r requirements.txt --force-reinstall
```

**Tests fail:**
- Check if website files are in correct location
- Verify base URL in pytest command
- Run with `-v` flag for detailed output

##  Need Help?

Read the complete documentation: **TEST_FRAMEWORK_README.md**
