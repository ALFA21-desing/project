"""
WebDriverFactory - Factory pattern for creating WebDriver instances
Supports Chrome and Firefox with configurable options
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import subprocess
import socket
import time
import urllib.request


class WebDriverFactory:
    """Factory class to create and configure WebDriver instances"""
    
    @staticmethod
    def create_driver(browser="chrome", headless=False):
        """
        Create a WebDriver instance for the specified browser
        
        Args:
            browser (str): Browser name - 'chrome' or 'firefox'
            headless (bool): Run browser in headless mode
            
        Returns:
            WebDriver: Configured WebDriver instance
        """
        if browser.lower() == "chrome":
            return WebDriverFactory._create_chrome_driver(headless)
        elif browser.lower() == "firefox":
            return WebDriverFactory._create_firefox_driver(headless)
        else:
            raise ValueError(f"Unsupported browser: {browser}. Use 'chrome' or 'firefox'")
    
    @staticmethod
    def _create_chrome_driver(headless=False):
        """Create and configure Chrome WebDriver"""
        options = webdriver.ChromeOptions()
        
        if headless:
            options.add_argument("--headless")
        
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")
        options.add_argument("--ignore-certificate-errors")
        
        service_path = ChromeDriverManager().install()
        try:
            service = ChromeService(service_path)
            driver = webdriver.Chrome(service=service, options=options)
        except Exception:
            # Fallback: start chromedriver as a subprocess and connect via RemoteWebDriver
            sock = socket.socket()
            sock.bind(('', 0))
            port = sock.getsockname()[1]
            sock.close()
            proc = subprocess.Popen([service_path, f'--port={port}'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            # wait for driver to be ready
            url = f'http://127.0.0.1:{port}/status'
            for _ in range(30):
                try:
                    with urllib.request.urlopen(url, timeout=1) as resp:
                        if resp.status == 200:
                            break
                except Exception:
                    time.sleep(0.2)
            caps = options.to_capabilities() if hasattr(options, 'to_capabilities') else {}
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            rc = RemoteConnection(f'http://127.0.0.1:{port}')
            try:
                rc.timeout = 30
            except Exception:
                pass
            driver = webdriver.Remote(command_executor=rc, desired_capabilities=caps)

        driver.implicitly_wait(10)
        return driver
    
    @staticmethod
    def _create_firefox_driver(headless=False):
        """Create and configure Firefox WebDriver"""
        options = webdriver.FirefoxOptions()
        
        if headless:
            options.add_argument("--headless")
        
        service_path = GeckoDriverManager().install()
        try:
            service = FirefoxService(service_path)
            driver = webdriver.Firefox(service=service, options=options)
        except Exception:
            # Fallback: start geckodriver subprocess and connect via Remote
            sock = socket.socket()
            sock.bind(('', 0))
            port = sock.getsockname()[1]
            sock.close()
            proc = subprocess.Popen([service_path, f'--port={port}'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            url = f'http://127.0.0.1:{port}/status'
            for _ in range(30):
                try:
                    with urllib.request.urlopen(url, timeout=1) as resp:
                        if resp.status == 200:
                            break
                except Exception:
                    time.sleep(0.2)
            caps = options.to_capabilities() if hasattr(options, 'to_capabilities') else {}
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            rc = RemoteConnection(f'http://127.0.0.1:{port}')
            try:
                rc.timeout = 30
            except Exception:
                pass
            driver = webdriver.Remote(command_executor=rc, desired_capabilities=caps)

        try:
            driver.maximize_window()
        except Exception:
            pass
        driver.implicitly_wait(10)
        return driver
