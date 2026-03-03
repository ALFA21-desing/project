#!/usr/bin/env python3
"""Generate an Excel file for Katalon containing the selected 28 tests.

Reads `tests/selected_tests.txt` and writes `test_results/katalon_selected_tests.xlsx`.
"""
import os
from openpyxl import Workbook


def main():
    infile = os.path.join('tests', 'selected_tests.txt')
    outdir = 'test_results'
    os.makedirs(outdir, exist_ok=True)

    if not os.path.exists(infile):
        print(f"Input file not found: {infile}")
        return 1

    with open(infile, 'r', encoding='utf-8') as f:
        lines = [l.strip() for l in f if l.strip() and not l.strip().startswith('#')]

    # Limit to the curated 28 tests expected for Katalon export
    MAX_TESTS = 28
    original_count = len(lines)
    if original_count > MAX_TESTS:
        print(f"Input contained {original_count} tests; trimming to {MAX_TESTS}.")
        lines = lines[:MAX_TESTS]

    wb = Workbook()
    ws = wb.active
    ws.title = 'Katalon Selected Tests'
    ws.append(['TestCaseID', 'TestPath', 'Description'])

    for idx, path in enumerate(lines, start=1):
        tcid = f'TC{idx:03d}'
        ws.append([tcid, path, ''])

    outfile = os.path.join(outdir, 'katalon_selected_tests.xlsx')
    wb.save(outfile)
    print(f'Wrote {len(lines)} tests to {outfile}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
