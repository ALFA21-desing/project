from pathlib import Path
import pytest


def pytest_collection_modifyitems(config, items):
    """Filter collected tests to only those listed in tests/selected_tests.txt (if present).

    This allows selecting a curated subset of tests without editing individual files.
    """
    sel_file = Path(__file__).parent / "selected_tests.txt"
    if not sel_file.exists():
        return

    keep = {line.strip() for line in sel_file.read_text(encoding="utf-8").splitlines() if line.strip()}
    if not keep:
        return

    kept_items = []
    deselected = []
    for item in list(items):
        if item.nodeid in keep:
            kept_items.append(item)
        else:
            deselected.append(item)

    if deselected:
        config.hook.pytest_deselected(items=deselected)
    items[:] = kept_items
