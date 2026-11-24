"""Unit tests for the voice-workshop profile helper script."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'voice-workshop/scripts/voice_profile.py'


class VoiceProfileTests(unittest.TestCase):
    def run_script(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args],
                              text=True, capture_output=True)

    def test_init_creates_a_valid_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'profile.md'
            result = self.run_script('init', '--path', str(path))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(path.is_file())
            self.assertIn('# Voice Profile', path.read_text())
            check = self.run_script('validate', '--path', str(path))
            self.assertEqual(check.returncode, 0, check.stdout + check.stderr)

    def test_init_refuses_to_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'profile.md'
            path.write_text('local edits')
            result = self.run_script('init', '--path', str(path))
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(path.read_text(), 'local edits')

    def test_init_force_overwrites(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'profile.md'
            path.write_text('local edits')
            result = self.run_script('init', '--path', str(path), '--force')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('# Voice Profile', path.read_text())

    def test_validate_reports_missing_sections(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'profile.md'
            path.write_text('# Voice Profile\n\nUpdated: 2026-01-01\n\n## Rules\n')
            result = self.run_script('validate', '--path', str(path))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('missing section: Examples', result.stdout)

    def test_validate_missing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_script('validate', '--path', str(Path(tmp) / 'nope.md'))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Missing profile', result.stdout)

    def test_show_prints_the_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'profile.md'
            self.run_script('init', '--path', str(path))
            result = self.run_script('show', '--path', str(path))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('# Voice Profile', result.stdout)

    def test_name_selects_a_named_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            env = dict(__import__('os').environ, HOME=str(home), USERPROFILE=str(home))
            result = subprocess.run(
                [sys.executable, str(SCRIPT), 'init', '--name', 'work'],
                text=True, capture_output=True, env=env,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((home / '.voice-workshop' / 'work.md').is_file())


if __name__ == '__main__':
    unittest.main()
