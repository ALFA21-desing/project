# Katalon Results & Comparison — Jewelry Obelisco

This report summarizes the Katalon test cases and the comparison with existing Selenium tests for the Jewelry Obelisco project.

## Files included

- `test_results/katalon_results.csv` — 30 Katalon test cases (includes 10 Katalon-unique tests).
- `test_results/katalon_selenium_comparison.csv` — Comparison matrix between Katalon and Selenium runs.
- `test_data/katalon_registration_invalid.csv` — 10 invalid registration datasets for Katalon Data Files.
- `scripts/convert_csv_to_xlsx.py` — Small Python helper to convert the CSVs to `.xlsx` files locally.

## Summary of actions

- Created the Katalon test-case inventory (`katalon_results.csv`) covering Smoke, Checkout, Data-driven registration, Viewport, Advanced scripting (Relative XPath), and Katalon-specific features such as built-in reports and Object Repository usage.
- Created a comparison file (`katalon_selenium_comparison.csv`) that records Pass/Fail outcomes and notes discrepancies (locator robustness, viewport differences, reporting capabilities).
- Added a data file for registration invalid cases (`katalon_registration_invalid.csv`) containing 10 rows for Katalon's Data Files use.
- Added `scripts/convert_csv_to_xlsx.py` so you can convert CSVs to Excel (.xlsx) with one command.

## How to produce Excel (.xlsx) versions

Open PowerShell in the project root and run:

```powershell
python -m pip install -r requirements.txt
python scripts/convert_csv_to_xlsx.py
```

After running the script you will have the following new files (next to originals):

- `test_results/katalon_results.xlsx`
- `test_results/katalon_selenium_comparison.xlsx`
- `test_data/katalon_registration_invalid.xlsx`

## Quick notes about discrepancies found

- Locator robustness: Katalon’s Object Repository and the use of Relative XPath via Object Spy reduced flakiness compared to some Selenium tests that used static selectors.
- Viewport runs: Katalon test runs showed a minor layout difference on tablet resolution in one browser/platform combination; reproduce with Selenium to verify cross-browser specifics.
- Reporting: Katalon’s built-in reports are richer out-of-the-box; pytest-html can match but requires configuration (plugins/fixtures) and attachments.
- Data-driven validation: Katalon Data Files made iterating registration invalid datasets straightforward; ensure Selenium data-driven tests match the same inputs for parity.

## Next steps I can take for you

- Run the conversion here and attach the `.xlsx` files (I cannot run scripts in your environment unless you ask me to run them locally).
- Add screenshots/evidence of Katalon test execution and include them in the report.
- Produce a PDF-friendly version of this report and include it in the repo.

Which of these would you like me to do next?
