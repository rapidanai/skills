"""Validate eval definitions and fixture oracles; does not grade an AI response."""
import json
from pathlib import Path
import runpy


def main():
    root = Path(__file__).resolve().parent
    suite = json.loads((root / 'cases.json').read_text())
    assert suite['schema_version'] == 1
    fixture = (root / suite['fixture']).resolve()
    assert fixture.is_relative_to(root)
    seen = set()
    for case in suite['cases']:
        assert case['id'] not in seen
        seen.add(case['id'])
        assert case['prompt'].strip()
        assert case['must'] and all(isinstance(item, str) and item.strip() for item in case['must'])
    orders = runpy.run_path(str(fixture / 'orders.py'))
    assert orders['preview_total'](100, True) == 90
    assert orders['checkout_total'](100, True) == 95
    assert orders['preview_total'](100, False) == orders['checkout_total'](100, False) == 100
    for name in ('README.md', 'ui.py', 'loader.py', 'plugins/receipt.py'):
        assert (fixture / name).is_file(), name
    print(f'PASS: {len(seen)} scenario definitions and fixture oracles validated.')
    print('This does not execute or score assistant behavior or evaluate code-quality measurement behavior.')


if __name__ == '__main__':
    main()
