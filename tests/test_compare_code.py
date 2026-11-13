"""Verify the deterministic code comparison helper."""
from pathlib import Path
from tempfile import TemporaryDirectory
import importlib.util
import unittest


class CompareCodeTests(unittest.TestCase):
    def test_comparable_lines_and_changes(self):
        script = Path(__file__).resolve().parents[1] / 'code-quality-analysis/scripts/compare_code.py'
        spec = importlib.util.spec_from_file_location('compare_code', script)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with TemporaryDirectory() as tmp:
            before, after = Path(tmp) / 'before', Path(tmp) / 'after'
            before.mkdir()
            after.mkdir()
            (before / 'orders.py').write_text('discount = 0.05\n\n')
            (after / 'orders.py').write_text('discount = 0.10\n\n')
            result = module.compare(before, after, ['orders.py'])
            self.assertEqual(result['totals'], {'before_lines': 2, 'after_lines': 2,
                                                'net_lines': 0, 'added_lines': 1,
                                                'deleted_lines': 1})
            with self.assertRaises(ValueError):
                module.compare(before, after, ['../outside.py'])


if __name__ == '__main__':
    unittest.main()
