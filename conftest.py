"""
Pytest configuration file
Contains fixtures and setup/teardown logic
"""

import pytest
from utils.WebDriverFactory import WebDriverFactory
import os


def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests: chrome or firefox"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode"
    )
    parser.addoption(
        "--base-url",
        action="store",
        default=f"file:///{os.getcwd().replace(chr(92), '/')}",
        help="Base URL of the application"
    )


@pytest.fixture(scope="function")
def driver(request):
    """
    Fixture to create and teardown WebDriver
    Scope: function - creates new driver for each test
    """
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    
    # Create driver
    driver_instance = WebDriverFactory.create_driver(browser=browser, headless=headless)
    
    # Yield driver to test
    yield driver_instance
    
    # Teardown - close driver
    driver_instance.quit()


@pytest.fixture(scope="function")
def base_url(request):
    """Fixture to provide base URL"""
    return request.config.getoption("--base-url")


@pytest.fixture(scope="class")
def driver_class(request):
    """
    Fixture for class-scoped driver
    Used when you want to share driver across multiple tests in a class
    """
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    
    driver_instance = WebDriverFactory.create_driver(browser=browser, headless=headless)
    request.cls.driver = driver_instance
    
    yield driver_instance
    
    driver_instance.quit()


# Hooks for better reporting
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results and take screenshots on failure
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        # Take screenshot on test failure
        driver = getattr(item.instance, 'driver', None) if hasattr(item, 'instance') else None
        
        if driver is None:
            # Try to get driver from fixtures
            if 'driver' in item.funcargs:
                driver = item.funcargs['driver']
        
        if driver:
            screenshot_dir = "test_results/screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = f"{screenshot_dir}/{item.name}.png"
            driver.save_screenshot(screenshot_path)
            print(f"\nScreenshot saved: {screenshot_path}")


def pytest_configure(config):
    """Create test results directory"""
    os.makedirs("test_results", exist_ok=True)
    os.makedirs("test_results/screenshots", exist_ok=True)
