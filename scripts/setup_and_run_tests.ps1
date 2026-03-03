# Setup and run tests script for Jewelry Obelisco
# Run this from project root in PowerShell:
# .\scripts\setup_and_run_tests.ps1

$ErrorActionPreference = 'Stop'

Write-Host "Creating virtual environment .venv..."
python -m venv .venv

Write-Host "Activating virtual environment..."
# Activate the venv for this PowerShell session
. .\.venv\Scripts\Activate.ps1

Write-Host "Upgrading pip, setuptools and wheel..."
python -m pip install --upgrade pip setuptools wheel

Write-Host "Installing test dependencies..."
python -m pip install selenium==4.10.0 webdriver-manager pytest pytest-html openpyxl

Write-Host "Running pytest and generating HTML report..."
python -m pytest -v --html=test_results/pytest_report.html --self-contained-html

Write-Host "Done. Report at test_results/pytest_report.html"

Write-Host "If installation of cffi or other binary packages fails, please install Microsoft Build Tools or run in an environment where binary wheels are available."