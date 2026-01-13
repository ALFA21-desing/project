
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
# Project: E2E Web Store + Test Framework

## Professional summary

This repository contains a sample web store together with an end-to-end (E2E) test framework implemented using Selenium, pytest and a Page Object Model (POM) structure. The project has been prepared and stabilized for academic submission: broken selectors were fixed, Excel/CSV utilities were hardened, a Katalon-compatible XLSX exporter was created, and a self-contained HTML test report was produced for the curated set of 28 test cases.

## Repository contents

- `website/` — Site source (HTML, CSS, JS, assets).
- `pages/` — POM classes used by the tests.
- `tests/` — Test cases (pytest).
- `utils/` — Helper modules (for example `ExcelUtility.py`, `WebDriverFactory.py`).
- `scripts/` — Helper scripts (for example `generate_katalon_xlsx.py`).
- `test_results/` — Generated artifacts and reports (HTML, XLSX).

## Key changes made

The following fixes and improvements were applied to stabilize the project for submission:

- `pages/CatalogPage.py`: corrected selectors to match `website/catalogo.html`.
- `pages/CartPage.py`: synchronized selectors and adapted the checkout flow to call page JS functions where required.
- `pages/ContactPage.py`: updated locators to Spanish IDs (`nombre`, `mensaje`) to resolve failures related to iframe interactions.
- `utils/ExcelUtility.py`: made the Excel/CSV handling more robust.
- `scripts/generate_katalon_xlsx.py`: added a script to export the curated test list to an XLSX for Katalon; the script now enforces exporting the curated 28 tests.

## Front-end files inspected

- `website/catalogo.html`
- `website/cart.html` and `website/cart.js`
- `website/contacto.html`

## Requirements and dependencies

- Python 3.12+
- Supported browsers: Google Chrome, Mozilla Firefox
- Python packages (install with pip): `selenium`, `webdriver-manager`, `pytest`, `pytest-html`, `openpyxl`.

Quick install (PowerShell):

```powershell
python -m pip install -U pip
python -m pip install selenium webdriver-manager pytest pytest-html openpyxl
```

## Serve the site locally

The site is static; you can open `website/index.html` in a browser or serve it with a simple HTTP server:

```powershell
cd website
python -m http.server 8000
# Open http://localhost:8000
```

## Run the test suite

Recommended command to run the curated tests and generate a self-contained HTML report:

```powershell
python -m pytest -q --maxfail=1 --html=test_results/pytest_selected_report.html --self-contained-html
```

Notes:

- The curated test list is `tests/selected_tests.txt`.
- Tests use the POM classes in `pages/` and utilities in `utils/`.

## Generate Katalon XLSX

The script `scripts/generate_katalon_xlsx.py` converts `tests/selected_tests.txt` into `test_results/katalon_selected_tests.xlsx`. If the input contains more than 28 entries, the script trims the list to the curated 28 tests and logs the action.

Run (PowerShell):

```powershell
python .\scripts\generate_katalon_xlsx.py
```

Expected output when trimming occurs:

```
Input contained 29 tests; trimming to 28.
Wrote 28 tests to test_results\katalon_selected_tests.xlsx
```

## Generated artifacts

- Self-contained pytest HTML report: `test_results/pytest_selected_report.html`
- Exported Katalon XLSX: `test_results/katalon_selected_tests.xlsx` (28 rows)

## Submission recommendations

- Include `test_results/pytest_selected_report.html` and `test_results/katalon_selected_tests.xlsx` in your submission package when allowed by the assignment guidelines.
- Add a `requirements.txt` to pin exact package versions for reproducibility.
- Verify tests locally before submitting to ensure everything remains green.

## Useful Git commands (PowerShell)

```powershell
git add .
git commit -m "Prepare submission: POM fixes, Katalon exporter, pytest report"
git push origin main
```

## Next actions I can take for you

- Verify contents of `test_results/katalon_selected_tests.xlsx` and open the file.
- Add a `requirements.txt` and a short `CONTRIBUTING.md` with quick setup steps.
- Commit the remaining changes and open a pull request for review.

---
Last updated: 2026-01-13

Author: ALFA21-desing



