#!/usr/bin/env python3
"""Convert CSV files to XLSX files using openpyxl.

Run from project root (Python 3.8+ required, openpyxl installed):

powershell
python scripts/convert_csv_to_xlsx.py

This will create .xlsx versions of CSVs placed next to the originals.
"""
import csv
from pathlib import Path
from openpyxl import Workbook


def convert(csv_path: Path, xlsx_path: Path) -> None:
    wb = Workbook()
    ws = wb.active
    with csv_path.open(newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        for row in reader:
            ws.append(row)
    wb.save(xlsx_path)


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    csv_files = [
        project_root / 'test_results' / 'katalon_results.csv',
        project_root / 'test_results' / 'katalon_selenium_comparison.csv',
        project_root / 'test_data' / 'katalon_registration_invalid.csv',
    ]

    for csv in csv_files:
        if not csv.exists():
            print(f"Skipping missing file: {csv}")
            continue
        xlsx = csv.with_suffix('.xlsx')
        try:
            print(f"Converting {csv} -> {xlsx}")
            convert(csv, xlsx)
        except Exception as e:
            print(f"Failed to convert {csv}: {e}")


if __name__ == '__main__':
    main()
