import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class InstallTests(unittest.TestCase):
    def run_install(self, *args, env=None):
        return subprocess.run([sys.executable, str(ROOT / 'install.py'), *args],
                              text=True, capture_output=True, env=env)

    def test_project_install_copies_complete_package_for_each_agent(self):
        for agent, folder in [('codex', '.agents'), ('claude', '.claude')]:
            with self.subTest(agent=agent), tempfile.TemporaryDirectory(prefix='skill project ') as tmp:
                result = self.run_install('--agent', agent, '--project', tmp)
                self.assertEqual(result.returncode, 0, result.stderr)
                dest = Path(tmp) / folder / 'skills/code-quality-analysis'
                source = ROOT / 'code-quality-analysis'
                for path in source.rglob('*'):
                    if path.is_file():
                        self.assertEqual(path.read_bytes(), (dest / path.relative_to(source)).read_bytes())

    def test_personal_install(self):
        for agent, folder in [('codex', '.agents'), ('claude', '.claude')]:
            with self.subTest(agent=agent), tempfile.TemporaryDirectory() as tmp:
                env = dict(os.environ, HOME=tmp, USERPROFILE=tmp)
                result = self.run_install('--agent', agent, env=env)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue((Path(tmp) / folder / 'skills/code-quality-analysis/SKILL.md').is_file())

    def test_hermes_active_home_and_explicit_override(self):
        with tempfile.TemporaryDirectory(prefix='hermes home ') as tmp:
            active = Path(tmp) / 'active'
            explicit = Path(tmp) / 'explicit'
            active.mkdir()
            explicit.mkdir()
            env = dict(os.environ, HERMES_HOME=str(active))
            result = self.run_install('--agent', 'hermes', env=env)
            self.assertEqual(result.returncode, 0, result.stderr)
            result = self.run_install('--agent', 'hermes', '--hermes-home', str(explicit), env=env)
            self.assertEqual(result.returncode, 0, result.stderr)
            for base in (active, explicit):
                dest = base / 'skills/software-development/code-quality-analysis'
                for path in (ROOT / 'code-quality-analysis').rglob('*'):
                    if path.is_file():
                        self.assertEqual(path.read_bytes(), (dest / path.relative_to(ROOT / 'code-quality-analysis')).read_bytes())

    def test_identical_reinstall_succeeds(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = ('--agent', 'codex', '--project', tmp)
            first = self.run_install(*args)
            self.assertEqual(first.returncode, 0, first.stderr)
            again = self.run_install(*args)
            self.assertEqual(again.returncode, 0, again.stderr)
            self.assertIn('Already installed and verified', again.stdout)

    def test_hermes_rejects_project_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_install('--agent', 'hermes', '--project', tmp)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Hermes uses a profile home', result.stderr)
            self.assertEqual(list(Path(tmp).iterdir()), [])

    def test_hermes_requires_resolved_profile(self):
        env = dict(os.environ)
        env.pop('HERMES_HOME', None)
        result = self.run_install('--agent', 'hermes', env=env)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Resolve the active Hermes profile', result.stderr)

    def test_symlink_destination_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / 'original'
            target.mkdir()
            (target / 'SKILL.md').write_text('local edits')
            dest = root / '.agents/skills/code-quality-analysis'
            dest.parent.mkdir(parents=True)
            try:
                dest.symlink_to(target, target_is_directory=True)
            except OSError:
                self.skipTest('Directory symlinks unavailable')
            result = self.run_install('--agent', 'codex', '--project', tmp)
            self.assertNotEqual(result.returncode, 0)
            self.assertTrue(dest.is_symlink())
            self.assertEqual((target / 'SKILL.md').read_text(), 'local edits')

    def test_existing_install_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / '.agents/skills/code-quality-analysis'
            dest.mkdir(parents=True)
            (dest / 'SKILL.md').write_text('local edits')
            result = self.run_install('--agent', 'codex', '--project', tmp)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Already installed', result.stderr)
            self.assertEqual((dest / 'SKILL.md').read_text(), 'local edits')
            self.assertEqual(list(dest.iterdir()), [dest / 'SKILL.md'])

    def test_missing_project_does_not_create_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / 'missing'
            result = self.run_install('--agent', 'codex', '--project', str(missing))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Directory does not exist', result.stderr)
            self.assertFalse(missing.exists())


class SelectionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.repo = self.root / 'repo'
        self.repo.mkdir()
        shutil.copy2(ROOT / 'install.py', self.repo / 'install.py')
        for name in ('first-skill', 'second-skill'):
            package = self.repo / name
            package.mkdir()
            (package / 'SKILL.md').write_text(f'---\nname: {name}\ndescription: Test fixture\n---\n')
        self.project = self.root / 'project'
        self.project.mkdir()

    def run_install(self, *args):
        return subprocess.run([sys.executable, str(self.repo / 'install.py'), *args],
                              text=True, capture_output=True)

    def test_list_without_agent_or_writes(self):
        result = self.run_install('--list')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(), ['first-skill', 'second-skill'])
        self.assertEqual(list(self.project.iterdir()), [])

    def test_select_only_requested_skill(self):
        for agent, folder in [('codex', '.agents'), ('claude', '.claude'), ('hermes', 'skills/software-development')]:
            with self.subTest(agent=agent):
                scope = '--hermes-home' if agent == 'hermes' else '--project'
                result = self.run_install('--agent', agent, scope, str(self.project), '--skills', 'second-skill')
                self.assertEqual(result.returncode, 0, result.stderr)
                dest = self.project / folder
                if agent != 'hermes':
                    dest /= 'skills'
                self.assertEqual([p.name for p in dest.iterdir()], ['second-skill'])

    def test_multiple_selection_and_all(self):
        for selection in [('--skills', 'first-skill', 'second-skill'), ('--all',)]:
            with self.subTest(selection=selection):
                result = self.run_install('--agent', 'codex', '--project', str(self.project), *selection)
                self.assertEqual(result.returncode, 0, result.stderr)
                dest = self.project / '.agents/skills'
                self.assertEqual(sorted(p.name for p in dest.iterdir()), ['first-skill', 'second-skill'])

    def test_unspecified_selection_requires_choice_for_multiple_skills(self):
        result = self.run_install('--agent', 'codex', '--project', str(self.project))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Choose --skills', result.stderr)
        self.assertEqual(list(self.project.iterdir()), [])

    def test_unknown_name_or_path_does_not_install_anything(self):
        for name in ('unknown', '../first-skill', '/tmp/first-skill'):
            result = self.run_install('--agent', 'codex', '--project', str(self.project), '--skills', 'first-skill', name)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Unknown skill', result.stderr)
            self.assertEqual(list(self.project.iterdir()), [])

    def test_conflict_preflight_preserves_other_selections(self):
        dest = self.project / '.agents/skills/second-skill'
        dest.mkdir(parents=True)
        (dest / 'SKILL.md').write_text('local changes')
        result = self.run_install('--agent', 'codex', '--project', str(self.project), '--all')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((dest.parent / 'first-skill').exists())
        self.assertEqual((dest / 'SKILL.md').read_text(), 'local changes')


if __name__ == '__main__':
    unittest.main()
