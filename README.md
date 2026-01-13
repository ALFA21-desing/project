
# Jewelry Obelisco — Project

Academic summary and project guide for university submission.

## Description

This is a static web project (HTML/CSS/JS) that simulates a jewelry store called "Jewelry Obelisco" and includes an automated test framework written in Python using Selenium and PyTest to validate critical functionality.

The repository contains:
- A website: front-end pages (index, catalog, detail, cart, contact).
- Cart and checkout logic (localStorage, UI, validation, animations).
- An automated test framework (POM) with utilities and data-driven tests (CSV/Excel).

## Project structure

- `website/` — Site code (HTML, CSS, JS, assets).
	- `index.html`, `catalogo.html`, `detalle.html`, `cart.html`, `contacto.html`, `style.css`, `cart.js`, `assets/`.
- `pages/` — Page Object Model classes (Python) for tests.
- `tests/` — PyTest test cases (authentication, shopping, e2e, cross-browser, iframe).
- `utils/` — Utilities: `WebDriverFactory.py`, `WaitUtility.py`, `ExcelUtility.py`.
- `test_data/` — `login_credentials.csv`, `login_credentials.xlsx`.
- `requirements.txt` — Python dependencies.
- `conftest.py`, `pytest.ini` — PyTest configuration.
- Additional documentation: `QUICKSTART.md`, `TEST_FRAMEWORK_README.md`, `COMMANDS_REFERENCE.txt`, `FINAL_SUMMARY.txt`.

## Environment requirements

- Python 3.12+
- Browsers: Google Chrome, Mozilla Firefox
- Dependencies (see `requirements.txt`):
	- selenium==3.141.0
	- pytest==9.0.2
	- webdriver-manager
	- openpyxl
	- pytest-html

Quick install:

```powershell
python -m pip install -r requirements.txt
```

## Run the site locally

The site is static; you can open `website/index.html` in a browser or serve it with a simple server:

```powershell
# From the website folder
python -m http.server 8000
# Open http://localhost:8000
```

## Run the test suite

Useful commands:

```powershell
# Run all tests (defaults to Chrome)
pytest -v

# Run tests marked as smoke
pytest -m smoke -v

# Generate HTML report
pytest --html=test_results/report.html --self-contained-html -v
```

Options available in `conftest.py` (example): `--browser chrome|firefox`, `--headless`.

## Test framework design

- Architecture: Page Object Model (POM)
- Implemented pages: `LoginPage`, `CatalogPage`, `CartPage`, `ContactPage`, `BasePage`.
- Utilities: WebDriver management (`WebDriverFactory`), data reading from CSV/Excel (`ExcelUtility`), explicit waits (`WaitUtility`).
- Test types:
	- Data-driven login tests (CSV/Excel)
	- End-to-End checkout workflow
	- Dynamic waits (WebDriverWait)
	- Cross-browser testing (Chrome/Firefox)
	- Iframe and modal interaction tests

## Main E2E flow covered

1. Login (data-driven)
2. Search product in catalog
3. Add product(s) to cart
4. Checkout process (shipping → payment → review)
5. Place order and validate success screen

## Files of interest

- `website/cart.js` — Full cart, checkout logic, animations and modals.
- `website/catalogo.html` — Product catalog with search and filters.
- `tests/test_e2e_checkout.py` — Example E2E tests.
- `tests/test_authentication.py` — Data-driven login tests.
- `utils/WebDriverFactory.py` — WebDriver construction for Chrome/Firefox.

## Notes for submission

- The project was developed as a university assignment. It includes `QUICKSTART.md` and `TEST_FRAMEWORK_README.md` with detailed instructions.
- For tests requiring drivers, the project uses `webdriver-manager` to download drivers automatically.
- The checkout flow is a local simulation (no real payments). Card validation may be relaxed for testing purposes.

## What to review in the demo

- Site navigation and responsive layout.
- Adding items to the cart and the checkout flow with animations.
- Running tests: pytest discovery, smoke runs and report generation.

## Contact / Author

Author: ALFA21-desing



