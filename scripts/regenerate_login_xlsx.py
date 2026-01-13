"""Regenerate test_data/login_credentials.xlsx from login_credentials.csv

Run from project root:
    python scripts/regenerate_login_xlsx.py
"""
import csv
from pathlib import Path
from openpyxl import Workbook


def main():
    root = Path(__file__).resolve().parent.parent
    csv_path = root / 'test_data' / 'login_credentials.csv'
    xlsx_path = root / 'test_data' / 'login_credentials.xlsx'

    if not csv_path.exists():
        print(f"CSV not found: {csv_path}")
        return

    wb = Workbook()
    ws = wb.active

    with csv_path.open(newline='', encoding='utf-8') as fh:
        reader = csv.reader(fh)
        for row in reader:
            ws.append(row)

    wb.save(xlsx_path)
    print(f"Wrote: {xlsx_path}")


if __name__ == '__main__':
    main()
