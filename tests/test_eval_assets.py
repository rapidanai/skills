"""Package integrity checks, not behavioral grading of an assistant."""
from pathlib import Path
import subprocess
import sys
import unittest


class EvalAssetsTests(unittest.TestCase):
    def test_voice_workshop_eval_assets(self):
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            [sys.executable, str(root / 'voice-workshop/evals/validate.py')],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('scenario definitions and fixture oracles validated', result.stdout)

    def test_embedded_fixture_and_scenario_validation(self):
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            [sys.executable, str(root / 'code-quality-analysis/evals/validate.py')],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('scenario definitions and fixture oracles validated', result.stdout)


if __name__ == '__main__':
    unittest.main()
